# session_manager.py


import os
import json
from typing import Tuple
from playwright.sync_api import Playwright, Browser, BrowserContext

SESSION_FILE = "fb_session.json"


def save_session(context: BrowserContext) -> None:
    storage = context.storage_state()
    with open(SESSION_FILE, "w") as f:
        json.dump(storage, f)


def load_session(playwright: Playwright, browser_type: str = "chromium") -> Tuple[Browser, BrowserContext]:
    if os.path.exists(SESSION_FILE):
        browser: Browser = getattr(playwright, browser_type).launch(headless=False)
        context: BrowserContext = browser.new_context(storage_state=SESSION_FILE)
    else:
        browser: Browser = getattr(playwright, browser_type).launch(headless=False)
        context: BrowserContext = browser.new_context()
    return browser, context
