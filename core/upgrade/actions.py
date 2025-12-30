from typing import Optional, TypedDict
from core.utils.time_utils import parse_duration
from playwright.sync_api import Page

from core.notifications.telegram_notifier import TelegramNotifier

class UpgradeTech(TypedDict):
    page: Page
    planet_id: str
    tech_id: str
    notifier: Optional[TelegramNotifier]

def upgrade_tech(*, page: Page, planet_id: str, tech_id: str, notifier: Optional[TelegramNotifier] = None) -> int:
    """
    Perform the upgrade for any technology (building, research, ship, etc.) and return the upgrade duration.

    Args:
        page (Page): The Playwright page instance.
        params (Dict[str, Any]): A dictionary containing all necessary parameters, including:
            - planet_id (str): The ID of the planet where the upgrade is to be performed.
            - tech_id (str | int): The unique ID of the technology to upgrade.
        notifier (Optional[TelegramNotifier]): Notifier for sending upgrade notifications.

    Returns:
        int: The duration of the upgrade in seconds.
    """

    # Navigate directly to the planet and component using query parameters
    url = f"/game/index.php?page=ingame&component=overview&cp={planet_id}"
    page.goto(url)
    print(f"[DEBUG] Navigated to planet ID {planet_id} for upgrading tech ID {tech_id}.")

    # Locate the upgrade button for the technology
    tech_li_selector = f'#technologies li.technology[data-technology="{tech_id}"] button.upgrade'
    button = page.query_selector(tech_li_selector)

    if button:
        button.click()
        print(f"[DEBUG] Clicked upgrade button for tech ID {tech_id} on planet ID {planet_id}.")

        # Wait for the building state to update (e.g., countdown timer or level change)
        try:
            page.wait_for_selector('time.buildingCountdown', state="visible", timeout=5000)  # Adjust timeout as needed
            countdown = page.locator('time.buildingCountdown').first
            if countdown:
                duration_attr = countdown.get_attribute('datetime') or ""
                duration_text = countdown.inner_text() or ""
                return parse_duration(duration_attr, duration_text)
        except Exception as e:
            print(f"[ERROR] Upgrade did not start for tech ID {tech_id} on planet ID {planet_id}: {e}")
            return 0

    print(f"[ERROR] Upgrade button not found for tech ID {tech_id} on planet ID {planet_id}.")
    return 0