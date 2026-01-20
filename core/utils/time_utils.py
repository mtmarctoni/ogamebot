import re
import isodate # type: ignore
from datetime import timedelta

from constants.general import COMPONENTS

def extract_minutes_from_text(duration_text: str) -> int:
    """
    Extract minutes from a duration text (e.g., '5m 30s' or '300s').
    Adds 1 to ensure completion.
    """
    match = re.search(r'(\d+)m\s*(\d+)s', duration_text)
    if match:
        minutes, seconds = map(int, match.groups())
        return (minutes * 60 + seconds) // 60 + 1

    match_seconds = re.search(r'(\d+)s', duration_text)
    if match_seconds:
        return int(match_seconds.group(1)) // 60 + 1

    return 1  # Default to 1 minute if no valid duration is found

def parse_duration(duration_attr: str, duration_text: str) -> int:
    """
    Parse the duration from either an ISO 8601 duration attribute or a text-based duration.
    Returns the duration in minutes, adding 1 to ensure completion.
    """
    # Try parsing ISO 8601 duration
    if duration_attr:
        try:
            duration: timedelta = isodate.parse_duration(duration_attr)  # type: ignore
            if isinstance(duration, timedelta):
                return int(duration.total_seconds() // 60 + 1)
        except Exception as e:
            print(f"[ERROR] Failed to parse ISO 8601 duration: {e}")

    # Fallback: Parse text-based duration
    return extract_minutes_from_text(duration_text)


def get_countdown_selector(section: COMPONENTS) -> str:
    """
    Get the appropriate countdown selector based on the section.

    This function determines the correct CSS selector for the countdown timer
    element based on the provided section. Different sections of the game
    (e.g., resources, lifeform buildings, research) use different countdown timer IDs.

    Args:
        section (COMPONENTS): The section to determine the selector for.

    Returns:
        str: The CSS selector for the countdown element.

    Raises:
        ValueError: If no selector is defined for the given section.
    """
    if section == COMPONENTS.SUPPLIES or section == COMPONENTS.FACILITIES:
        return 'time#countdownbuildingDetails'
    elif section == COMPONENTS.LFBUILDINGS:
        return 'time#countdownlfbuildingDetails'
    elif section == COMPONENTS.RESEARCH:
        return 'time#countdownresearchDetails'
    else:
        return 'time'  # Default selector as a last resort
    
def wait_minutes(minutes: int) -> int:
    """
    Converts minutes to seconds for waiting purposes.

    Args:
        minutes (int): The number of minutes to wait.
    Returns:
        int: The equivalent number of seconds.
    """
    return minutes * 60