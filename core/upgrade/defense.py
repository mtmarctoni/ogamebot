import json
import math
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import TypeAlias, cast, Dict, Optional

from playwright.sync_api import Page

from config.config import DB_SCHEDULE_PATH
from config.types import ConfigType, DefensesType, EmpireSnapshotDict, PlanetDict
from config.shared_types import TechId
from constants.defenses import Defenses
from constants.general import COMPONENTS
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.utils.resource_utils import read_current_planet_resources
from core.utils.time_utils import minutes_to_seconds

ScheduleTaskState: TypeAlias = Dict[str, str]
ScheduleState: TypeAlias = Dict[str, ScheduleTaskState]

SCHEDULE_STATE_FILE = os.path.join(DB_SCHEDULE_PATH, "schedule_state.json")
DEFENSE_SCHEDULE_TASK = "defenses"
DEFAULT_DEFENSE_RECHECK_SECONDS = minutes_to_seconds(30)


@dataclass
class DefenseBudget:
    metal: int
    crystal: int
    deuterium: int


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _load_schedule_state() -> ScheduleState:
    if not os.path.exists(SCHEDULE_STATE_FILE):
        default_state: ScheduleState = {DEFENSE_SCHEDULE_TASK: {}}
        _save_schedule_state(default_state)
        return default_state

    try:
        with open(SCHEDULE_STATE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return {DEFENSE_SCHEDULE_TASK: {}}

    if not isinstance(data, dict):
        return {DEFENSE_SCHEDULE_TASK: {}}

    raw_schedule_state = cast(dict[object, object], data)
    state: ScheduleState = {}

    for task_name, raw_task_state in raw_schedule_state.items():
        if not isinstance(raw_task_state, dict):
            continue

        raw_task_state_dict = cast(dict[object, object], raw_task_state)
        state[str(task_name)] = {
            str(key): str(value)
            for key, value in raw_task_state_dict.items()
        }

    if DEFENSE_SCHEDULE_TASK not in state:
        state[DEFENSE_SCHEDULE_TASK] = {}

    return state


def _save_schedule_state(state: ScheduleState) -> None:
    os.makedirs(DB_SCHEDULE_PATH, exist_ok=True)
    with open(SCHEDULE_STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def _load_defense_state() -> ScheduleTaskState:
    schedule_state = _load_schedule_state()
    defense_state = schedule_state.get(DEFENSE_SCHEDULE_TASK, {})
    return dict(defense_state)


def _save_defense_state(state: ScheduleTaskState) -> None:
    schedule_state = _load_schedule_state()
    schedule_state[DEFENSE_SCHEDULE_TASK] = dict(state)
    _save_schedule_state(schedule_state)


def _get_last_run_at(state: ScheduleTaskState, planet_id: str) -> Optional[datetime]:
    raw_value = state.get(planet_id)
    if not raw_value:
        return None

    try:
        return datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _mark_defense_run(state: ScheduleTaskState, planet_id: str, when: datetime) -> None:
    state[planet_id] = when.isoformat().replace("+00:00", "Z")


def _seconds_until_due(last_run_at: Optional[datetime], interval_hours: int) -> int:
    if last_run_at is None:
        return 0

    next_run_at = last_run_at + timedelta(hours=interval_hours)
    return max(0, math.ceil((next_run_at - _now_utc()).total_seconds()))


def _calculate_defense_budget(planet: PlanetDict, defense_config: DefensesType) -> DefenseBudget:
    percentages = defense_config["resource_budget_percent"]
    resources = planet["resources"]

    return DefenseBudget(
        metal=math.floor(resources["metal"] * percentages["metal"] / 100),
        crystal=math.floor(resources["crystal"] * percentages["crystal"] / 100),
        deuterium=math.floor(resources["deuterium"] * percentages["deuterium"] / 100),
    )


def _has_budget(budget: DefenseBudget) -> bool:
    return budget.metal > 0 or budget.crystal > 0 or budget.deuterium > 0


def _get_budget_limited_max_units(defense_id: str, budget: DefenseBudget) -> int:
    costs = Defenses.get_costs_by_id(TechId(defense_id))
    limits: list[int] = []

    if costs["metal"] > 0:
        limits.append(budget.metal // costs["metal"])
    if costs["crystal"] > 0:
        limits.append(budget.crystal // costs["crystal"])
    if costs["deuterium"] > 0:
        limits.append(budget.deuterium // costs["deuterium"])

    if not limits:
        return 0

    return max(0, min(limits))


def _consume_budget(budget: DefenseBudget, defense_id: str, built_units: int) -> DefenseBudget:
    costs = Defenses.get_costs_by_id(TechId(defense_id))
    return DefenseBudget(
        metal=max(0, budget.metal - costs["metal"] * built_units),
        crystal=max(0, budget.crystal - costs["crystal"] * built_units),
        deuterium=max(0, budget.deuterium - costs["deuterium"] * built_units),
    )


def _set_build_amount(page: Page, amount: int) -> bool:
    selectors: list[str] = ["#build_amount", "input[name='build_amount']"]

    for selector in selectors:
        locator = page.locator(selector).first
        try:
            if not locator.is_visible(timeout=1000):
                continue
        except Exception:
            continue

        locator.fill(str(amount))
        return True

    return False


def _open_defense_details(page: Page, defense_id: str) -> bool:
    button_selector = f'#technologies li.technology[data-technology="{defense_id}"] button.upgrade'
    button = page.locator(button_selector).first
    try:
        if not button.is_visible(timeout=2000):
            return False
    except Exception:
        return False

    button.click()
    page.wait_for_selector(f'#technologydetails[data-technology-id="{defense_id}"]', timeout=5000)
    return True


def _start_defense_build(page: Page) -> int:
    details = page.locator("#technologydetails").first
    send_selectors: list[str] = [
        "button.upgrade[data-technology]",
        "div.build-it_wrap button.upgrade",
    ]

    for selector in send_selectors:
        button = details.locator(selector).first
        try:
            if not button.is_visible(timeout=1000):
                continue
        except Exception:
            continue

        button.click()
        break
    else:
        return 0

    countdown_selectors: list[str] = [
        "#technologydetails time.value",
        "#productionboxbuildingcomponent time",
        "time.shipyardCountdown",
    ]

    for selector in countdown_selectors:
        countdown = page.locator(selector).first
        try:
            if not countdown.is_visible(timeout=3000):
                continue
        except Exception:
            continue

        duration_text = countdown.inner_text() or ""
        digits = re.findall(r"\d+", duration_text)
        if not digits:
            continue
        if "h" in duration_text:
            if len(digits) >= 3:
                hours, minutes, seconds = map(int, digits[:3])
                return hours * 3600 + minutes * 60 + seconds + 1
            if len(digits) == 2:
                hours, minutes = map(int, digits)
                return hours * 3600 + minutes * 60 + 1
        if "m" in duration_text:
            if len(digits) >= 2:
                minutes, seconds = map(int, digits[:2])
                return minutes * 60 + seconds + 1
            return int(digits[0]) * 60 + 1
        if "s" in duration_text:
            return int(digits[0]) + 1

    return 0


def _build_defense_once(page: Page, defense_id: str, budget: DefenseBudget) -> tuple[int, int]:
    if not _open_defense_details(page, defense_id):
        return 0, 0

    budget_max_units = _get_budget_limited_max_units(defense_id, budget)
    build_units = max(0, budget_max_units)

    if build_units <= 0:
        return 0, 0

    if not _set_build_amount(page, int(build_units)):
        return 0, 0

    duration_seconds = _start_defense_build(page)
    return int(build_units), duration_seconds


def handle_scheduled_defense_build(
    page: Page,
    empire_data: EmpireSnapshotDict,
    notifier: Optional[TelegramNotifier],
    config: ConfigType,
) -> int:
    defense_config = config["defenses"]
    if not defense_config["enable_defenses"]:
        return 0

    interval_hours = max(1, int(defense_config["interval_hours"]))
    state = _load_defense_state()
    next_check_seconds = 0

    for planet in empire_data["planets"]:
        if planet.get("type") == "moon":
            continue

        planet_id = str(planet["id"])
        last_run_at = _get_last_run_at(state, planet_id)
        seconds_until_due = _seconds_until_due(last_run_at, interval_hours)
        if seconds_until_due > 0:
            next_check_seconds = seconds_until_due if next_check_seconds == 0 else min(next_check_seconds, seconds_until_due)
            continue

        budget = _calculate_defense_budget(planet, defense_config)
        if not _has_budget(budget):
            _mark_defense_run(state, planet_id, _now_utc())
            continue

        try:
            navigate_to_section(page, planet["id"], COMPONENTS.DEFENSES)
        except Exception as exc:
            print(f"[WARN] Failed to navigate to defenses page for {planet['name']}: {exc}")
            continue

        current_resources = read_current_planet_resources(page)
        if current_resources is not None:
            budget = DefenseBudget(
                metal=min(budget.metal, current_resources["metal"]),
                crystal=min(budget.crystal, current_resources["crystal"]),
                deuterium=min(budget.deuterium, current_resources["deuterium"]),
            )

        built_any = False
        for defense_id in sorted(defense_config["included_tech_ids"], key=int, reverse=True):
            if not Defenses.is_repeatable(TechId(defense_id)):
                continue

            built_units, duration_seconds = _build_defense_once(page, defense_id, budget)
            if built_units <= 0:
                continue

            built_any = True
            budget = _consume_budget(budget, defense_id, built_units)
            defense_name = Defenses.get_name_by_id(TechId(defense_id)).name
            message = (
                f"✅ Defense build started on {planet['name']} ({planet['coords']}): "
                f"{defense_name} x{built_units}"
            )
            print(message)
            safe_notify(notifier, message)

            if duration_seconds > 0:
                next_check_seconds = duration_seconds if next_check_seconds == 0 else min(next_check_seconds, duration_seconds)
            if not _has_budget(budget):
                break

        _mark_defense_run(state, planet_id, _now_utc())
        if not built_any and next_check_seconds == 0:
            next_check_seconds = DEFAULT_DEFENSE_RECHECK_SECONDS

    _save_defense_state(state)
    return next_check_seconds
