from typing import Optional, List
from playwright.sync_api import Page
import isodate # type: ignore
from datetime import timedelta

from config.types import EmpireSnapshotDict, UpgradableBuilding
from core.notifications.telegram_notifier import TelegramNotifier
from typing import List, Optional
from config.types import EmpireSnapshotDict, StorageUpgradeCandidate
from config.constants import RESOURCE_TO_STORAGE, buildings, RESOURCE_UPGRADE_PREFERENCE  # Removed unused ENERGY_CONSUMPTION import
from core.navigation.planet import navigate_to_resources_page
from core.utils.calculate import calculate_energy_needed

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

    # Debugging: Log all planets and their upgradable buildings
    print("[DEBUG] Checking for upgradable buildings on all planets.")
    for planet in empire_data.get('planets', []):
        print(f"[DEBUG] Planet: {planet.get('name')} ({planet.get('coords')})")
        buildings_data = planet.get('buildings', {})
        for building_id, building_info in buildings_data.items():
            print(f"    [DEBUG] Building ID: {building_id}, Info: {building_info}")

    for planet in empire_data.get('planets', []):
        planet_id = planet.get('id')
        planet_name = planet.get('name')
        coords = planet.get('coords')
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

def determine_building_to_upgrade(building: UpgradableBuilding, empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier] = None) -> Optional[UpgradableBuilding]:
    """
    Determine which building to upgrade based on custom logic.
    Prioritize the lowest level building that has enough energy available on the planet.
    Notify if there is a building to upgrade but not enough energy.
    """
    print(f"[DEBUG] Determining if building can be upgraded: {building}")
    planet_id = building['planet_id']
    resource = building['resource']
    building_level = building['level']
    planet = next((p for p in empire_data.get('planets', []) if str(p.get('id')) == planet_id), None)
    if not planet:
        print(f"[DEBUG] Planet with ID {planet_id} not found in empire data.")
        return None
    # Get current energy on the planet
    current_energy: int = 0
    
    # Handle energy as a string (e.g., '+328') and convert to integer
    if isinstance(planet.get('energy'), str):
        current_energy = int(planet.get('energy', '0').replace('+', ''))

    # Calculate energy consumption after the upgrade
    energy_needed = calculate_energy_needed(resource, building_level)

    if current_energy >= energy_needed:
        return building

    # Notify when there is a building to upgrade but not enough energy
    if notifier is not None:
        notifier.send_message(
            f"[NOTIFICATION] Not enough energy to upgrade {building['resource']} on {building['planet_name']} ({building['coordinates']}). "
            f"Energy needed: {energy_needed}, Current energy: {current_energy}."
        )
    
    print(f"[DEBUG] Not enough energy to upgrade {resource} on {planet.get('name')} ({building['coordinates']}). Needed: {energy_needed}, Available: {current_energy}")

    return None

def upgrade_building(page: Page, building: UpgradableBuilding, notifier: Optional[TelegramNotifier] = None) -> int:
    """
    Perform the upgrade for the given building and return the upgrade duration.
    """
    # Navigate to the resources page of the planet
    print(f"[DEBUG] Upgrading building on planet ID {building['planet_id']}")
    navigate_to_resources_page(page, building['planet_id'])
    print(f"[DEBUG] Navigated to planet ID {building['planet_id']} for upgrading.")

    building_id = building['building_id']
    tech_li_selector = f'#technologies li.technology[data-technology="{building_id}"] button.upgrade'
    button = page.query_selector(tech_li_selector)

    if button:
        button.click()
        print(f"Clicked to open upgrade details for {building['resource']} on {building['planet_name']} ({building['coordinates']})")

        # Wait for the building state to update (e.g., countdown timer or level change)
        try:
            page.wait_for_selector('time.buildingCountdown', state="visible", timeout=5000)  # Adjust timeout as needed
            print(f"[DEBUG] Upgrade started for {building['resource']} on {building['planet_name']} ({building['coordinates']})")
            # Extract the upgrade duration from the countdown timer
            countdown = page.locator('time.buildingCountdown').first
            if countdown:
                duration_attr = countdown.get_attribute('datetime')
                if duration_attr:
                    try:
                        duration: timedelta = isodate.parse_duration(duration_attr) # type: ignore
                        if isinstance(duration, timedelta):
                            return int(duration.total_seconds())
                    except Exception as e:
                        print(f"[ERROR] Failed to parse upgrade duration: {e}")


                # Fallback: Extract duration from text content
                duration_text = countdown.inner_text()
                if duration_text:
                    import re
                    match = re.search(r'(\d+)m\s*(\d+)s', duration_text)
                    if match:
                        minutes, seconds = map(int, match.groups())
                        return minutes * 60 + seconds
        except Exception as e:
            print(f"[ERROR] Upgrade did not start for {building['resource']} on {building['planet_name']} ({building['coordinates']}): {e}")
            return 0


    # Notify when a building has been successfully upgraded
    if notifier:
        notifier.send_message(
            f"[NOTIFICATION] Successfully upgraded {building['resource']} to level {building['level'] + 1} on {building['planet_name']} ({building['coordinates']})."
        )

    return 0

def handle_resources_upgrades(empire_data: EmpireSnapshotDict, game_page: Page, notifier: Optional[TelegramNotifier]) -> List[int]:
    """
    Checks if resource buildings (metal, crystal, deuterium) are upgradable on any planet.
    Triggers the upgrade if possible and returns a list of upgrade durations.
    """
    upgradable_buildings = check_for_upgradable_buildings(empire_data)
    upgrade_durations: List[int] = []  # Explicitly define the type of the list

    # Sort the upgradable buildings list before determining which one to upgrade
    upgradable_buildings = sorted(upgradable_buildings, key=lambda b: (RESOURCE_UPGRADE_PREFERENCE.index(b['resource']), b['level']))

    print(f"[DEBUG] Found {upgradable_buildings} upgradable buildings.")
    if not upgradable_buildings:
        print("No resource buildings to upgrade.")
        return upgrade_durations

    for building in upgradable_buildings:
        building_to_upgrade = determine_building_to_upgrade(building, empire_data, notifier)
        print(f"[DEBUG] Determined building to upgrade: {building_to_upgrade}")
        if not building_to_upgrade:
            continue

        duration = upgrade_building(game_page, building_to_upgrade)
        if duration > 0:
            upgrade_durations.append(duration)

        # Re-check upgradable buildings after upgrading one building
        upgradable_buildings = check_for_upgradable_buildings(empire_data)
        break  # Exit after upgrading one building

    return upgrade_durations