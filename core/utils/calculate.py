from constants.resources import ENERGY_CONSUMPTION


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