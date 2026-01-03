import time
import re
from typing import List, Optional
from playwright.sync_api import Page

from config.config import PLANET_IDS
from config.types import EmpireSnapshotDict, FleetToDispatch, PlanetDict, PlanetId, ShipToDispatch, TechId
from constants.general import COMPONENTS
from constants.ships import Ships
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify

# Target coordinates for expeditions
TARGET_COORDINATES = [2, 8, 16]

def get_target_planet(empire_data: EmpireSnapshotDict) -> Optional[PlanetDict]:
    """
    Retrieves the planet object for 'Abyssal Nexus'.
    """
    planet_id = PlanetId(PLANET_IDS["default"])
    for planet in empire_data.get("planets", []):
        if planet.get("id") == planet_id:
            return planet
    return None

def get_available_ships(planet: PlanetDict) -> FleetToDispatch:
    """
    Returns a dictionary of all ships on the planet with their counts.
    """
    available_ships: FleetToDispatch = []
    if 'ships' in planet:
        ships = planet.get("ships", {})
        for ship_id, ship_info in ships.items():
            count = int(ship_info.get('level', 0))
            ship_to_dispatch: ShipToDispatch = {
                'ship_id': TechId(ship_id),
                'count': count
            }
            if count > 0:
                available_ships.append(ship_to_dispatch)
    return available_ships

def calculate_ships_per_expedition(total_ships: FleetToDispatch, slots: int) -> FleetToDispatch:
    """
    Divides available ships by the number of slots.
    Returns a list of ships to dispatch per expedition.
    Handles decimals by taking the lesser integer value.
    """
    if slots == 0:
        return []

    ships_per_expedition: FleetToDispatch = []
    for ship in total_ships:
        per_slot = ship['count'] // slots  # Integer division ensures we take the lesser value
        if per_slot > 0:
            ships_per_expedition.append({
                'ship_id': ship['ship_id'],
                'count': per_slot
            })

    return ships_per_expedition

def dispatch_expedition(page: Page, ships: FleetToDispatch, coordinates: List[int]) -> Optional[int]:
    """
    Dispatches a single expedition.
    Returns the return time in seconds if successful, None otherwise.
    """
    try:
        # 1. Select Ships
        # We assume we are already on the fleet dispatch page (Fleet 1)
        print(f"Selecting ships: {ships}")
        has_ships = False
        for ship in ships:
            ship_id = ship['ship_id']
            count = ship['count']
            # Use the mapping from constants/ships.py
            ship_name = Ships.get_name_by_id(str(ship_id)).value
            ship_input = page.locator(f"input[name='{ship_name}']")
            if ship_input.is_visible():
                ship_input.fill(str(count))
                has_ships = True
            else:
                # If input is not visible, maybe we don't have that ship or it's hidden
                pass

        if not has_ships:
            print("No ships selected.")
            return None

        # Click Continue to Fleet 2
        page.locator("#continueToFleet2").click()
        page.wait_for_selector("#fleet2", state="visible")

        # 2. Set Coordinates
        galaxy, system, position = coordinates
        page.locator("input#galaxy").fill(str(galaxy))
        page.locator("input#system").fill(str(system))
        page.locator("input#position").fill(str(position))

        # 3. Select Mission (Expedition = 15)
        mission_button = page.locator("#missionButton15")
        if not mission_button.is_visible():
            print("Expedition mission not available.")
            return None

        mission_button.click()

        # Validate Mission Selection
        if not mission_button.is_checked():
            mission_button.check()

        # 4. Send Fleet
        send_button = page.locator("#sendFleet")
        send_button.click()

        # 5. Get Return Time
        page.wait_for_selector("form#shipsChosen", timeout=10000)  # Wait for the main fleet dispatch page
        print("Expedition dispatched successfully.")

    except Exception as e:
        print(f"Error dispatching expedition: {e}")
        return None

def handle_expeditions(page: Page, empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier]) -> Optional[int]:
    """
    Main handler for expeditions.
    Returns the time to wait until next check (in seconds).
    """
    print("Handling expeditions...")
    
    # 1. Get Target Planet
    planet = get_target_planet(empire_data)
    if not planet:
        print(f"Planet not found.")
        return 0

    planet_id = PlanetId(str(planet.get("id")))

    # 2. Switch to Target Planet and Go to Fleet Dispatch
    try:
        navigate_to_section(page, planet_id, COMPONENTS.FLEET_DISPATCH)
    except Exception as e:
        print(f"Failed to navigate to fleet dispatch: {e}")
        return 600

    # 3. Check Available Slots
    available_slots = 0
    try:
        # Wait for slots info to be visible
        page.wait_for_selector("#slots", timeout=5000)
        
        # Get all text from the slots container
        slots_text = page.locator("#slots").inner_text()
        # Clean up newlines for easier regex
        slots_text_clean = slots_text.replace("\n", " ").replace("\r", "")
        
        # Parse Expeditions: "Expeditions: 0/4"
        exp_match = re.search(r"Expeditions:\s*(\d+)/(\d+)", slots_text_clean)
        # Parse Fleets: "Fleets:0/11"
        fleet_match = re.search(r"Fleets:\s*(\d+)/(\d+)", slots_text_clean)

        if exp_match and fleet_match:
            current_exp = int(exp_match.group(1))
            max_exp = int(exp_match.group(2))
            
            current_fleets = int(fleet_match.group(1))
            max_fleets = int(fleet_match.group(2))
            
            avail_exp = max_exp - current_exp
            avail_fleets = max_fleets - current_fleets
            
            # We are limited by whichever is smaller
            available_slots = min(avail_exp, avail_fleets)
            print(f"Slots Status - Expeditions: {current_exp}/{max_exp}, Fleets: {current_fleets}/{max_fleets}")
        else:
            print(f"Could not parse slots from text: '{slots_text_clean}'")
            
    except Exception as e:
        print(f"Error checking slots: {e}")
        
    print(f"Available expedition slots: {available_slots}")
    
    if available_slots <= 0:
        print("No expedition slots available.")
        return 600 # Wait 10 mins
        
    # 4. Get Available Ships
    available_ships = get_available_ships(planet)
    
    # 5. Calculate Ships per Expedition
    ships_to_send = calculate_ships_per_expedition(available_ships, available_slots)
    
    if not ships_to_send:
        print("No ships available for expedition.")

    # 6. Dispatch Expeditions
    for i in range(available_slots):
        print(f"Dispatching expedition {i+1}/{available_slots}...")
        
        # If this is not the first iteration, we need to navigate back to fleet dispatch
        if i > 0:
            try:
                navigate_to_section(page, planet_id, COMPONENTS.FLEET_DISPATCH)
            except Exception as e:
                print(f"Failed to navigate to fleet dispatch for subsequent expedition: {e}")
                break

        return_time = dispatch_expedition(page, ships_to_send, TARGET_COORDINATES)
        
        if return_time:
            safe_notify(notifier, f"Expedition dispatched to {TARGET_COORDINATES}. Ships: {ships_to_send}")
            # Wait a bit between dispatches
            time.sleep(5)
        else:
            print("Failed to dispatch expedition.")
            