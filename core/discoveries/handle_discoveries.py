from typing import Optional
from random import choice
from playwright.sync_api import Page

from config.types import DiscoveriesConfig, EmpireSnapshotDict, PlanetId
from core.navigation.planet import navigate_to_section
from constants.general import COMPONENTS
from core.notifications.telegram_notifier import TelegramNotifier

def handle_discoveries(game_page: Page, empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier], config: Optional[DiscoveriesConfig]) -> None:
    """
    Handles discoveries by navigating to the Galaxy page for a random planet and clicking the discovery button.

    Args:
        empire_data (dict): Data containing information about all planets.
        game_page (Page): Current Playwright game page instance.
        notifier (Optional): Notifier for logging or sending alerts.
    """
    print("[INFO] Starting handle_discoveries process...")

    # Get all available planets
    planets = empire_data.get('planets', [])
    if not planets:
        print("[ERROR] No planets available for discoveries.")
        return

    # Choose a random system from the target planet
    # random_planet = choice(planets)
    if config and "target_id" in config:
        planet_id = PlanetId(config["target_id"])
    else:
        # Find a random planet that has an "id" key
        valid_planets = [planet for planet in planets if "id" in planet]
        if not valid_planets:
            print("[ERROR] No planets with 'id' found for discoveries.")
            return
        planet_id = PlanetId(choice(valid_planets)["id"])

    print(f"[INFO] Selected random planet ID: {planet_id}")

    # Navigate to the Galaxy page for the selected planet
    try:
        print("[INFO] Navigating to Galaxy page...")
        navigate_to_section(game_page, planet_id, COMPONENTS.GALAXY)
    except Exception as e:
        print(f"[ERROR] Failed to navigate to Galaxy page: {e}")
        return

    # Interact with the Discovery button
    try:
        print("[INFO] Clicking discovery button...")
        game_page.click("button.discovery-btn")  # Replace selector with the actual one
        print("[INFO] Discovery action completed!")
    except Exception as e:
        print(f"[ERROR] Failed to interact with discovery button: {e}")