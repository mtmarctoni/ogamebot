from playwright.sync_api import Page
from typing import List, Dict, Optional

from config.types import EmpireSnapshotDict, PlanetId, PlanetName, UpgradableLifeformBuilding, Coordinates, TechId, TechName, TechLevel
from config.config import HUMAN_LIFEFORM_BUILDING_PRIORITY
from constants.lifeform_buildings import HumanLifeformBuildingClass
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.actions import UpgradeTech, upgrade_tech


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

def find_upgradable_lifeform_buildings(empire_data: EmpireSnapshotDict) -> List[UpgradableLifeformBuilding]:
    """
    Finds upgradable lifeform buildings across all planets in the empire data.

    Args:
        empire_data (Dict[str, Any): The empire data containing planet information.

    Returns:
        List[UpgradableLifeformBuilding]: A list of upgradable buildings with planet ID and details.
    """
    upgradable_buildings: List[UpgradableLifeformBuilding] = []

    for planet in empire_data.get('planets', []):
        planet_id = planet.get('id')
        planet_name = planet.get('name') or "Unknown"
        coords = planet.get('coords') or "?"
        lifeform_buildings_data = planet.get('lifeform_buildings', {})

        for building_id, building_info in lifeform_buildings_data.items():
            building_name = HumanLifeformBuildingClass.get_name_by_id(int(building_id)) or "Not a lifeform building"
            if building_info.get('upgradable'):
                upgradable_buildings.append({
                    'planet_id': PlanetId(str(planet_id)),
                    'planet_name': PlanetName(planet_name),
                    'coordinates': Coordinates(coords),
                    'building': TechName(building_name),
                    'building_id': TechId(building_id),
                    'level': TechLevel(building_info.get('level', 0)),
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

def handle_lifeform_uildings_upgrade(empire_data: EmpireSnapshotDict, page: Page, notifier: Optional[TelegramNotifier]) -> List[int]:
    """
    Loops through all planets to upgrade the first lifeform building for each planet based on priority.

    Args:
        empire_data (Dict[str, Any]): The empire data containing planet information.

    Returns:
        List[Dict[str, Any]]: A list of upgraded buildings with planet ID and upgrade duration.
    """
    upgrade_durations: List[int] = []
    upgradable_buildings = find_upgradable_lifeform_buildings(empire_data)

    # Group buildings by planet
    grouped_buildings = group_upgradable_buildings_by_planet(upgradable_buildings)

    for planet_id, buildings in grouped_buildings.items():
        building_to_upgrade = buildings[0]  # The first building is the highest priority
        building_id = building_to_upgrade['building_id']

        # Simulate navigation and upgrade logic
        params: UpgradeTech = {
            "page": page,  # Replace with actual Page instance
            "planet_id": str(planet_id),
            "tech_id": str(building_id),
            "notifier": notifier
        }

        # Unpack the dictionary into the function
        duration = upgrade_tech(**params)

        if duration > 0:
            upgrade_durations.append(duration)

        break  # Exit after upgrading one building

    return upgrade_durations

