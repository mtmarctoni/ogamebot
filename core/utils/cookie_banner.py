from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def handle_cookie_banner(page: Page) -> None:
    """
    Checks for the OGame cookie banner and clicks 'Accept Cookies' if present.
    Safe to call repeatedly; ignores transient errors.
    """
    try:
        accept_button = page.locator("div.cookiebanner1 button:has-text('Accept Cookies')").first
        if accept_button.is_visible(timeout=1500):
            accept_button.click(timeout=5000)
            print("[INFO] Cookie banner detected and accepted.")
    except (PlaywrightTimeoutError, PlaywrightError):
        pass
