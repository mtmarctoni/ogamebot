import re
from typing import Optional, TypedDict

from playwright.sync_api import Page


class FleetSlotsInfo(TypedDict):
    current_expeditions: int
    max_expeditions: int
    current_fleets: int
    max_fleets: int
    available_expeditions: int
    available_fleets: int
    available_joint: int


def _parse_slots_text(slots_text: str) -> Optional[FleetSlotsInfo]:
    slots_text_clean = slots_text.replace("\n", " ").replace("\r", "")

    exp_match = re.search(r"Expeditions:\s*(\d+)/(\d+)", slots_text_clean)
    fleet_match = re.search(r"Fleets:\s*(\d+)/(\d+)", slots_text_clean)

    if not exp_match or not fleet_match:
        return None

    current_exp = int(exp_match.group(1))
    max_exp = int(exp_match.group(2))
    current_fleets = int(fleet_match.group(1))
    max_fleets = int(fleet_match.group(2))

    available_expeditions = max(0, max_exp - current_exp)
    available_fleets = max(0, max_fleets - current_fleets)

    return {
        "current_expeditions": current_exp,
        "max_expeditions": max_exp,
        "current_fleets": current_fleets,
        "max_fleets": max_fleets,
        "available_expeditions": available_expeditions,
        "available_fleets": available_fleets,
        "available_joint": min(available_expeditions, available_fleets),
    }


def get_fleet_slots_info(page: Page, timeout_ms: int = 5000) -> Optional[FleetSlotsInfo]:
    page.wait_for_selector("#slots", timeout=timeout_ms)
    slots_text = page.locator("#slots").inner_text()
    return _parse_slots_text(slots_text)
