from typing import cast, Type
from playwright.sync_api import Page
from typing import List, Dict, Optional

from config.types import ConfigType, LifeformBuildingsType, PlanetDict, PlanetId, PlanetName, UpgradableLifeformBuilding, StringCoords, TechId, TechName, TechLevel, LIFEFORM_BUILDING_ENUM_MAP, LIFEFORM_BUILDING_CLASS_MAP
from constants.lifeforms import Lifeforms
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech


def prioritize_lifeform_buildings(
    buildings: List[TechName],
    prioritized_lifeform_buildings: List[LifeformBuildingsType]
) -> List[LifeformBuildingsType]:
    """
    Sorts the given list of lifeform buildings based on the priority defined in the configuration.

    Args:
        buildings (list[str]): List of building names to prioritize.
        specie (str): The specie of the planet (e.g., 'human', 'kaelesh').

    Returns:
        list[str]: Sorted list of buildings based on priority.
    """
    sorted_buildings: List[LifeformBuildingsType] = []
    lifeform_buildings = cast(List[LifeformBuildingsType], buildings)
    for priority_building in prioritized_lifeform_buildings:
        for building in lifeform_buildings:
            if building == priority_building:
                sorted_buildings.append(building)

    return sorted_buildings

def find_upgradable_lifeform_buildings(planet: PlanetDict) -> List[UpgradableLifeformBuilding]:
    """
    Finds upgradable lifeform buildings across all planets in the empire data.

    Args:
        planet (PlanetDict): The planet data containing lifeform information.

    Returns:
        List[UpgradableLifeformBuilding]: A list of upgradable buildings with planet ID and details.
    """
    upgradable_buildings: List[UpgradableLifeformBuilding] = []

    planet_id = planet['id']
    planet_name = planet['name']
    coords = planet['coords']
    lifeform_buildings_data = planet['lifeform_buildings']
    
    # Determine the lifeform type for this planet
    lifeform_str = planet['specie'].lower()

    try:
        lifeform = Lifeforms(lifeform_str)
    except ValueError:
        print(f"[ERROR] Unknown lifeform specie: {lifeform_str}. Skipping building lookup.")
        return upgradable_buildings
    
    # Get the appropriate building class for ID lookups
    building_class = LIFEFORM_BUILDING_CLASS_MAP[lifeform]

    for building_id, building_info in lifeform_buildings_data.items():
        try:
            building_name = building_class.get_name_by_id(building_id)
        except ValueError:
            print(f"[WARN] Unknown building ID {building_id} for {lifeform.value} on planet {planet_name}")
            continue
            
        if building_info['upgradable'] is True:
            upgradable_buildings.append({
                'planet_id': PlanetId(str(planet_id)),
                'planet_name': PlanetName(planet_name),
                'coordinates': StringCoords(coords),
                'building': cast(TechName, building_name),
                'building_id': TechId(building_id),
                'level': TechLevel(building_info['level']),
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
    config: ConfigType,
    notifier: Optional[TelegramNotifier]
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

    # Find all upgradable lifeform buildings on the planet
    upgradable_buildings = find_upgradable_lifeform_buildings(planet)
    
    # Convert to Lifeforms enum
    lifeform = Lifeforms(planet['specie'].lower())

    # get prioritized upgradable lifeform buildings from config
    # Convert config strings to the appropriate Enum type based on lifeform
    enum_class: Type[LifeformBuildingsType] = LIFEFORM_BUILDING_ENUM_MAP[lifeform]
    prioritized_lifeform_buildings: List[LifeformBuildingsType] = [
        enum_class(b) for b in config["upgrades"]['priorities']['lifeform_buildings'][lifeform.value]
    ]

    building_list: List[TechName] =  [b['building'] for b in upgradable_buildings]

    # Prioritize the upgradable buildings based on the defined priority
    prioritized_upgradable_lifeform_buildings = prioritize_lifeform_buildings(building_list, prioritized_lifeform_buildings)

    # Filter the upgradable buildings to match the prioritized order
    upgradable_buildings = [b for name in prioritized_upgradable_lifeform_buildings for b in upgradable_buildings if b['building'] == name]

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
            print(f"[INFO] Lifeform upgrade: '{building_name}' started on planet {planet['name']} (duration: {duration}s)")
            safe_notify(notifier, f"✅ Successfully started upgrade for '{building_name}' on planet {planet['name']}. Duration: {duration} seconds.")
        else:
            print(f"[ERROR] Lifeform upgrade failed: '{building_name}' on planet {planet['name']}")
            safe_notify(notifier, f"⚠️ Failed to upgrade '{building_name}' on planet {planet['name']}. Please check manually.")

        break  # Exit after upgrading one building
    return upgrade_durations

