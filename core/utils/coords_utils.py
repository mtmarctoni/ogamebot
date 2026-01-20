from random import choices

from config.config import MAX_SYSTEM_NUMBER
from config.types import Coordinates, PlanetDict

def generate_target_coordinates_for_expedition(galaxy: int, system: int) -> Coordinates:
    """
    Generates a list of target coordinates for expeditions based on the planet's location.

    Args:
        galaxy (int): The galaxy of the dispatching planet.
        system (int): The system of the dispatching planet.
        max_system (int): Maximum system number in the universe (defaults to MAX_SYSTEM_NUMBER).

    Returns:
        List[List[int]]: A list of [galaxy, system, slot] coordinates for expeditions.
    """
    slot = 16  # Expeditions always use slot 16
    # Systems ±3 from the current system, constrained within bounds
    valid_systems = [max(1, min(system + delta, MAX_SYSTEM_NUMBER)) for delta in range(-3, 4)]

    target_coordinates_list = [[galaxy, s, slot] for s in valid_systems]

    # get random target with more weight the same system
    weights = [3 if s == system else 1 for s in valid_systems]
    target_coordinates = choices(target_coordinates_list, weights=weights, k=1)[0]

    return target_coordinates

def get_coords_from_planet(planet: PlanetDict) -> Coordinates:
    """
    Extracts the coordinates from a planet dictionary.

    Args:
        planet (PlanetDict): The planet data containing coordinates.
    Returns:
        Coordinates: The coordinates as a list of integers [galaxy, system, slot].
    Raises:
        KeyError: If "coords" is missing from the planet dictionary.
        ValueError: If "coords" is not in the expected format.
    """
    coords_str = planet.get("coords")
    if coords_str is None:
        raise KeyError('Planet dictionary is missing "coords" key.')
    coords_str = coords_str.strip('[]')
    return [int(part) for part in coords_str.split(':')]