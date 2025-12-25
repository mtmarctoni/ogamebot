from playwright.sync_api import Page

from config.config import COMPONENT_URL_TEMPLATE
from config.constants import COMPONENTS

def navigate_to_planet(page: Page, planet_id: str) -> None:
    """
    Navigates to the specified planet by accessing the respective URL.
    """
    page.goto(COMPONENT_URL_TEMPLATE.format(component=COMPONENTS.supplies,planet_id=planet_id))