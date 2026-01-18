import subprocess
from config.config import MAX_RESTART_ATTEMPTS, RESTART_DELAY
from core.start.restart import handle_restart
from core.start.run_bot_session import run_bot_session
from core.notifications.telegram_notifier import create_notifier

def get_git_version_info():
    try:
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        commit = commit.decode('utf-8').strip()
        date = subprocess.check_output(['git', 'log', '-1', '--date=short', '--pretty=format:%ad'])
        date = date.decode('utf-8').strip()
        return commit, date
    except Exception:
        return None, None

def print_version_banner():
    commit, date = get_git_version_info()
    if commit and date:
        print("\n==============================")
        print(f"OGameBot Version: [commit {commit}] built on {date}")
        print("==============================\n")
    else:
        print("\n==============================")
        print("OGameBot Version: [version info unavailable]")
        print("==============================\n")

def main() -> None:
    print_version_banner()
    notifier = create_notifier()
    restart_count = 0
    while restart_count < MAX_RESTART_ATTEMPTS:
        should_restart = run_bot_session(notifier)
        if not should_restart:
            break
        restart_count += 1
        handle_restart(notifier, restart_count, MAX_RESTART_ATTEMPTS, RESTART_DELAY)

if __name__ == "__main__":
    main()
