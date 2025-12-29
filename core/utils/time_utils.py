import re
import isodate # type: ignore
from datetime import timedelta

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

# Note: Consider installing the `isodate` library stub for type checking.