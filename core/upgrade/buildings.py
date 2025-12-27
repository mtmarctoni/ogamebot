from typing import Optional, List
from playwright.sync_api import Page
import isodate # type: ignore
from datetime import timedelta


from config.types import EmpireSnapshotDict, UpgradableBuilding
from core.notifications.telegram_notifier import TelegramNotifier
from typing import List, Optional
from config.types import EmpireSnapshotDict, StorageUpgradeCandidate
from config.constants import RESOURCE_TO_STORAGE, buildings

def is_upgrading(page: Page, building_id: int) -> bool:
    """
    Checks if the storage building with building_id is currently upgrading on the current planet.
    Looks for data-status="active" or a countdown timer in the technology li.
    """
    tech_li_selector = f'#technologies li.technology[data-technology="{building_id}"]'
    li = page.query_selector(tech_li_selector)
    if not li:
        return False
    # Check for data-status="active"
    if li.get_attribute('data-status') == 'active':
        return True
    # Or check for countdown timer
    countdown = li.query_selector('time.buildingCountdown')
    
    return countdown is not None

def find_storages_to_upgrade(
    snapshot: EmpireSnapshotDict, threshold: float = 0.95
) -> List[StorageUpgradeCandidate]:
    """
    Analyze the empire snapshot and return a list of storages that should be upgraded.
    Each item contains verbose info: planet, resource, current, max, percent, building_id, upgradable.
    """
    # Mapping from resource to storage building id using constants
    resource_to_building = {
        'metal': buildings.metal_storage[0],
        'crystal': buildings.crystal_storage[0],
        'deuterium': buildings.deuterium_storage[0],
    }
    results: List[StorageUpgradeCandidate] = []
    for planet in snapshot.get('planets', []):
        planet_id = planet.get('id')
        planet_name = planet.get('name')
        coords = planet.get('coordinates')
        storage = planet.get('storage', {})
        resources = planet.get('resources', {})
        buildings_data = planet.get('buildings', {})
        print(f"[DEBUG] Planet: {planet_name} ({coords})")
        print(f"  Storage: {storage}")
        print(f"  Resources: {resources}")
        print(f"  Buildings: {buildings_data}")
        for resource, building_id in resource_to_building.items():
            current = resources.get(resource)
            max_cap = storage.get(RESOURCE_TO_STORAGE[resource])
            print(f"    [DEBUG] Resource: {resource}, Current: {current}, Max: {max_cap}")
            if current is None or max_cap is None or max_cap == 0:
                print(f"      [SKIP] Missing or zero max_cap for {resource}")
                continue
            percent = current / max_cap
            building_info = buildings_data.get(str(building_id), {})
            upgradable = building_info.get('upgradable', False)
            level = building_info.get('level', '?')
            print(f"      [DEBUG] Percent: {percent:.2f}, Upgradable: {upgradable}, Level: {level}")
            if percent >= threshold and upgradable:
                print(f"      [ADD] Storage upgrade candidate for {resource}")
                results.append({
                    'planet_id': str(planet_id),
                    'planet_name': str(planet_name),
                    'coordinates': str(coords),
                    'resource': str(resource),
                    'current': int(current),
                    'max': int(max_cap),
                    'percent': float(percent),
                    'building_id': int(building_id),
                    'building_level': int(level) if isinstance(level, int) or (hasattr(level, 'isdigit') and level.isdigit()) else str(level),
                    'upgradable': bool(upgradable),
                })
            else:
                print(f"      [NO ADD] Not over threshold or not upgradable")
    return results



def check_for_upgradable_buildings(empire_data: EmpireSnapshotDict) -> List[UpgradableBuilding]:
    """
    Check for resource buildings (metal, crystal, deuterium) that are upgradable on all planets.
    Returns a list of dictionaries containing building data.
    """
    upgradable_buildings: List[UpgradableBuilding] = []

    for planet in empire_data.get('planets', []):
        planet_id = planet.get('id')
        planet_name = planet.get('name')
        coords = planet.get('coordinates')
        buildings_data = planet.get('buildings', {})

        for resource, building_id in {
            'metal': buildings.metal_mine[0],
            'crystal': buildings.crystal_mine[0],
            'deuterium': buildings.deuterium_mine[0],
        }.items():
            building_info = buildings_data.get(str(building_id), {})
            if building_info.get('upgradable', False):
                upgradable_buildings.append({
                    'planet_id': str(planet_id),
                    'planet_name': str(planet_name),
                    'coordinates': str(coords),
                    'resource': resource,
                    'building_id': building_id,
                    'level': building_info.get('level', 0),
                })

    return upgradable_buildings

def determine_building_to_upgrade(upgradable_buildings: List[UpgradableBuilding]) -> Optional[UpgradableBuilding]:
    """
    Determine which building to upgrade based on custom logic.
    For now, prioritize the lowest level building.
    """
    if not upgradable_buildings:
        return None

    return min(upgradable_buildings, key=lambda b: b['level'])

def upgrade_building(page: Page, building: UpgradableBuilding) -> int:
    """
    Perform the upgrade for the given building and return the upgrade duration.
    """
    building_id = building['building_id']
    tech_li_selector = f'#technologies li.technology[data-technology="{building_id}"] button.build-it'
    button = page.query_selector(tech_li_selector)

    if button:
        button.click()
        print(f"Clicked to open upgrade details for {building['resource']} on {building['planet_name']} ({building['coordinates']})")

        # Wait for the upgrade details modal to appear
        details_selector = f'#technologydetails[data-technology-id="{building_id}"] .build-it_wrap button.upgrade'
        page.wait_for_selector(details_selector, timeout=5000)

        # Click the actual upgrade button
        upgrade_button = page.query_selector(details_selector)
        if upgrade_button:
            upgrade_button.click()
            print(f"Upgrading {building['resource']} on {building['planet_name']} ({building['coordinates']})")

            # Extract the upgrade duration from the `datetime` attribute or text content
            countdown = page.query_selector('time.buildingCountdown')
            if countdown:
                duration_attr = countdown.get_attribute('datetime')
                if duration_attr:
                    # Parse ISO 8601 duration (e.g., PT49M15S)
                    try:
                        # Explicitly annotate the type of duration as timedelta
                        duration: timedelta = isodate.parse_duration(duration_attr)  # type: ignore
                        # Ensure `total_seconds` is treated as a callable method
                        # Explicitly cast `total_seconds` to a float before converting to int
                        # Refine type handling for `total_seconds` to ensure compatibility
                        # Final refinement: Explicitly cast `total_seconds` to a float
                        # Simplify and ensure type safety for `total_seconds`
                        # Explicitly cast `duration` to `timedelta` to ensure type safety
                        if isinstance(duration, timedelta):
                            return int(duration.total_seconds())
                        return 0
                    except Exception as e:
                        print(f"Error parsing duration: {e}")

                # Fallback: Extract duration from text content
                duration_text = countdown.inner_text()
                if duration_text:
                    import re
                    match = re.search(r'(\d+)m\s*(\d+)s', duration_text)
                    if match:
                        minutes, seconds = map(int, match.groups())
                        return minutes * 60 + seconds

    return 0

def handle_resources_upgrades(empire_data: EmpireSnapshotDict, game_page: Page, notifier: Optional[TelegramNotifier]) -> List[int]:
    """
    Checks if resource buildings (metal, crystal, deuterium) are upgradable on any planet.
    Triggers the upgrade if possible and returns a list of upgrade durations.
    """
    upgradable_buildings = check_for_upgradable_buildings(empire_data)
    upgrade_durations: List[int] = []  # Explicitly define the type of the list

    while upgradable_buildings:
        building_to_upgrade = determine_building_to_upgrade(upgradable_buildings)
        if not building_to_upgrade:
            break

        duration = upgrade_building(game_page, building_to_upgrade)
        if duration > 0:
            upgrade_durations.append(duration)

        # Re-check upgradable buildings after each upgrade
        upgradable_buildings = check_for_upgradable_buildings(empire_data)

    return upgrade_durations