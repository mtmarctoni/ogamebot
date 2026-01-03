from typing import Optional, List
from playwright.sync_api import Page

from config.config import SOFT_CAPS
from config.types import Coordinates, PlanetDict, PlanetId, PlanetName, TechId, TechLevel, TechName, UpgradableResourceBuilding
from constants.buildings import buildings
from constants.general import COMPONENTS
from constants.resources import RESOURCE_TO_STORAGE, RESOURCE_UPGRADE_PREFERENCE, ResourceClass
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from typing import List, Optional
from config.types import StorageUpgradeCandidate
from core.utils.calculate import calculate_energy_needed, can_upgrade, energy_int
from core.utils.time_utils import parse_duration

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
    planet: PlanetDict, threshold: float = 0.95
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
                'planet_id': PlanetId(str(planet_id)),
                    'planet_name': PlanetName(str(planet_name)),
                'coordinates': Coordinates(str(coords)),
                'resource': TechName(str(resource)),
                'current': int(current),
                'max': int(max_cap),
                'percent': float(percent),
                'building_id': TechId(str(building_id)),
                'building_level': TechLevel(int(level)) if isinstance(level, int) or (hasattr(level, 'isdigit') and level.isdigit()) else TechLevel(int((level))),
                'upgradable': bool(upgradable)
            })
        else:
            print(f"      [NO ADD] Not over threshold or not upgradable")
    return results



def check_for_upgradable_resource_buildings(planet: PlanetDict) -> List[UpgradableResourceBuilding]:
    """
    Check for resource buildings (metal, crystal, deuterium) that are upgradable on all planets.
    Returns a list of dictionaries containing building data.
    """
    upgradable_buildings: List[UpgradableResourceBuilding] = []

    # Debugging: Log all planets and their upgradable buildings
    # print("[DEBUG] Checking for upgradable buildings on all planets.")
    # for planet in empire_data.get('planets', []):
    #     print(f"[DEBUG] Planet: {planet.get('name')} ({planet.get('coords')})")
    #     buildings_data = planet.get('buildings', {})
    #     for building_id, building_info in buildings_data.items():
    #         print(f"    [DEBUG] Building ID: {building_id}, Info: {building_info}")

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
                'planet_id': PlanetId(str(planet_id)),  # Convert to PlanetId
                'planet_name': PlanetName(str(planet_name)),  # Convert to PlanetName
                'coordinates': Coordinates(str(coords)),  # Convert to Coordinates
                'resource': TechName(str(resource)),  # Convert to TechName
                'building_id': TechId(str(building_id)),  # Convert to TechId
                'level': TechLevel(building_info.get('level', 0)),  # Convert to TechLevel
            })

    return upgradable_buildings

def determine_building_to_upgrade(building: UpgradableResourceBuilding, planet: PlanetDict, notifier: Optional[TelegramNotifier] = None) -> Optional[UpgradableResourceBuilding]:
    """
    Determine which building to upgrade based on custom logic.
    Prioritize resource buildings (metal, crystal, deuterium) based on soft caps and relative levels.
    Notify if there is a building to upgrade but not enough energy.
    
    Args:
        building: The building data to evaluate for upgrade.
        planet: The planet dictionary containing resource and energy data.
        notifier: Optional notifier for sending user notifications.

    Returns:
        The building to upgrade if criteria are met, otherwise None.
    """
    print(f"[DEBUG] Determining if building can be upgraded: {building}")

    resource = building['resource']
    building_level = building['level']

    # Get current energy on the planet
    current_energy = energy_int(planet.get('energy', '0'))

    # Calculate energy consumption after the upgrade
    energy_needed = calculate_energy_needed(resource, building_level)

    # Check if there is enough energy for the upgrade
    if current_energy < energy_needed:
        if notifier:
            safe_notify(
                notifier,
                f"[NOTIFICATION] Not enough energy to upgrade {resource} on {building['planet_name']} ({building['coordinates']}). "
                f"Energy needed: {energy_needed}, Current energy: {current_energy}."
            )
        print(f"[DEBUG] Not enough energy to upgrade {resource} on {planet.get('name')} ({building['coordinates']}). Needed: {energy_needed}, Available: {current_energy}")
        return None

    # Retrieve resource levels
    metal, crystal, deut = ResourceClass.get_levels(planet)

    # Determine upgrade priority based on resource levels and soft caps
    if resource == ResourceClass.crystal and can_upgrade(crystal, SOFT_CAPS[ResourceClass.crystal], crystal <= metal):
        return building

    if resource == ResourceClass.metal and can_upgrade(metal, SOFT_CAPS[ResourceClass.metal], metal <= crystal + 2):
        return building

    if resource == ResourceClass.deuterium and can_upgrade(deut, SOFT_CAPS[ResourceClass.deuterium], deut < crystal - 3):
        return building

    # If no priority matches, return None
    print(f"[DEBUG] No upgrade priority matched for {resource} on {building['planet_name']} ({building['coordinates']}).")
    return None

def upgrade_building(page: Page, building: UpgradableResourceBuilding, notifier: Optional[TelegramNotifier] = None) -> int:
    """
    Perform the upgrade for the given building and return the upgrade duration.
    """
    # Navigate to the resources page of the planet
    print(f"[DEBUG] Upgrading building on planet ID {building['planet_id']}")
    navigate_to_section(page, building['planet_id'], COMPONENTS.SUPPLIES)
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
                duration_attr = countdown.get_attribute('datetime') or ""
                duration_text = countdown.inner_text() or ""
                return parse_duration(duration_attr, duration_text)
        except Exception as e:
            print(f"[ERROR] Upgrade did not start for {building['resource']} on {building['planet_name']} ({building['coordinates']}): {e}")
            return 0


    # Notify when a building has been successfully upgraded
    if notifier:
        safe_notify(notifier, f"[NOTIFICATION] Successfully upgraded {building['resource']} to level {building['level'] + 1} on {building['planet_name']} ({building['coordinates']}).")

    return 0

def handle_building_resources_upgrade(planet: PlanetDict, game_page: Page, notifier: Optional[TelegramNotifier]) -> List[int]:
    """
    Checks if resource buildings (metal, crystal, deuterium) are upgradable on any planet.
    Triggers the upgrade if possible and returns a list of upgrade durations.
    """
    # Initial check for upgradable resources buildings
    upgradable_buildings = check_for_upgradable_resource_buildings(planet)
    upgrade_durations: List[int] = []  # Explicitly define the type of the list

    if not upgradable_buildings:
        # Check if solar plant or fusion reactor can be upgraded and add them to the list

        return upgrade_durations

    # Sort the upgradable buildings list before determining which one to upgrade
    upgradable_buildings = sorted(upgradable_buildings, key=lambda b: (RESOURCE_UPGRADE_PREFERENCE.index(b['resource']), b['level']))

    print(f"[DEBUG] Found {upgradable_buildings} upgradable buildings.")

    for building in upgradable_buildings:
        building_to_upgrade = determine_building_to_upgrade(building, planet, notifier)
        print(f"[DEBUG] Determined building to upgrade: {building_to_upgrade}")
        if not building_to_upgrade:
            continue

        duration = upgrade_building(game_page, building_to_upgrade)
        if duration > 0:
            upgrade_durations.append(duration)

        # Re-check upgradable buildings after upgrading one building
        upgradable_buildings = check_for_upgradable_resource_buildings(planet)
        break  # Exit after upgrading one building

    return upgrade_durations