from typing import List, Optional
from config.types import PlanetDict, PlanetId, TechId
from playwright.sync_api import Page

from constants.energy import EnergyBuilding, EnergyBuildings
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech

def handle_energy_buildings_upgrade(planet: PlanetDict, page: Page, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of energy buildings (solar plant and fusion reactor) on a given planet.
    Checks if there is an upgradable solar plant or fusion reactor, and upgrades the first available one.
    Returns the upgrade duration if an upgrade is performed, otherwise None.
    """
    upgrade_durations: List[int] = []

    # Define the energy buildings in priority order using constants from the buildings module

    for building_name in EnergyBuilding:
        building_id = EnergyBuildings.get_id_by_name(building_name)
        building_info = planet.get('buildings', {}).get(building_id, {})
        planet_id = PlanetId(str(planet.get('id')))
        if building_info.get('upgradable', False):
            # Prepare the building data
            params: UpgradeTech = {
                'page': page,
                'planet_id': planet_id,
                'tech_id': TechId(building_id),
                'notifier': notifier
            }

            # Upgrade the building
            print(f"[DEBUG] Upgrading {building_name} on planet {planet.get('name')} ({planet.get('coords')})")
            duration = upgrade_tech(**params)

            if duration > 0:
                upgrade_durations.append(duration)
                if notifier:
                    safe_notify(notifier, f"Upgraded {building_name} on planet {planet.get('name')} ({planet.get('coords')}). Duration: {duration} seconds.")
            else:
                if notifier:
                    safe_notify(notifier, f"Failed to upgrade {building_name} on planet {planet.get('name')} ({planet.get('coords')}).")

            break  # Exit after upgrading one building
    return upgrade_durations
