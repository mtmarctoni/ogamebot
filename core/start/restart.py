import time
from typing import Optional

from core.notifications.telegram_notifier import TelegramNotifier, safe_notify


def handle_restart(notifier: Optional[TelegramNotifier], restart_count: int, max_restarts: int, delay: int) -> None:
    """
    Handles the restart logic, including printing messages, sending notifications, and sleeping.

    Args:
        notifier (Optional[TelegramNotifier]): The notifier instance for sending notifications.
        restart_count (int): The current restart attempt count.
        max_restarts (int): The maximum allowed restart attempts.
        delay (int): The delay in seconds between restarts.
    """
    if restart_count < max_restarts:
        print(f"[INFO] Restarting bot (#{restart_count}/{max_restarts}) in {delay} seconds...")
        if notifier:
            safe_notify(notifier, f"🔄 Restarting bot (attempt {restart_count}/{max_restarts})...")
        time.sleep(delay)
    else:
        print(f"[ERROR] Max restart attempts ({max_restarts}) reached. Stopping bot.")
        if notifier:
            safe_notify(notifier, f"❌ Bot stopped after {max_restarts} failed restart attempts.")
