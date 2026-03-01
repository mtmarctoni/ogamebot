from config.types import FleetToDispatch, PlanetDict, ShipToDispatch, TechId
from constants.ships import Ship, Ships, PROBES_PER_EXPEDITION, RESERVE_ON_PLANET_SHIPS, EXCLUDED_EXPEDITION_SHIPS


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
        ship_id = str(ship['ship_id'])
        ship_count = int(ship['count'])
        ship_type = Ships.get_name_by_id(ship_id)

        if ship_type in EXCLUDED_EXPEDITION_SHIPS:
            continue

        # Send only a couple of probes per expedition, keep the rest on the planet
        if ship_type == Ship.ESPIONAGE_PROBE:
            per_slot = min(PROBES_PER_EXPEDITION, ship_count // slots)
        # Leave reserve for cargos and pathfinders (transport/farming utility)
        elif ship_type in RESERVE_ON_PLANET_SHIPS:
            per_slot = ship_count // (slots + 1)
        # Combat ships: send all available across expedition slots
        else:
            per_slot = ship_count // slots

        if per_slot > 0:
            ships_per_expedition.append({
                'ship_id': ship['ship_id'],
                'count': per_slot
            })

    return ships_per_expedition

def get_available_ships(planet: PlanetDict) -> FleetToDispatch:
    """
    Returns a dictionary of all ships on the planet with their counts.
    """
    available_ships: FleetToDispatch = []
    if 'ships' in planet:
        ships = planet.get("ships", {})
        for ship_id, ship_info in ships.items():
            count = int(ship_info.get('level', 0))

            try:
                ship_type = Ships.get_name_by_id(str(ship_id))
            except ValueError:
                print(f"[WARN] Invalid ship ID {ship_id} encountered. Skipping.")
                continue  # Skip invalid ship IDs

            # Skip ships that should never be sent on expeditions
            if ship_type in EXCLUDED_EXPEDITION_SHIPS:
                continue

            ship_to_dispatch: ShipToDispatch = {
                'ship_id': TechId(ship_id),
                'count': count
            }
            if count > 0:
                available_ships.append(ship_to_dispatch)
    return available_ships