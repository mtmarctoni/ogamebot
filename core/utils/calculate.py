from config.types import PlanetDict, TechLevel
from constants.resources import ENERGY_CONSUMPTION
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
    threshold = (total_ships // 1000) * 10_000
    
    # Minimum threshold of 10000 deuterium
    if threshold < 50_000:
        threshold = 50_000

    deuterium = int(planet.get('resources', {}).get('deuterium', 0))

    return deuterium >= threshold
