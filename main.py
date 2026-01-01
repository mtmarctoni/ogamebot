from config.config import MAX_RESTART_ATTEMPTS, RESTART_DELAY
from core.start.restart import handle_restart
from core.start.run_bot_session import run_bot_session
from core.notifications.telegram_notifier import create_notifier

def main() -> None:
    notifier = create_notifier()

    restart_count = 0

    while restart_count < MAX_RESTART_ATTEMPTS:
        should_restart = run_bot_session(notifier)

        if not should_restart:
            # User requested stop or clean exit
            break

        restart_count += 1
        handle_restart(notifier, restart_count, MAX_RESTART_ATTEMPTS, RESTART_DELAY)

if __name__ == "__main__":
    main()
