import time
from typing import List, Optional
from playwright.sync_api import Page

from config.config import DEFAULT_EXPEDITION_PLANET_ID, DEFAULT_EXPEDITION_SPEED
from config.types import EmpireSnapshotDict, ExpeditionConfig, FleetToDispatch, PlanetId
from constants.general import COMPONENTS
from constants.ships import Ships
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.utils.calculate import check_deuterium_level
from core.utils.coords_utils import generate_target_coordinates_for_expedition, get_coords_from_planet
from core.utils.empire_utils import get_target_planet
from core.utils.fleet_slots import get_fleet_slots_info
from core.utils.ships_utils import calculate_ships_per_expedition, get_available_ships
from core.utils.time_utils import wait_minutes

def dispatch_expedition(page: Page, ships: FleetToDispatch, coordinates: List[int]) -> Optional[int]:
    """
    Dispatches a single expedition.
    Returns the return time in seconds if successful, None otherwise.
    """
    try:
        # 1. Select Ships
        # We assume we are already on the fleet dispatch page (Fleet 1)
        print(f"[INFO] Preparing ships for expedition: {ships}")
        has_ships = False
        for ship in ships:
            ship_id = ship['ship_id']
            count = ship['count']
            # Use the mapping from constants/ships.py
            ship_name = Ships.get_name_by_id(str(ship_id)).value

            ship_input = page.locator(f"input[name='{ship_name}']")
            if ship_input.is_visible():
                ship_input.focus()  # Focus the input field before filling
                ship_input.fill(str(count))
                has_ships = True
            else:
                # If input is not visible, maybe we don't have that ship or it's hidden
                pass

        if not has_ships:
            print("[WARN] Could not select any ships for expedition.")
            return None

        page.wait_for_timeout(1000)  # Small wait to ensure inputs are registered
        # Press Enter after filling the ship inputs instead of clicking the button
        page.keyboard.press("Enter")
        page.wait_for_selector("#fleet2", state="visible")
        page.wait_for_timeout(1000)  # Small wait to ensure inputs are registered


        # 2. Set Coordinates
        galaxy, system, position = coordinates
        print(f"[INFO] Filling coordinates for expedition: Galaxy={galaxy}, System={system}, Position={position}")

        galaxy_input = page.locator("input#galaxy")
        system_input = page.locator("input#system")
        position_input = page.locator("input#position")

        galaxy_input.focus()
        galaxy_input.type(str(galaxy))

        system_input.focus()
        system_input.type(str(system))

        position_input.focus()
        position_input.type(str(position))  # Use .type() to emulate typing the number

        # Wait 1 second after typing the position
        page.wait_for_timeout(1500)

        # Click the mission button
        mission_button = page.locator("#missionButton15")
        mission_button.click()
        page.wait_for_timeout(1000)

        # 3. Set Speed
        print(f"[INFO] Setting expedition speed to {DEFAULT_EXPEDITION_SPEED}%...")
        try:
            # Calculate the data-step attribute based on speed percentage
            # Speed steps: 10%=1, 20%=2, 30%=3, ..., 100%=10
            speed_step = DEFAULT_EXPEDITION_SPEED // 10
            
            # Locate the speed percentage div for the configured speed
            speed_selector = page.locator(f'#speedPercentage div[data-step="{speed_step}"]:has-text("{DEFAULT_EXPEDITION_SPEED}")')
            if speed_selector.is_visible():
                speed_selector.click()
                print(f"[INFO] Speed set to {DEFAULT_EXPEDITION_SPEED}%")
                page.wait_for_timeout(500)
            else:
                print(f"[WARN] Could not find speed selector with {DEFAULT_EXPEDITION_SPEED}%. Proceeding with default speed.")
        except Exception as e:
            print(f"[WARN] Failed to set speed to {DEFAULT_EXPEDITION_SPEED}%: {e}. Proceeding with default speed.")

        # 4. Click the send fleet button
        send_button = page.locator("#sendFleet")
        send_button.click()

        # 5. Get Return Time
        page.wait_for_selector("form#shipsChosen", timeout=10000)  # Wait for the main fleet dispatch page
        print("[INFO] Expedition dispatched successfully.")

    except Exception as e:
        print(f"[ERROR] Expedition dispatch failed: {e}")
        return None

def handle_expeditions(page: Page, empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier], config: Optional[ExpeditionConfig]) -> Optional[int]:
    """
    Main handler for expeditions.
    Returns the time to wait until next check (in seconds).
    """
    print("[INFO] Handling expeditions batch...")

    # 1. Get Target Planet
    if config and config["target_id"]:
        target_id = config["target_id"]
        planet_id = PlanetId(target_id)
    else:
        print("[INFO] No target planet IDs in config. Using default Moon.")
        planet_id = PlanetId(DEFAULT_EXPEDITION_PLANET_ID)

    planet = get_target_planet(empire_data, planet_id)
    if not planet:
        print(f"[ERROR] Target planet not found for expedition. Requested ID: {planet_id}")
        return 0

    planet_id = PlanetId(str(planet['id']))

    # Check Deuterium Level
    has_enough_deut, required_deut = check_deuterium_level(planet)
    if not has_enough_deut:
        current_deut = int(planet['resources']['deuterium'])
        print(f"[WARN] Not enough deuterium on planet {planet['name']} for expeditions. Have: {current_deut:,}, Need: ~{required_deut:,}")
        safe_notify(notifier, f"⚠️ Not enough deuterium on planet {planet['name']} for expeditions. Have: {current_deut:,}, Need: ~{required_deut:,}. Skipping expedition dispatch.")
        return wait_minutes(10)

    # 2. Switch to Target Planet and Go to Fleet Dispatch
    try:
        navigate_to_section(page, planet_id, COMPONENTS.FLEET_DISPATCH)
    except Exception as e:
        print(f"[ERROR] Expedition fleet dispatch navigation failed: {e}")
        return wait_minutes(10)

    # Check if there are ships available
    # in the div element with id="warning" it has to be some inner text saying: "There are no ships available"
    try:
        warning_locator = page.locator("#warning")
        if warning_locator.is_visible():
            warning_text = warning_locator.inner_text()
            if "There are no ships on this planet." in warning_text:
                print("[INFO] No ships available for expeditions.")
                return wait_minutes(10)
    except Exception as e:
        print(f"[ERROR] Checking for available ships failed: {e}")

    # 3. Check Available Slots
    available_slots = 0
    try:
        slots_info = get_fleet_slots_info(page)
        if slots_info:
            available_slots = slots_info["available_joint"]
            print(
                f"[INFO] Available slots - Expeditions: "
                f"{slots_info['current_expeditions']}/{slots_info['max_expeditions']}, "
                f"Fleets: {slots_info['current_fleets']}/{slots_info['max_fleets']}"
            )
        else:
            print("[WARN] Could not parse slots info from #slots container.")

    except Exception as e:
        print(f"[ERROR] Checking slots failed: {e}")

    print(f"[INFO] Expedition slots available: {available_slots}")

    if available_slots <= 0:
        print("[INFO] No expedition slots available.")
        return wait_minutes(10)

    # 4. Get Available Ships
    available_ships = get_available_ships(planet)

    # 5. Calculate Ships per Expedition
    ships_to_send = calculate_ships_per_expedition(available_ships, available_slots)

    if not ships_to_send:
        print("[WARN] No ships available for expedition.")
        return wait_minutes(10)

    # 6. Dispatch Expeditions
    for i in range(available_slots):
        print(f"[INFO] Dispatching expedition {i+1}/{available_slots}...")

        # If this is not the first iteration, we need to navigate back to fleet dispatch
        if i > 0:
            try:
                navigate_to_section(page, planet_id, COMPONENTS.FLEET_DISPATCH)
            except Exception as e:
                print(f"[ERROR] Failed to navigate to fleet dispatch for subsequent expedition: {e}")
                break

        # Fetch dynamic target coordinates based on the dispatching planet's system
        galaxy, system, _ = get_coords_from_planet(planet)
        target_coordinates = generate_target_coordinates_for_expedition(galaxy, system)

        return_time = dispatch_expedition(page, ships_to_send, target_coordinates)

        if return_time:
            safe_notify(notifier, f"Expedition dispatched to {target_coordinates}. Ships: {ships_to_send}")
            # Wait a bit between dispatches
            time.sleep(5)
        else:
            print("[ERROR] Expedition dispatch failed.")