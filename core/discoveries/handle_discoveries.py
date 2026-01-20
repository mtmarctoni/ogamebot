from typing import Optional
from utils.random_utils import get_random_galaxy, get_random_system
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
        # Get the first planet's ID as default
        valid_planets = [planet for planet in planets if "id" in planet]
        if not valid_planets:
            print("[ERROR] No planets with 'id' found for discoveries.")
            return
        planet_id = PlanetId(valid_planets[0]["id"])

    print(f"[INFO] Selected random planet ID: {planet_id}")

    # Get random system and galaxy
    random_galaxy = get_random_galaxy()
    random_system = get_random_system()

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

        galaxy_input.focus()
        galaxy_input.type(str(random_galaxy))

        system_input.focus()
        system_input.type(str(random_system))

        # Wait 1 second after typing the position
        page.wait_for_timeout(1500)

        # Click the Galaxy confirmation button within the header region
        try:
            galaxy_header = page.locator("#galaxyHeader .btn_blue", has_text="Go!")
            galaxy_header.click()
            page.wait_for_timeout(1000)  # Wait 1 second before the next action
        except Exception as e:
            print(f"[ERROR] Failed to click the Galaxy confirmation button: {e}")

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