from config.types import UpgradableLifeformBuilding
from constants.lifeform_buildings import HumanLifeformBuildingClass
from config.config import HUMAN_LIFEFORM_BUILDING_PRIORITY
from typing import List, Dict, Any

def prioritize_lifeform_buildings(buildings: list[str]) -> list[str]:
    """
    Sorts the given list of lifeform buildings based on the priority defined in the configuration.

    Args:
        buildings (list[str]): List of building names to prioritize.

    Returns:
        list[str]: Sorted list of buildings based on priority.
    """
    priority_map = {name: index for index, name in enumerate(HUMAN_LIFEFORM_BUILDING_PRIORITY)}
    return sorted(buildings, key=lambda b: priority_map.get(b, float('inf')))

def find_upgradable_lifeform_buildings(empire_data: Dict[str, Any]) -> List[UpgradableLifeformBuilding]:
    """
    Finds upgradable lifeform buildings across all planets in the empire data.

    Args:
        empire_data (Dict[str, Any]): The empire data containing planet information.

    Returns:
        List[UpgradableLifeformBuilding]: A list of upgradable buildings with planet ID and details.
    """
    upgradable_buildings: List[UpgradableLifeformBuilding] = []

    for planet in empire_data.get('planets', []):
        planet_id = planet.get('id')
        planet_name = planet.get('name')
        coords = planet.get('coords')
        lifeform_buildings_data = planet.get('lifeform_buildings', {})

        for building_id, building_info in lifeform_buildings_data.items():
            building_name = HumanLifeformBuildingClass.get_name_by_id(building_id) or "Not a lifeform building"
            if building_info.get('upgradable'):
                upgradable_buildings.append({
                    'planet_id': str(planet_id),
                    'planet_name': str(planet_name),
                    'coordinates': str(coords),
                    'building': building_name,
                    'building_id': building_id,
                    'level': building_info.get('level', 0),
                })

    return upgradable_buildings

def group_upgradable_buildings_by_planet(upgradable_buildings: List[UpgradableLifeformBuilding]) -> Dict[str, List[UpgradableLifeformBuilding]]:
    """
    Groups upgradable buildings by planet, maintaining the priority order for each planet.

    Args:
        upgradable_buildings (List[UpgradableLifeformBuilding]): List of upgradable buildings sorted by priority.

    Returns:
        Dict[str, List[UpgradableLifeformBuilding]]: A dictionary where each key is a planet ID and the value is a list of upgradable buildings for that planet.
    """
    grouped_buildings: Dict[str, List[UpgradableLifeformBuilding]] = {}

    for building in upgradable_buildings:
        planet_id = building['planet_id']
        if planet_id not in grouped_buildings:
            grouped_buildings[planet_id] = []
        grouped_buildings[planet_id].append(building)

    return grouped_buildings

def upgrade_lifeform_buildings(empire_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Loops through all planets to upgrade the first lifeform building for each planet based on priority.

    Args:
        empire_data (Dict[str, Any]): The empire data containing planet information.

    Returns:
        List[Dict[str, Any]]: A list of upgraded buildings with planet ID and upgrade duration.
    """
    upgraded_buildings = []
    upgradable_buildings = find_upgradable_lifeform_buildings(empire_data)

    # Group buildings by planet
    grouped_buildings = group_upgradable_buildings_by_planet(upgradable_buildings)

    for planet_id, buildings in grouped_buildings.items():
        building_to_upgrade = buildings[0]  # The first building is the highest priority

        # Simulate navigation and upgrade logic
        upgrade_duration = simulate_upgrade(planet_id, building_to_upgrade['building'])

        upgraded_buildings.append({
            'planet_id': planet_id,
            'building': building_to_upgrade['building'],
            'duration': upgrade_duration
        })

    return upgraded_buildings

def simulate_upgrade(planet_id: int, building: str) -> int:
    """
    Simulates the upgrade process for a building on a planet.

    Args:
        planet_id (int): The ID of the planet.
        building (str): The building to upgrade.

    Returns:
        int: The duration of the upgrade in seconds.
    """
    # Placeholder logic for simulation
    print(f"Upgrading {building} on planet {planet_id}...")
    return 3600  # Assume a fixed duration for now