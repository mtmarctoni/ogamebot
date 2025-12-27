from playwright.sync_api import Page

from config.config import COMPONENT_URL_TEMPLATE
from config.constants import COMPONENTS

def navigate_to_resources_page(page: Page, planet_id: str | int) -> None:
    """
    Navigates to the specified planet by accessing the respective URL.
    Ensures the URL is valid and the page loads successfully.
    """
    if isinstance(planet_id, int):
        planet_id = str(planet_id)

    if not planet_id.isdigit():
        raise ValueError(f"Invalid planet_id: {planet_id}. It must be a numeric string or integer.")

    url = COMPONENT_URL_TEMPLATE.format(component=COMPONENTS.supplies, planet_id=planet_id)
    if not url.startswith("http"):
        raise ValueError(f"Generated URL is invalid: {url}")

    # Debugging: Log the URL and planet_id before navigation
    print(f"[DEBUG] Navigating to resources page for planet_id: {planet_id}")
    print(f"[DEBUG] Generated URL: {url}")

    retries = 3
    for attempt in range(retries):
        try:
            page.goto(url, timeout=3000)  # Increase timeout to 60 seconds

            # Debugging: Log the current URL after navigation
            print(f"[DEBUG] Current page URL after navigation: {page.url}")

            # Confirm the page has reloaded successfully by checking for a specific element
            page.wait_for_selector("#technologies", timeout=10000)  # Increase timeout to 10 seconds

            # Debugging: Log if the page reload check passes
            print(f"[DEBUG] Page reload check passed for planet_id: {planet_id}")

            if not page.url.startswith(url):
                raise RuntimeError(f"Failed to navigate to the resources page for planet_id {planet_id}.")

            return  # Exit the function if navigation is successful
        except Exception as e:
            print(f"[ERROR] Navigation attempt {attempt + 1} failed for planet_id {planet_id}: {e}")
            if attempt == retries - 1:
                raise RuntimeError(f"All navigation attempts failed for planet_id {planet_id}.")