import time
import random
import datetime
from config.config import NIGHT_MIN_SLEEP, NIGHT_MAX_SLEEP, DAY_MIN_SLEEP, DAY_MAX_SLEEP, DEFAULT_MIN_SLEEP, DEFAULT_MAX_SLEEP

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
