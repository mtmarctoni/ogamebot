# navigation.py
"""
Navigation and game entry logic for OGame bot.
Modularized for future extensibility.
"""
from typing import cast
from playwright.sync_api import Page

def enter_universe(page: Page, universe_name: str = "") -> Page:
    """
    Clicks the 'Play' button for the first available universe.
    Optionally, match by universe_name if provided.
    """
    # Wait for the 'Last played' button to be visible
    page.wait_for_selector("#joinGame .button-default")
    # Click the 'Last played' button to enter the main game
    page.click("#joinGame .button-default")
    # Try to wait for new tab to open (the game), fallback to current page if timeout
    try:
        new_page = cast(Page, page.context.wait_for_event("page", timeout=5000)) # type: ignore
        return new_page
    except Exception:
        # No new tab opened, continue with current page
        return page

