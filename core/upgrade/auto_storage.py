from typing import Optional, List, Tuple
from playwright.sync_api import Page

from config.types import EmpireSnapshotDict
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.buildings import find_storages_to_upgrade, is_upgrading
from core.navigation.planet import navigate_to_resources_page

def click_upgrade_button(page: Page, building_id: int) -> Tuple[bool, Optional[int]]:
    """
    Clicks the upgrade button for the given building ID on the current planet.
    Returns a tuple (bool, Optional[int]):
    - True if upgrade was triggered, False otherwise.
    - The upgrade duration in seconds, or None if not available.
    """
    # Find the correct upgrade button inside #technologies for the given building_id
    selector = f'#technologies li.technology[data-technology="{building_id}"] button.upgrade'
    try:
        page.wait_for_selector(selector, timeout=3000)
        btn = page.query_selector(selector)
        if btn:
            btn.click()
            # Wait up to 5 seconds for confirmation
            for _ in range(10):
                if is_upgrading(page, building_id):
                    # Extract upgrade duration from the page
                    duration_selector = '#technologies li.technology.active time.countdown.buildingCountdown'
                    try:
                        time_element = page.query_selector(duration_selector)
                        if time_element:
                            start_attr = time_element.get_attribute("data-start")
                            end_attr = time_element.get_attribute("data-end")
                            if start_attr and end_attr:
                                start = int(start_attr)
                                end = int(end_attr)
                                duration_seconds = end - start
                                return True, duration_seconds
                            return True, None
                    except Exception:
                        return True, None
                page.wait_for_timeout(500)
    except Exception:
        pass
    return False, None

def upgrade_full_storages(snapshot: EmpireSnapshotDict, page: Page, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Finds storages to upgrade and triggers the upgrade process using Playwright.
    Returns a list of upgrade durations (in seconds) for triggered upgrades.
    """
    storages_to_upgrade = find_storages_to_upgrade(snapshot)
    if not storages_to_upgrade:
        print("No storages need upgrading.")
        return []

    upgrade_durations: List[int] = []
    current_planet_id = None  # Track the current planet ID to avoid redundant navigation

    for storage in storages_to_upgrade:
        if current_planet_id != storage['planet_id']:
            print(f"[DEBUG] Navigating to planet ID {storage['planet_id']}.")
            navigate_to_resources_page(page, storage['planet_id'])
            current_planet_id = storage['planet_id']
        else:
            print(f"[DEBUG] Already on planet ID {storage['planet_id']}, skipping navigation.")

        print(f"[UPGRADE] {storage['planet_name']} {storage['coordinates']}: {storage['resource']} is {storage['percent']*100:.1f}% full (level {storage['building_level']}). Should upgrade building ID {storage['building_id']}.")
        if notifier:
            try:
                notifier.send_message(
                    f"⚠️ STORAGE ALERT: {storage['planet_name']} {storage['coordinates']}: {storage['resource'].title()} storage at {int(storage['percent']*100)}% (Level {storage['building_level']}, {storage['current']}/{storage['max']}) needs upgrade."
                )
            except Exception as e:
                print(f"[TELEGRAM ERROR] Could not send storage alert: {e}")
        try:
            upgraded, duration = click_upgrade_button(page, storage['building_id'])
            if upgraded:
                print(f"[ACTION] Upgrade triggered for {storage['resource']} storage on {storage['planet_name']}.")
                if duration is not None:
                    upgrade_durations.append(duration)
                if notifier:
                    notifier.send_message(f"✅ Upgrade triggered for {storage['resource'].title()} storage on {storage['planet_name']}.")
            else:
                print(f"[WARN] Could not trigger upgrade for {storage['resource']} storage on {storage['planet_name']}.")
        except Exception as e:
            print(f"[ERROR] Failed to upgrade {storage['resource']} storage on {storage['planet_name']}: {e}")
            if notifier:
                notifier.send_message(f"❌ Failed to upgrade {storage['resource'].title()} storage on {storage['planet_name']}: {e}")

    return upgrade_durations
