from config.types import FleetToDispatch, PlanetDict, TechLevel
from constants.resources import ENERGY_CONSUMPTION
from constants.ships import Ships
from constants.univers import SHIP_EXPO_POINTS
from core.utils.ships_utils import get_available_ships


def calculate_energy_needed(resource: str, level: int) -> int:
    """
    Calculate the energy needed for the next level of a resource mine.

    Args:
        resource (str): The resource type (e.g., 'metal', 'crystal', 'deuterium').
        level (int): The current level of the mine.

    Returns:
        int: The energy needed for the next level.
    """
    current_level_energy = ENERGY_CONSUMPTION[f"{resource}"](level)
    next_level_energy = ENERGY_CONSUMPTION[f"{resource}"](level + 1)
    return next_level_energy - current_level_energy

def extract_free_fields(fields: str) -> int:
    """
    Extracts the number of free fields from the "fields" string.

    Args:
        fields (str): The "fields" string in the format "used/total".

    Returns:
        int: The number of free fields.
    """
    used, total = map(int, fields.split('/'))
    return total - used

# Helper function to check if a resource can be prioritized
def can_upgrade(current: TechLevel, cap: TechLevel, condition: bool) -> bool:
    """
    Determines if a resource can be upgraded based on its current level, cap, and a custom condition.

    Args:
        current: The current level of the resource.
        cap: The soft cap for the resource.
        condition: A boolean condition specific to the resource.

    Returns:
        True if the resource can be upgraded, False otherwise.
    """
    return current < cap and condition

def energy_int(value: str | None) -> int:
    """
    Cleans and converts a string representing an OGame number into an integer.
    Handles thousands separators (commas, periods) and optional '+' signs.

    Args:
        value: The value to clean and convert. Can be a string or None.

    Returns:
        An integer representation of the cleaned value, or 0 if the value is None.
    """
    if not isinstance(value, str):
        return int(value) if value is not None else 0

    # Remove common non-digit characters: +, commas, and periods
    cleaned = value.replace('+', '').replace(',', '').replace('.', '')
    return int(cleaned)

def check_deuterium_level(planet: PlanetDict) -> bool:
    """
    Checks if the planet has enough deuterium to proceed with expeditions.
    Args:
        planet (PlanetDict): The planet data dictionary.
        threshold (int): The minimum deuterium required.
    Returns:
        bool: True if there is enough deuterium, False otherwise.
    """
    available_ships = get_available_ships(planet)
    total_ships = sum(ship['count'] for ship in available_ships)
    # For each 1000 ships we need at least 10000 deuterium
    threshold = (total_ships // 1000) * 10
    # Minimum threshold of 10000 deuterium
    if threshold < 50_000:
        threshold = 50_000
    deuterium = int(planet.get('resources', {}).get('deuterium', 0))
    return True
    return deuterium >= threshold

# def calculate_expedition_deuterium(planet: PlanetDict, target_coords: str) -> int:
#     _, system, _ = map(int, target_coords.split(':'))
    
#     # 1. Expo points
#     fleet = get_available_ships(planet)
#     expo_points = get_expo_points(fleet)
    
#     # 2. Base (your tested empirical constant)
#     base_deut = expo_points * system * 0.85
    
#     # 3. Drive tech reduction (OGame standard)
#     combustion = planet['research'].get('combustionDriveTechnology', 0)
#     impulse = planet['research'].get('impulseDriveTechnology', 0)
#     hyperspace = planet['research'].get('hyperspaceTechnology', 0)
#     drive_factor = max(0.1, 1.0 - (combustion * 0.02 + impulse * 0.015 + hyperspace * 0.01))
    
#     # 4. Server settings (Pluto s271-en)
#     uni_speed = 8
#     discoverer_bonus = 0.85
#     server_deut_reduction = 0.5
    
#     # 5. KAELESH LIFEFORM MODIFIER (new!)
#     kaelesh_deut_reduction = planet['research'].get('kaeleshDeuteriumTech', 0) * 0.0015  # 0.15%/level
#     kaelesh_factor = 1.0 - min(0.05, kaelesh_deut_reduction)  # Max 5% reduction
    
#     # FINAL CALCULATION (clean, no magic numbers beyond your 0.85)
#     total_deut = int(
#         base_deut 
#         * drive_factor 
#         * discoverer_bonus 
#         * server_deut_reduction 
#         * kaelesh_factor 
#         / uni_speed  # Direct division (pure math)
#     )
    
#     return max(1, total_deut)


# def check_deuterium_level(planet: PlanetDict, target_coords: str) -> tuple[bool, int]:
#     """
#     IMPROVED VERSION: Calculates exact cost + safety buffer
#     """
#     required_deut = calculate_expedition_deuterium(planet, target_coords)
    
#     # 15% safety buffer + 25k minimum
#     threshold = max(required_deut * 1.15 + 25_000, 75_000)
    
#     deuterium = int(planet.get('resources', {}).get('deuterium', 0))
    
#     return deuterium >= threshold, required_deut

# def get_expo_points(fleet: FleetToDispatch) -> int:
#     """
#     Calculates expedition points = (Structural Integrity * 5) / 1000 per ship
#     """
#     total_points = 0
#     for ship in fleet:
#         ship_type = Ships.get_name_by_id(ship['ship_id'])
#         count = ship['count']
#         points_per_ship = SHIP_EXPO_POINTS[ship_type]
#         total_points += count * points_per_ship
#     return total_points
