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