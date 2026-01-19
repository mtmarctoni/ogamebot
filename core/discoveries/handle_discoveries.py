from typing import Optional
from random import choice
from playwright.sync_api import Page

from config.types import DiscoveriesConfig, EmpireSnapshotDict, PlanetId
from constants.general import COMPONENTS
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify

def handle_discoveries(page: Page, empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier], config: Optional[DiscoveriesConfig]) -> None:
    """
    Handles discoveries by navigating to the Galaxy page for a random planet and clicking the discovery button.

    Args:
        empire_data (dict): Data containing information about all planets.
        page (Page): Current Playwright game page instance.
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

    # Get the planet from planet_id
    target_planet = next((planet for planet in planets if str(planet.get("id")) == planet_id), None)
    if not target_planet or "coords" not in target_planet:
        print(f"[ERROR] Target planet with ID {planet_id} not found or missing coordinates.")
        return
    
    # Get the coordinates
    coords = target_planet["coords"]
    try:
        galaxy_str, system_str, _ = coords.split(":")
        galaxy = int(galaxy_str.strip())
        system = int(system_str.strip())
    except Exception as e:
        print(f"[ERROR] Failed to parse coords '{coords}': {e}")
        return

    # Get random system numbers within a range where system is the center
    min_system = max(1, system - 10)
    max_system = min(499, system + 10)
    system_range = range(min_system, max_system + 1)
    random_system = choice(list(system_range))

    # Navigate to the Galaxy page for the selected planet
    try:
        print("[INFO] Navigating to Galaxy page...")
        navigate_to_section(page, planet_id, COMPONENTS.GALAXY)
    except Exception as e:
        print(f"[ERROR] Failed to navigate to Galaxy page: {e}")
        return

    # Interact with Galaxy and System inputs and the Discovery button
    try:
        print("[INFO] Waiting for galaxyHeader elements...")
        page.wait_for_selector('#galaxyHeader', state="visible", timeout=15000)

        galaxy_input = page.locator("input#galaxy_input")
        system_input = page.locator("input#system_input")

        galaxy_input.type(str(galaxy))  # Focus is implicit
        system_input.type(str(random_system))  # Focus is implicit

        # Wait 1 second after typing the position
        page.wait_for_timeout(1500)

        # Click the Discovery button
        mission_button = page.locator("#discoverSystemBtn")
        mission_button.click()
        page.wait_for_timeout(1000)

        # Verify that the discovery was successfully started
        try:
            print("[INFO] Verifying discovery initiation...")
            event_box = page.wait_for_selector("#eventboxFilled", state="visible", timeout=15000)
            spans = event_box.query_selector_all("span") if event_box else []

            searchText = "Search for lifeforms"
            discoverLunched = False
            for span in spans:  # Use available span handles, iterate directly
                inner_text = span.inner_text()
                if searchText in inner_text:
                    discoverLunched = True
                    break

            if discoverLunched:
                print("[SUCCESS] Discovery mission successfully initiated!")
                safe_notify(notifier, "🚀 Discovery mission successfully initiated!")
            else:
                print("[ERROR] Discovery mission might not have started as expected.")
        except Exception as e:
            print(f"[ERROR] Failed to verify discovery initiation: {e}")


    except Exception as e:
        print(f"[ERROR] Discovery action failed: {e}")