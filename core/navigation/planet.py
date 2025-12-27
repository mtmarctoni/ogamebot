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

    page.goto(url)
    # Confirm the page has reloaded successfully by checking for a specific element
    page.wait_for_selector("#technologies", timeout=5000)
    if not page.url.startswith(url):
        raise RuntimeError(f"Failed to navigate to the resources page for planet_id {planet_id}.")