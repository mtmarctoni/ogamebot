from playwright.sync_api import Page
from typing import List, Dict, Optional

from config.types import PlanetDict, PlanetId, PlanetName, UpgradableLifeformBuilding, StringCoords, TechId, TechName, TechLevel
from config.config import HUMAN_LIFEFORM_BUILDING_PRIORITY, KALESH_LIFEFORM_BUILDING_PRIORITY   
from constants.lifeform_buildings import HumanLifeformBuildingClass, KaeleshLifeformBuildingClass
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech


def prioritize_lifeform_buildings(buildings: list[str], specie: str) -> list[str]:
    """
    Sorts the given list of lifeform buildings based on the priority defined in the configuration.

    Args:
        buildings (list[str]): List of building names to prioritize.
        specie (str): The specie of the planet (e.g., 'human', 'kaelesh').

    Returns:
        list[str]: Sorted list of buildings based on priority.
    """
    if specie == 'kaelesh':
        priority_map = {name: index for index, name in enumerate(KALESH_LIFEFORM_BUILDING_PRIORITY)}
    else:  # Default to Human
        priority_map = {name: index for index, name in enumerate(HUMAN_LIFEFORM_BUILDING_PRIORITY)}

    return sorted(buildings, key=lambda b: priority_map.get(b, float('inf')))

def find_upgradable_lifeform_buildings(planet: PlanetDict) -> List[UpgradableLifeformBuilding]:
    """
    Finds upgradable lifeform buildings across all planets in the empire data.

    Args:
        planet (PlanetDict): The planet data containing lifeform information.

    Returns:
        List[UpgradableLifeformBuilding]: A list of upgradable buildings with planet ID and details.
    """
    upgradable_buildings: List[UpgradableLifeformBuilding] = []

    planet_id = planet.get('id')
    planet_name = planet.get('name') or "Unknown"
    coords = planet.get('coords') or "?"
    lifeform_buildings_data = planet.get('lifeform_buildings', {})

    # Determine the lifeform class based on the 'specie' field
    specie = planet.get('specie', '').lower()
    if specie == 'kaelesh':
        lifeform_class = KaeleshLifeformBuildingClass
    else:  # Default to Human
        lifeform_class = HumanLifeformBuildingClass

    for building_id, building_info in lifeform_buildings_data.items():
        building_name = lifeform_class.get_name_by_id(int(building_id)) or "Not a lifeform building"
        if building_info.get('upgradable'):
            upgradable_buildings.append({
                'planet_id': PlanetId(str(planet_id)),
                'planet_name': PlanetName(planet_name),
                'coordinates': StringCoords(coords),
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

def handle_lifeform_buildings_upgrade(
    planet: PlanetDict, 
    page: Page, 
    notifier: Optional[TelegramNotifier], 
) -> List[int]:
    """
    Generalized handler for upgrading lifeform buildings based on the specified lifeform.
    On moons (type=='moon'), skips all upgrades (moonbase logic handled in facilities handler).
    if planet.get('type') == 'moon':
        return []


    Args:
        planet (PlanetDict): Planet data.
        page (Page): Playwright page instance.
        notifier (Optional[TelegramNotifier]): Notifier for sending messages.

    Returns:
        List[int]: List of upgrade durations.
    """

    upgrade_durations: List[int] = []
    upgradable_buildings = find_upgradable_lifeform_buildings(planet)

    # Prioritize the upgradable buildings based on the defined priority
    prioritized_buildings = prioritize_lifeform_buildings([b['building'] for b in upgradable_buildings], planet.get('specie', 'Human').lower())

    # Filter the upgradable buildings to match the prioritized order
    upgradable_buildings = [b for name in prioritized_buildings for b in upgradable_buildings if b['building'] == name]

    # Group buildings by planet
    grouped_buildings = group_upgradable_buildings_by_planet(upgradable_buildings)

    for planet_id, buildings in grouped_buildings.items():
        building_to_upgrade = buildings[0]  # The first building is the highest priority
        building_id = building_to_upgrade['building_id']
        building_name = building_to_upgrade['building']

        # Simulate navigation and upgrade logic
        params: UpgradeTech = {
            "page": page,  # Replace with actual Page instance
            "planet_id": PlanetId(planet_id),
            "tech_id": TechId(building_id),
            "notifier": notifier
        }

        # Unpack the dictionary into the function
        duration = upgrade_tech(**params)

        if duration > 0:
            upgrade_durations.append(duration)
            print(f"[INFO] Lifeform upgrade: '{building_name}' started on planet {planet.get('name', 'Unknown')} (duration: {duration}s)")
            safe_notify(notifier, f"✅ Successfully started upgrade for '{building_name}' on planet {planet.get('name', 'Unknown')}. Duration: {duration} seconds.")
        else:
            print(f"[ERROR] Lifeform upgrade failed: '{building_name}' on planet {planet.get('name', 'Unknown')}")
            safe_notify(notifier, f"⚠️ Failed to upgrade '{building_name}' on planet {planet.get('name', 'Unknown')}. Please check manually.")

        break  # Exit after upgrading one building
    return upgrade_durations

