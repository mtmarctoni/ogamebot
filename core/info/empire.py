# core/info/empire_logger.py
from typing import Optional, cast
from playwright.sync_api import Page
from config.types import EmpireSnapshotDict
from core.info.info_extractor import extract_empire_view
from core.info.logger import log_empire_view
from core.notifications.telegram_notifier import TelegramNotifier

def extract_empire_info(page: Page, notifier: Optional[TelegramNotifier]) -> EmpireSnapshotDict:
    """
    Navigates to the Empire View page and extracts planet and moon data.
    """
    print("[INFO] Starting Empire View extraction...")
    # Wait for the Empire button to appear and click it (opens in new tab)
    with page.context.expect_page() as new_page_info:
        page.click('a.menubutton span.textlabel:text("Empire")')
    empire_page = new_page_info.value

    # Wait for the new page to load the expected content
    try:
        empire_page.wait_for_selector("div.planetWrapper div.planet", state="visible", timeout=20000)
    except Exception as e:
        print(f"[ERROR] Empire View load failed: {e} (URL: {empire_page.url})")
        raise

    # Extract planet data
    planets_html = empire_page.content()
    print("[INFO] Extracting planet data from Empire View...")
    planet_data = extract_empire_view(planets_html, is_moon=False)

    # Click the moons tab to load moon data
    print("[INFO] Switching to Moons tab for moon data extraction...")
    try:
        empire_page.click('#moonsTab')
        empire_page.wait_for_selector("div.planetWrapper div.planet", state="visible", timeout=20000)
    except Exception as e:
        print(f"[ERROR] Failed to extract moon data from Empire View: {e} (URL: {empire_page.url})")
        raise

    # Extract moon data
    moons_html = empire_page.content()
    print("[INFO] Extracting moon data from Empire View...")
    moon_data = extract_empire_view(moons_html, is_moon=True)

    # Combine planet and moon data
    empire_data: EmpireSnapshotDict = cast(EmpireSnapshotDict, planet_data)
    empire_data['planets'].extend(moon_data['planets'])

    # Log and notify
    log_empire_view(empire_data, notifier)

    return empire_data
