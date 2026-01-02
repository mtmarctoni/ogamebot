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

def sleep_random_interval(min_minutes: int = 0, max_minutes: int = 0) -> None:
    """
    Sleep for a random interval based on the time of day to mimic human behavior.
    If min_minutes and max_minutes are provided, use them instead of the default behavior.
    Enforces the default maximum sleep time for the current time of day.
    """
    # Determine default sleep times based on the time of day
    default_min, default_max = get_default_sleep_times()

    # If arguments are provided, enforce the default maximum
    if min_minutes > 0 and max_minutes > 0:
        min_minutes = max(min_minutes, default_min)  # Ensure at least the default minimum
        max_minutes = min(max_minutes, default_max)  # Cap at the default maximum
    else:
        min_minutes = default_min
        max_minutes = default_max

    if min_minutes > max_minutes:
        min_minutes, max_minutes = max_minutes, min_minutes  # Swap to ensure valid range

    minutes = random.randint(min_minutes, max_minutes)
    print(f"\nSleeping for {minutes} minutes before next check... (Ctrl+C to stop)")
    time.sleep(minutes * 60)

def sleep_for_minimum_duration(duration: int, notifier: Optional[TelegramNotifier]) -> None:
    """
    Sleep for the given duration, ensuring it does not exceed the default maximum sleep time
    for the current time of day. Falls back to a random interval if duration is 0.

    Args:
        duration (int): The duration to sleep in minutes.
        notifier (Optional[TelegramNotifier]): The notifier instance for sending notifications.
    """
    default_max = get_default_sleep_times()[1]

    # Adjust duration if it exceeds the default maximum
    if duration > default_max:
        print(f"[DEBUG] Provided duration ({duration} minutes) exceeds default maximum ({default_max} minutes). Using default maximum.")
        duration = default_max

    if duration > 0:
        print(f"[DEBUG] Sleeping for duration: {duration} minutes.")
        sleep_random_interval(duration, duration + 1)
        if notifier:
            notifier.send_message(f"Sleeping for {duration} minutes before next check.")
    else:
        print("[DEBUG] No valid durations found. Sleeping for a random interval.")
        sleep_random_interval()
        if notifier:
            notifier.send_message("Sleeping randomly before next check.")

