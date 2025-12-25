# core/info/empire_logger.py
from typing import List, Optional, cast
from playwright.sync_api import Page
from config.config import EMPIRE_VIEW_URL
from config.types import EmpireSnapshotDict
from core.info.info_extractor import extract_empire_view
from core.notifications.telegram_notifier import TelegramNotifier

def log_empire_view(empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier]) -> None:
    print("\n\033[1;36mEmpire View Planets:\033[0m")
    summary_lines: List[str] = []
    for planet in empire_data.get('planets', []):
        name = planet.get('name', 'Unknown')
        coords = planet.get('coords', '?')
        resources = planet.get('resources', {})
        buildings = planet.get('buildings', {})
        building_levels = {k: v.get('level') for k, v in buildings.items()}
        print(f"\033[1;33m★ {name} \033[0m(\033[1;32m{coords}\033[0m)")
        print(f"    \033[1;35mResources:\033[0m {resources}")
        print(f"    \033[1;34mBuildings:\033[0m {building_levels}")
        summary_lines.append(f"★ {name} ({coords})\n  Resources: {resources}\n  Buildings: {building_levels}")
    if notifier:
        try:
            message = "Empire View Planets:\n" + "\n\n".join(summary_lines)
            notifier.send_message(message)
        except Exception as e:
            print(f"Failed to send empire view notification: {e}")

def extract_empire_info(page: Page, notifier: Optional[TelegramNotifier]) -> EmpireSnapshotDict:
    """
    Navigates to the Empire View page and extracts planet data.
    """
    page.goto(EMPIRE_VIEW_URL)
    page.wait_for_selector("div.planet")  # Wait for at least one planet to load
    html = page.content()
    empire_data = cast(EmpireSnapshotDict, extract_empire_view(html))
    log_empire_view(empire_data, notifier)  # Log and notify

    return empire_data
