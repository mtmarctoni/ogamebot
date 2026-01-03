from typing import List, Optional
from config.config import SOFT_CAPS
from config.types import PlanetDict, PlanetId, TechId
from playwright.sync_api import Page

from constants.energy import EnergyBuilding, EnergyBuildings
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech

def determine_energy_building_to_upgrade(building_name: EnergyBuilding, planet: PlanetDict) -> Optional[EnergyBuilding]:
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
    building_info = planet.get('buildings', {}).get(building_id, {})
    current_level = building_info.get('level', 0)
    soft_cap = SOFT_CAPS.get(building_name, 0)

    if current_level >= soft_cap:
        print(f"[DEBUG] {building_name} on {planet.get('name')} ({planet.get('coords')}) is at or above the soft cap ({soft_cap}).")
        return None

    if not building_info.get('upgradable', False):
        print(f"[DEBUG] {building_name} on {planet.get('name')} ({planet.get('coords')}) is not upgradable.")
        return None

    return building_name


def handle_energy_buildings_upgrade(planet: PlanetDict, page: Page, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of energy buildings (solar plant and fusion reactor) on a given planet.
    Checks if there is an upgradable solar plant or fusion reactor, and upgrades the first available one.
    Returns the upgrade duration if an upgrade is performed, otherwise None.
    """
    upgrade_durations: List[int] = []

    # Define the energy buildings in priority order using constants from the buildings module
    for building_name in EnergyBuilding:
        building_to_upgrade = determine_energy_building_to_upgrade(building_name, planet)
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
        print(f"[DEBUG] Upgrading {building_to_upgrade} on planet {planet.get('name')} ({planet.get('coords')})")
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
