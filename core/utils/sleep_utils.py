import time
import random

def sleep_random_interval(min_minutes: int = 45, max_minutes: int = 75):
    """
    Sleep for a random interval between min_minutes and max_minutes (in minutes).
    """
    minutes = random.randint(min_minutes, max_minutes)
    print(f"\nSleeping for {minutes} minutes before next check... (Ctrl+C to stop)")
    time.sleep(minutes * 60)
