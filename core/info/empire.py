# core/info/empire_logger.py
from typing import Optional, cast
from playwright.sync_api import Page
from config.types import EmpireSnapshotDict
from core.info.info_extractor import extract_empire_view
from core.info.logger import log_empire_view
from core.notifications.telegram_notifier import TelegramNotifier

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
