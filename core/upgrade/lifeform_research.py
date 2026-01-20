from typing import List, Optional
from playwright.sync_api import Page

from config.types import PlanetDict, PlanetId, PlanetName, StringCoords, TechId, TechLevel, UpgradableLifeformResearch
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech


def find_upgradable_lifeform_research(planet: PlanetDict) -> List[UpgradableLifeformResearch]:
    """
    Finds upgradable lifeform-specific research technologies on a given planet.
    
    Args:
        planet (PlanetDict): Planet data containing lifeform research details.

    Returns:
        List[Dict[str, any]]: A list of dictionaries representing upgradable research details.
    """
    upgradable_research: List[UpgradableLifeformResearch] = []

    planet_id = planet.get('id')
    planet_name = planet.get('name') or "Unknown"
    coords = planet.get('coords') or "?"
    upgradable_research = []

    for tech_id, tech_info in planet.get("lifeform_research", {}).items():
        if tech_info.get("upgradable"):
            upgradable_research.append({
                "planet_id": PlanetId(str(planet_id)),
                "planet_name": PlanetName(planet_name),
                "coordinates": StringCoords(coords),
                "research_id": TechId(tech_id),
                "level": TechLevel(tech_info.get("level", 0)),
            })

    return upgradable_research


def handle_lifeform_research_upgrade(
    planet: PlanetDict, 
    page: Page, 
    notifier: Optional[TelegramNotifier]
) -> List[int]:
    """
    Handles the upgrades of upgradable lifeform-specific research technologies.

    Args:
        planet (PlanetDict): Planet data.
        page (Page): Playwright page object for automation.
        notifier (Optional[TelegramNotifier]): Used for sending notifications.

    Returns:
        List[int]: A list of durations for successfully upgraded technologies.
    """
    upgrade_durations: List[int] = []
    upgradable_research = find_upgradable_lifeform_research(planet)

    if not upgradable_research:
        return upgrade_durations

    # Upgrade the first upgradable research
    research_to_upgrade = upgradable_research[0]  # Select the highest-priority research
    tech_id = research_to_upgrade["research_id"]

    params: UpgradeTech = {
        "page": page,
        "planet_id": PlanetId(planet.get("id", "")),
        "tech_id": tech_id,
        "notifier": notifier,
    }

    duration = upgrade_tech(**params)

    if duration > 0:
        upgrade_durations.append(duration)
        print(f"[INFO] Lifeform research upgrade: '{tech_id}' started on planet {planet.get('name', 'Unknown')} (duration: {duration}s)")
        safe_notify(notifier, f"✅ Successfully started lifeform research for '{tech_id}' on planet {planet.get('name', 'Unknown')}. Duration: {duration} seconds.")
    else:
        print(f"[ERROR] Lifeform research upgrade failed: '{tech_id}' on planet {planet.get('name', 'Unknown')}")
        safe_notify(notifier, f"⚠️ Failed to upgrade lifeform research '{tech_id}' on planet {planet.get('name', 'Unknown')}. Please check manually.")

    return upgrade_durations