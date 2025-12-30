import time
import random
import datetime
from typing import List, Optional
from config.config import NIGHT_MIN_SLEEP, NIGHT_MAX_SLEEP, DAY_MIN_SLEEP, DAY_MAX_SLEEP, DEFAULT_MIN_SLEEP, DEFAULT_MAX_SLEEP
from core.notifications.telegram_notifier import TelegramNotifier

def sleep_random_interval(min_minutes: int = 0, max_minutes: int = 0) -> None:
    """
    Sleep for a random interval based on the time of day to mimic human behavior.
    If min_minutes and max_minutes are provided, use them instead of the default behavior.
    """
    if min_minutes == 0 or max_minutes == 0:
        now = datetime.datetime.now()
        current_hour = now.hour

        if current_hour >= 2 and current_hour < 8:
            # After 2 AM, sleep for at least 4 hours
            min_minutes = NIGHT_MIN_SLEEP
            max_minutes = NIGHT_MAX_SLEEP
        elif current_hour >= 8 and current_hour < 20:
            # Between 8 AM and 8 PM, check every 25–35 minutes
            min_minutes = DAY_MIN_SLEEP
            max_minutes = DAY_MAX_SLEEP
        else:
            # Default behavior for other times
            min_minutes = DEFAULT_MIN_SLEEP
            max_minutes = DEFAULT_MAX_SLEEP

    minutes = random.randint(min_minutes, max_minutes)
    print(f"\nSleeping for {minutes} minutes before next check... (Ctrl+C to stop)")
    time.sleep(minutes * 60)

def sleep_for_minimum_duration(duration_lists: List[int], notifier: Optional[TelegramNotifier]) -> None:
    """
    Calculate the minimum non-zero duration from a list of lists of durations
    and sleep for that duration.

    Args:
        duration_lists (List[List[int]]): A list of lists containing integer durations.

    Returns:
        None
    """
    # Flatten the list of lists and filter out zero durations
    all_durations: List[int] = [duration for duration in duration_lists if duration > 0]

    if all_durations:
        min_duration = min(all_durations)
        print(f"[DEBUG] Sleeping for minimum duration: {min_duration}")
        sleep_random_interval(min_duration, min_duration + 1)
        
        notifier.send_message(f"Sleeping for {min_duration} seconds before next check.") if notifier else None
    else:
        print("[DEBUG] No valid durations found. Sleeping for a random interval.")
        sleep_random_interval()
        notifier.send_message(f"Sleeping randomly before next check.") if notifier else None

