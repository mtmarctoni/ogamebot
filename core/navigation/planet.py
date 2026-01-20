from playwright.sync_api import Page

from config.config import COMPONENT_URL_TEMPLATE
from config.types import PlanetId
from constants.general import COMPONENTS

def navigate_to_section(page: Page, planet_id: PlanetId, section: COMPONENTS) -> None:
    """
    Generic function to navigate to a specific section of a planet.

    Args:
        page (Page): The Playwright page instance.
        planet_id (str): The ID of the planet to navigate to.
        section (COMPONENTS): The section to navigate to (e.g., COMPONENTS.SUPPLIES, COMPONENTS.LFBUILDINGS).

    Returns:
        None
    """
    url = COMPONENT_URL_TEMPLATE.format(component=section.value, planet_id=planet_id)
    if not url.startswith("http"):
        raise ValueError(f"Generated URL is invalid: {url}")

    print(f"[DEBUG] Navigating to {section.name.lower()} page for planet_id: {planet_id}")
    print(f"[DEBUG] Generated URL: {url}")

    retries = 3
    for attempt in range(retries):
        try:
            page.goto(url, timeout=3000)
            print(f"[DEBUG] Current page URL after navigation: {page.url}")

            # Wait for the correct selector depending on section
            if section == COMPONENTS.GALAXY:
                page.wait_for_selector("#eventboxFilled", timeout=10000)
            elif section == COMPONENTS.FLEET_DISPATCH:
                page.wait_for_selector("#fleet1", timeout=10000)
            else:
                page.wait_for_selector("#technologies", timeout=10000)
            print(f"[DEBUG] Page reload check passed for planet_id: {planet_id}")

            if not page.url.startswith(url):
                raise RuntimeError(f"Failed to navigate to the {section.name.lower()} page for planet_id {planet_id}.")

            return
        except Exception as e:
            print(f"[ERROR] Navigation attempt {attempt + 1} failed for planet_id {planet_id}: {e}")
            if attempt == retries - 1:
                raise RuntimeError(f"All navigation attempts failed for planet_id {planet_id}.")