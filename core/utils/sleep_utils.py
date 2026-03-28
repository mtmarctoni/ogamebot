import time
import random
import datetime
from typing import Optional
from config.config import NIGHT_MIN_SLEEP, NIGHT_MAX_SLEEP, DAY_MIN_SLEEP, DAY_MAX_SLEEP, DEFAULT_MIN_SLEEP, DEFAULT_MAX_SLEEP
from core.notifications.telegram_notifier import TelegramNotifier

def get_default_sleep_times() -> tuple[int, int]:
    """
    Determine the default minimum and maximum sleep times based on the current time of day.

    Returns:
        tuple[int, int]: A tuple containing the default minimum and maximum sleep times in minutes.
    """
    now = datetime.datetime.now()
    current_hour = now.hour

    if current_hour >= 2 and current_hour < 8:
        return NIGHT_MIN_SLEEP, NIGHT_MAX_SLEEP
    elif current_hour >= 8 and current_hour < 20:
        return DAY_MIN_SLEEP, DAY_MAX_SLEEP
    else:
        return DEFAULT_MIN_SLEEP, DEFAULT_MAX_SLEEP

def format_duration(seconds: int) -> str:
    minutes, remaining_seconds = divmod(max(0, seconds), 60)
    if minutes and remaining_seconds:
        return f"{minutes}m {remaining_seconds}s"
    if minutes:
        return f"{minutes}m"
    return f"{remaining_seconds}s"


def sleep_random_interval(min_seconds: int = 0, max_seconds: int = 0) -> None:
    """
    Sleep for a random interval in seconds.
    If explicit bounds are not provided, fall back to the time-of-day defaults.
    """
    if min_seconds > 0 and max_seconds > 0:
        sleep_min_seconds = min_seconds
        sleep_max_seconds = max_seconds
    else:
        default_min_minutes, default_max_minutes = get_default_sleep_times()
        sleep_min_seconds = default_min_minutes * 60
        sleep_max_seconds = default_max_minutes * 60

    if sleep_min_seconds > sleep_max_seconds:
        sleep_min_seconds, sleep_max_seconds = sleep_max_seconds, sleep_min_seconds

    duration_seconds = random.randint(sleep_min_seconds, sleep_max_seconds)
    print(f"\nSleeping for {format_duration(duration_seconds)} before next check... (Ctrl+C to stop)")
    time.sleep(duration_seconds)

def sleep_for_minimum_duration(duration_seconds: int, notifier: Optional[TelegramNotifier], max_check_minutes: Optional[int]) -> None:
    """
    Sleep for the given duration in seconds, capped by the configured heartbeat.
    Falls back to a random interval if duration is 0.

    Args:
        duration_seconds (int): The duration to sleep in seconds.
        notifier (Optional[TelegramNotifier]): The notifier instance for sending notifications.
    """
    if max_check_minutes is not None and max_check_minutes > 0:
        max_sleep_seconds = max_check_minutes * 60
    else:
        max_sleep_seconds = get_default_sleep_times()[1] * 60

    if duration_seconds > max_sleep_seconds:
        print(
            f"[DEBUG] Provided duration ({format_duration(duration_seconds)}) exceeds maximum "
            f"({format_duration(max_sleep_seconds)}). Using maximum."
        )
        duration_seconds = max_sleep_seconds

    if duration_seconds > 0:
        print(f"[DEBUG] Sleeping for duration: {format_duration(duration_seconds)}.")
        sleep_random_interval(duration_seconds, duration_seconds + 5)
        if notifier:
            notifier.send_message(f"Sleeping for {format_duration(duration_seconds)} before next check.")
    else:
        print("[DEBUG] No valid durations found. Sleeping for a random interval.")
        sleep_random_interval()
        if notifier:
            notifier.send_message("Sleeping randomly before next check.")
