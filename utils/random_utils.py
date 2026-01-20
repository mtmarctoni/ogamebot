import random

from config.config import MAX_GALAXY_NUMBER, MAX_SYSTEM_NUMBER

def generate_random_number(min_value: int, max_value: int) -> int:
    """
    Generate a random number between min_value and max_value (inclusive).

    Args:
        min_value (int): The minimum value (inclusive).
        max_value (int): The maximum value (inclusive).

    Returns:
        int: A random integer between the specified range.
    """
    return random.randint(min_value, max_value)

def get_random_galaxy() -> int:
    """
    Generate a random galaxy number between 1 and 6.

    Returns:
        int: Random galaxy number (1-6).
    """
    return generate_random_number(1, MAX_SYSTEM_NUMBER)

def get_random_system() -> int:
    """
    Generate a random system number between 1 and 499.

    Returns:
        int: Random system number (1-499).
    """
    return generate_random_number(1, MAX_GALAXY_NUMBER)