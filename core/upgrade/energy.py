from typing import Dict, List, Optional
from config.types import ConfigType
from config.shared_types import PlanetDict, PlanetId, TechId, TechLevel
from playwright.sync_api import Page

from constants.energy import EnergyBuilding, EnergyBuildings
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech

def determine_energy_building_to_upgrade(building_name: EnergyBuilding, planet: PlanetDict, soft_caps: Dict[EnergyBuilding, TechLevel]) -> Optional[EnergyBuilding]:
    """
    Determine which energy building to upgrade based on soft caps.

    Args:
        building_name: The name of the energy building (e.g., Solar Plant, Fusion Plant).
        planet: The planet dictionary containing building data.
        notifier: Optional notifier for sending user notifications.

    Returns:
        The energy building to upgrade if criteria are met, otherwise None.
    """
    building_id = EnergyBuildings.get_id_by_name(building_name)
    building_info = planet['buildings'].get(building_id, {})
    current_level = building_info['level']

    if current_level >= soft_caps[building_name]:
        print(f"[WARN] {building_name} on {planet['name']} ({planet['coords']}) is already at soft cap ({soft_caps}).")
        return None

    if not building_info['upgradable']:
        # [INFO] {building_name} on {planet.get('name')} ({planet.get('coords')}) is not upgradable.
        return None

    return building_name


def handle_energy_buildings_upgrade(planet: PlanetDict, page: Page, config: ConfigType, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of energy buildings (solar plant and fusion reactor) on a given planet.
    Checks if there is an upgradable solar plant or fusion reactor, and upgrades the first available one.
    Returns the upgrade duration if an upgrade is performed, otherwise None.
    On moons (type=='moon'), skips all upgrades (moonbase logic handled in facilities handler).
    """
    if planet.get('type') == 'moon':
        return []
    upgrade_durations: List[int] = []

    soft_level_caps = config["upgrades"]["soft_level_caps"]['energy']
    soft_level_caps = {EnergyBuilding(k): v for k, v in soft_level_caps.items()}

    # Define the energy buildings in priority order using constants from the buildings module
    for building_name in EnergyBuilding:
        building_to_upgrade = determine_energy_building_to_upgrade(building_name, planet, soft_level_caps)
        if not building_to_upgrade:
            continue

        building_id = EnergyBuildings.get_id_by_name(building_to_upgrade)
        params: UpgradeTech = {
            'page': page,
            'planet_id': PlanetId(str(planet.get('id'))),
            'tech_id': TechId(building_id),
            'notifier': notifier
        }

        # Upgrade the building
        print(f"[INFO] Upgrading {building_to_upgrade} on planet {planet.get('name')} ({planet.get('coords')})")
        duration = upgrade_tech(**params)

        if duration > 0:
            upgrade_durations.append(duration)
            if notifier:
                safe_notify(notifier, f"Upgraded {building_to_upgrade} on planet {planet.get('name')} ({planet.get('coords')}). Duration: {duration} seconds.")
        else:
            if notifier:
                safe_notify(notifier, f"Failed to upgrade {building_to_upgrade} on planet {planet.get('name')} ({planet.get('coords')}).")

        break  # Exit after upgrading one building

    return upgrade_durations
