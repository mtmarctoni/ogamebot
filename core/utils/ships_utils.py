from config.types import FleetToDispatch, PlanetDict, ShipToDispatch, TechId
from constants.ships import Ships, unwanted_ships_for_expeditions


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
        per_slot = ship['count'] // (slots + 1)  # Divide by slots + 1 to leave some ships on the planet
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

            ship_name = Ships.get_name_by_id(str(ship_id)).value

            # Skip unwanted ships for expeditions
            if ship_name in unwanted_ships_for_expeditions:
                continue

            ship_to_dispatch: ShipToDispatch = {
                'ship_id': TechId(ship_id),
                'count': count
            }
            if count > 0:
                available_ships.append(ship_to_dispatch)
    return available_ships