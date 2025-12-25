
from bs4 import BeautifulSoup
from typing import Optional
from playwright.sync_api import Page
from config.config import COMPONENT_URL_TEMPLATE, DEFAULT_PLANET_ID
from config.constants import COMPONENTS
from core.notifications.telegram_notifier import TelegramNotifier

def detect_attack(html: str) -> Optional[str]:
    """
    Returns a string with attack info if an attack is detected, otherwise None.
    """
    soup = BeautifulSoup(html, "html.parser")
    attack_div = soup.find("div", id="attack_alert")
    if attack_div:
        classes = attack_div.get("class")
        if isinstance(classes, list) and "noAttack" not in classes:
            title = attack_div.get("title")
            if isinstance(title, str):
                return title
            return "Attack detected!"
    return None

def check_for_attack_alert(page: Page, notifier: Optional[TelegramNotifier] = None) -> Optional[str]:
    """
    Navigates to the overview page, checks for attack alert, and returns info if present.
    If notifier is provided, sends a Telegram message on attack.
    """
    overview_url = COMPONENT_URL_TEMPLATE.format(
        component=COMPONENTS.overview,
        planet_id=DEFAULT_PLANET_ID
    )
    page.goto(overview_url)
    html = page.content()
    attack_info = detect_attack(str(html))
    if attack_info and notifier:
        notifier.send_message(f"⚠️ ALERT: {attack_info}")
    return attack_info
