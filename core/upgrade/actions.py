import re
from typing import Optional, TypedDict, Dict
from config.types import PlanetId, TechId, ResourceMinimumsType
from constants.general import TechIdToSection
from core.navigation.planet import navigate_to_section
from core.utils.time_utils import get_countdown_selector, parse_duration
from playwright.sync_api import Page
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify

class UpgradeTech(TypedDict):
    page: Page
    planet_id: PlanetId
    tech_id: TechId
    notifier: Optional[TelegramNotifier]
    resource_minimums: ResourceMinimumsType


def _parse_resource_value(raw_value: str) -> int:
    digits = re.sub(r"[^0-9]", "", raw_value or "")
    return int(digits) if digits else 0


def _read_current_planet_resources(page: Page) -> Optional[Dict[str, int]]:
    selectors = {
        "metal": ["#resources_metal"],
        "crystal": ["#resources_crystal"],
        "deuterium": ["#resources_deuterium"],
    }

    resources: Dict[str, int] = {}

    for resource_name, selector_list in selectors.items():
        value_found = None
        for selector in selector_list:
            locator = page.locator(selector).first
            try:
                if not locator.is_visible(timeout=1000):
                    continue
            except Exception:
                continue

            raw_value = (
                locator.get_attribute("data-raw")
                or locator.get_attribute("data-value")
                or locator.get_attribute("data-amount")
                or locator.inner_text()
                or ""
            )
            value_found = _parse_resource_value(raw_value)
            break

        if value_found is None:
            return None

        resources[resource_name] = value_found

    return resources


def _has_minimum_resources(
    page: Page,
    planet_id: PlanetId,
    minimums: ResourceMinimumsType,
    notifier: Optional[TelegramNotifier] = None,
) -> bool:
    current_resources = _read_current_planet_resources(page)
    if current_resources is None:
        print(f"[WARN] Could not read current resources for planet ID {planet_id}. Skipping minimum resource check.")
        return True

    below_minimum = [
        resource_name
        for resource_name in ("metal", "crystal", "deuterium")
        if current_resources.get(resource_name, 0) < minimums[resource_name]
    ]

    if not below_minimum:
        return True

    details = ", ".join(
        [
            f"{name}: {current_resources.get(name, 0)} < min {minimums[name]}"
            for name in below_minimum
        ]
    )
    msg = f"[WARN] Resource minimum check failed on planet ID {planet_id}: {details}. Upgrade skipped."
    print(msg)
    safe_notify(notifier, msg)
    return False

def upgrade_tech(
    *,
    page: Page,
    planet_id: PlanetId,
    tech_id: TechId,
    notifier: Optional[TelegramNotifier] = None,
    resource_minimums: ResourceMinimumsType,
) -> int:
    """
    Perform the upgrade for any technology (building, research, ship, etc.) and return the upgrade duration.

    Args:
        page (Page): The Playwright page instance.
        params (Dict[str, Any]): A dictionary containing all necessary parameters, including:
            - planet_id (str): The ID of the planet where the upgrade is to be performed.
            - tech_id (str | int): The unique ID of the technology to upgrade.
        notifier (Optional[TelegramNotifier]): Notifier for sending upgrade notifications.

    Returns:
        int: The duration of the upgrade in seconds.
    """

    # Extract the section based on tech_id
    section = TechIdToSection.get_section(tech_id)  # Removed `.value` to use the COMPONENTS enum directly

    # Navigate directly to the planet and component using the extracted section
    navigate_to_section(page, planet_id, section)
    print(f"[DEBUG] Navigated to planet ID {planet_id} for upgrading tech ID {tech_id} in section {section.value}.")

    if not _has_minimum_resources(page, planet_id, resource_minimums, notifier):
        return 0

    # Locate the upgrade button for the technology
    tech_li_selector = f'#technologies li.technology[data-technology="{tech_id}"] button.upgrade'
    button = page.query_selector(tech_li_selector)

    if button:
        button.click()
        print(f"[DEBUG] Clicked upgrade button for tech ID {tech_id} on planet ID {planet_id}.")

        selector: str = get_countdown_selector(section)

        # Wait for the building state to update (e.g., countdown timer or level change)
        try:
            page.wait_for_selector(selector, state="visible", timeout=5000)  # Adjust timeout as needed
            countdown = page.locator(selector).first
            if countdown:
                _has_minimum_resources(page, planet_id, resource_minimums, notifier)
                duration_attr = countdown.get_attribute('datetime') or ""
                duration_text = countdown.inner_text() or ""
                return parse_duration(duration_attr, duration_text)
        except Exception as e:
            print(f"[ERROR] Upgrade did not start for tech ID {tech_id} on planet ID {planet_id}: {e}")
            return 0

    print(f"[ERROR] Upgrade button not found for tech ID {tech_id} on planet ID {planet_id}.")
    
    # Handle notifier errors gracefully
    safe_notify(notifier, f"[NOTIFICATION] Failed to upgrade tech ID {tech_id} on planet ID {planet_id}.")

    return 0