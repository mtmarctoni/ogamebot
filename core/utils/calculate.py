from config.types import FleetToDispatch, PlanetDict, TechLevel
from constants.resources import ENERGY_CONSUMPTION
from constants.ships import Ships
from constants.univers import BASE_DISTANCE_PENALTY, DISCOVERER_FUEL_DISCOUNT, DISTANCE_DIVISOR, FURTHER_SYSTEM_DISTANCE_FOR_EXPEDITION, INTRA_SYSTEM_DISTANCE, IS_DISCVERER_CLASS, PLUTO_CONSUMPTION_RATE, PLUTO_PEACEFUL_SPEED_MULT, SPEED_SQUARE_COEFFICIENT
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

# def check_deuterium_level(planet: PlanetDict) -> bool:
#     """
#     Checks if the planet has enough deuterium to proceed with expeditions.
#     Args:
#         planet (PlanetDict): The planet data dictionary.
#         threshold (int): The minimum deuterium required.
#     Returns:
#         bool: True if there is enough deuterium, False otherwise.
#     """
#     available_ships = get_available_ships(planet)
#     total_ships = sum(ship['count'] for ship in available_ships)
#     # For each 1000 ships we need at least 10000 deuterium
#     threshold = (total_ships // 1000) * 10
#     # Minimum threshold of 10000 deuterium
#     if threshold < 50_000:
#         threshold = 50_000
#     deuterium = int(planet.get('resources', {}).get('deuterium', 0))
#     return True
#     return deuterium >= threshold

import math

def calculate_expedition_deuterium(planet: PlanetDict) -> int:

    distance = BASE_DISTANCE_PENALTY + (INTRA_SYSTEM_DISTANCE * FURTHER_SYSTEM_DISTANCE_FOR_EXPEDITION)

    # 1.5 Get Fleet Composition
    fleet = get_available_ships(planet)
    
    # 2. Base Consumption Logic
    total_fuel_sum = 0
    for ship in fleet:
        ship_id = ship['ship_id']
        count = ship['count']
        ship_base_cons = Ships.get_consumption_by_id(ship_id)
        # Ensure both ship_base_cons and count are numeric
        count = int(count)
        # OGame standard fuel formula: 1 + FLOOR(BaseCons * Count * (Dist / 35000) * (Speed + 1)^2)
        fuel_per_ship_type: int = 1 + math.floor(
            ship_base_cons * count * (distance / DISTANCE_DIVISOR) * SPEED_SQUARE_COEFFICIENT
        )
        total_fuel_sum += fuel_per_ship_type

    # 3. Apply Multipliers
    final_multiplier = PLUTO_CONSUMPTION_RATE * PLUTO_PEACEFUL_SPEED_MULT
    if IS_DISCVERER_CLASS:
        final_multiplier *= DISCOVERER_FUEL_DISCOUNT
        
    return int(max(1, total_fuel_sum * final_multiplier))

def check_deuterium_level(planet: PlanetDict) -> tuple[bool, int]:
    """
    IMPROVED VERSION: Calculates exact cost + safety buffer
    """
    required_deut = calculate_expedition_deuterium(planet)  
    # 15% safety buffer + 25k minimum
    threshold = max(required_deut * 1.15 + 25_000, 75_000)  
    deuterium = int(planet['resources']['deuterium'])  
    print(f"[DEBUG] check_deuterium_level: Available Deuterium={deuterium}, Required Deuterium with buffer={threshold}")
    print("Planer: ", planet)
    return deuterium >= threshold, required_deut

def get_expo_points(fleet: FleetToDispatch) -> int:
    """
    Calculates expedition points = (Structural Integrity * 5) / 1000 per ship
    """
    total_points = 0
    for ship in fleet:
        count = ship['count']
        points_per_ship = Ships.get_expedition_points_by_id(ship['ship_id'])
        total_points += count * points_per_ship
    return total_points
