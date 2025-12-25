from typing import List, Dict, Any
from config.types import EmpireSnapshotDict
from config.constants import buildings

def find_storages_to_upgrade(snapshot: EmpireSnapshotDict, threshold: float = 0.95) -> List[Dict[str, Any]]:
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
    results: List[Dict[str, Any]] = []
    for planet in snapshot.get('planets', []):
        planet_name = planet.get('name')
        coords = planet.get('coordinates')
        storage = planet.get('storage', {})
        resources = planet.get('resources', {})
        buildings_data = planet.get('buildings', {})
        for resource, building_id in resource_to_building.items():
            current = resources.get(resource)
            max_cap = storage.get(resource)
            if current is None or max_cap is None or max_cap == 0:
                continue
            percent = current / max_cap
            building_info = buildings_data.get(str(building_id), {})
            upgradable = building_info.get('upgradable', False)
            level = building_info.get('level', '?')
            if percent >= threshold and upgradable:
                results.append({
                    'planet': planet_name,
                    'coordinates': coords,
                    'resource': resource,
                    'current': current,
                    'max': max_cap,
                    'percent': percent,
                    'building_id': building_id,
                    'building_level': level,
                    'upgradable': upgradable,
                })
    return results