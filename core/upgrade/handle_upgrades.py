from typing import List, Optional
from playwright.sync_api import Page

from config.types import ConfigType, EmpireSnapshotDict
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.auto_storage import upgrade_full_storages
from core.upgrade.energy import handle_energy_buildings_upgrade
from core.upgrade.facilities import handle_facilities_building_upgrades
from core.upgrade.lifeform_buildings import handle_lifeform_buildings_upgrade
from core.upgrade.buildings import handle_building_resources_upgrade
from core.upgrade.research import handle_research_upgrades

def handle_upgrades(empire_data: EmpireSnapshotDict, page: Page, notifier: Optional[TelegramNotifier], config: ConfigType) -> int:
    """
    Handles upgrades for all planets in the empire data.

    Args:
        empire_data (dict): Data containing information about all planets.
        page: Playwright page object for interacting with the game.
        notifier: TelegramNotifier instance for sending notifications.
    """

    # Initialize total_durations to ensure it is always defined
    total_durations: List[int] = []

    # Iterate through all planets and handle upgrades for each
    for planet in empire_data["planets"]:
        planet_name = planet.get('name', 'Unknown')
        planet_id = planet.get('id', 'Unknown')
        print(f"\nProcessing upgrades for planet: {planet_name} (ID: {planet_id})")

        # Check and upgrade facilities for the planet
        if config.get("enable_facility_upgrades", True):
            facility_upgrade_durations = handle_facilities_building_upgrades(planet, page, notifier)
        else:
            facility_upgrade_durations = []

        # Check and upgrade resources (metal, crystal, deuterium) for the planet
        if config.get("enable_resource_upgrades", True):
            resource_upgrade_durations = handle_building_resources_upgrade(planet, page, notifier)
        else:
            resource_upgrade_durations = []

        # Check and upgrade energy buildings for the planet
        if config.get("enable_energy_upgrades", True):
            energy_upgrade_durations = handle_energy_buildings_upgrade(planet, page, notifier)
        else:
            energy_upgrade_durations = []

        # Check and upgrade research technologies for the planet
        if config.get("enable_research_upgrades", True):
            research_upgrade_durations = handle_research_upgrades(planet, page, notifier)
        else:
            research_upgrade_durations = []

        # Check and upgrade lifeform buildings for the planet
        if config.get("enable_lifeform_upgrades", True):
            lifeform_upgrade_durations = handle_lifeform_buildings_upgrade(planet, page, notifier)
        else:
            lifeform_upgrade_durations = []

        # Check and upgrade storages for the planet
        if config.get("enable_storage_upgrades", True):
            storage_upgrade_durations = upgrade_full_storages(planet, page, notifier)
        else:
            storage_upgrade_durations = []

        # Combine durations for this planet and append to total_durations
        planet_durations = resource_upgrade_durations + storage_upgrade_durations + lifeform_upgrade_durations + energy_upgrade_durations + research_upgrade_durations + facility_upgrade_durations
        total_durations.extend(planet_durations)

    all_durations: List[int] = [duration for duration in total_durations if duration > 0]

    return min(all_durations) if all_durations else 0

