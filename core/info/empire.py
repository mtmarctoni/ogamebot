# core/info/empire_logger.py
from typing import List, Optional, cast
from playwright.sync_api import Page
from config.types import EmpireSnapshotDict
from core.info.info_extractor import extract_empire_view
from config.constants import buildings as BUILDINGS_CONST
from core.notifications.telegram_notifier import TelegramNotifier

def log_empire_view(empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier]) -> None:
    print("\n\033[1;36mEmpire View Planets:\033[0m")
    summary_lines: List[str] = []
    for planet in empire_data.get('planets', []):
        name = planet.get('name', 'Unknown')
        coords = planet.get('coords', '?')
        resources = planet.get('resources', {})
        buildings = planet.get('buildings', {})
        # Use human-readable building names if available
        building_levels: object = []
        for k, v in buildings.items():
            try:
                int_id = int(k)
                bname = BUILDINGS_CONST.get_name(int_id) or f"ID {k}"
            except Exception:
                bname = f"ID {k}"
            building_levels.append((bname, v.get('level')))
        # Sort for consistent output
        building_levels.sort()
        # Format resources with emojis and fixed width
        res_map = {'metal': '🪙', 'crystal': '💎', 'deuterium': '🧪'}
        res_str = ' '.join(f"{res_map.get(r, r.title())}{str(resources.get(r, '-')).rjust(6)}" for r in ['metal', 'crystal', 'deuterium'])
        # Format buildings as a table
        bld_lines = [f"{bname.ljust(24, '·')} | {str(level).rjust(3)}" for bname, level in building_levels]
        bld_table = '\n'.join(bld_lines)
        # Compose planet summary with triple backticks for Telegram
        planet_summary = (
            f"★ {name} [{coords}]\n"
            f"Resources: {res_str}\n\n"
            f"🏗️ Buildings:\n"
            f"\n__________\n\n{bld_table}\n__________\n"
        )
        print(f"\033[1;33m★ {name} \033[0m(\033[1;32m{coords}\033[0m)")
        print(f"    \033[1;35mResources:\033[0m {resources}")
        print(f"    \033[1;34mBuildings:\033[0m {dict(building_levels)}")
        summary_lines.append(planet_summary)
    if notifier:
        try:
            message = "Empire View Planets:\n\n" + "\n\n".join(summary_lines)
            notifier.send_message(message)
        except Exception as e:
            print(f"Failed to send empire view notification: {e}")

def extract_empire_info(page: Page, notifier: Optional[TelegramNotifier]) -> EmpireSnapshotDict:
    """
    Navigates to the Empire View page and extracts planet data.
    """
    print("[Empire] Clicking the Empire menu button to open Empire View...")
    # Wait for the Empire button to appear and click it (opens in new tab)
    with page.context.expect_page() as new_page_info:
        page.click('a.menubutton span.textlabel:text("Empire")')
    empire_page = new_page_info.value
    # Wait for the new page to load the expected content
    try:
        empire_page.wait_for_selector("div.planetWrapper div.planet", state="visible", timeout=20000)
    except Exception as e:
        print(f"[Empire] Failed to find expected selectors on Empire View page.\n Error: {e} \nCurrent URL: {empire_page.url}")
        content_preview = empire_page.content()[:2000]
        print(f"[Empire] Page content preview:\n{content_preview}\n...")
        raise
    html = empire_page.content()
    empire_data = cast(EmpireSnapshotDict, extract_empire_view(html))
    log_empire_view(empire_data, notifier)  # Log and notify

    return empire_data
