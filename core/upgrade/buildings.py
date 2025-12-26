from playwright.sync_api import Page
from typing import List

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
        print(f"[DEBUG] Planet data: {planet}")
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
                    'planet_id': str(planet_id) if planet_id is not None else "",
                    'planet_name': str(planet_name) if planet_name is not None else '',
                    'coordinates': str(coords) if coords is not None else '',
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