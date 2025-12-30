from typing import List, Optional
from playwright.sync_api import Page

from config.types import EmpireSnapshotDict
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.auto_storage import upgrade_full_storages
from core.upgrade.lifeform_buildings import handle_lifeform_uildings_upgrade
from core.upgrade.buildings import handle_resources_upgrades

def handle_upgrades(empire_data: EmpireSnapshotDict, game_page: Page, notifier: Optional[TelegramNotifier]) -> int:
    """
    Handles upgrades for all planets in the empire data.

    Args:
        empire_data (dict): Data containing information about all planets.
        game_page: Playwright page object for interacting with the game.
        notifier: TelegramNotifier instance for sending notifications.
    """
    # Initialize total_durations to ensure it is always defined
    total_durations: List[int] = []

    # Iterate through all planets and handle upgrades for each
    for planet in empire_data["planets"]:
        planet_name = planet.get('name', 'Unknown')
        planet_id = planet.get('id', 'Unknown')
        print(f"\nProcessing upgrades for planet: {planet_name} (ID: {planet_id})")

        # Check and upgrade resources (metal, crystal, deuterium) for the planet
        resource_upgrade_durations = handle_resources_upgrades(planet, game_page, notifier)

        # Check and upgrade storages for the planet
        storage_upgrade_durations = upgrade_full_storages(planet, game_page, notifier)

        # Check and upgrade lifeform buildings for the planet
        lifeform_upgrade_durations = handle_lifeform_uildings_upgrade(planet, game_page, notifier)

        # Combine durations for this planet and append to total_durations
        planet_durations = resource_upgrade_durations + storage_upgrade_durations + lifeform_upgrade_durations
        total_durations.extend(planet_durations)

    all_durations: List[int] = [duration for duration in total_durations if duration > 0]

    return min(all_durations) if all_durations else 0

