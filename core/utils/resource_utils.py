import re
from typing import Optional, Dict
from playwright.sync_api import Page
from config.types import PlanetId, ResourceMinimumsType
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify

def parse_resource_value(raw_value: str) -> int:
    digits = re.sub(r"[^0-9]", "", raw_value or "")
    return int(digits) if digits else 0


def read_current_planet_resources(page: Page) -> Optional[Dict[str, int]]:
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
            value_found = parse_resource_value(raw_value)
            break

        if value_found is None:
            return None

        resources[resource_name] = value_found

    return resources


def has_minimum_resources(
    page: Page,
    planet_id: PlanetId,
    minimums: ResourceMinimumsType,
    notifier: Optional[TelegramNotifier] = None,
) -> bool:
    current_resources = read_current_planet_resources(page)
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
