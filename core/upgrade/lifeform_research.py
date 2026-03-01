from typing import List, Optional
from playwright.sync_api import Page

from config.types import ConfigType, PlanetDict, PlanetId, PlanetName, StringCoords, TechId, TechLevel, UpgradableLifeformResearch
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

    planet_id = planet['id']
    planet_name = planet["name"]
    coords = planet["coords"]
    upgradable_research = []

    for tech_id, tech_info in planet["lifeform_research"].items():
        if tech_info["upgradable"]:
            upgradable_research.append({
                "planet_id": PlanetId(str(planet_id)),
                "planet_name": PlanetName(planet_name),
                "coordinates": StringCoords(coords),
                "research_id": TechId(tech_id),
                "level": TechLevel(tech_info["level"]),
            })

    return upgradable_research


def handle_lifeform_research_upgrade(
    planet: PlanetDict, 
    page: Page, 
    config: ConfigType,
    notifier: Optional[TelegramNotifier],
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
    resource_minimums = config["upgrades"]["resource_minimums"]

    # Skip upgrade if planet is the designated expedition planet
    expedition_planet_id = config["expeditions"]["expedition_planet_id"]
    if str(planet['id']) == str(expedition_planet_id):
        print(f"[INFO] Skipping lifeform research upgrades on expedition planet {planet['name']} ({planet['coords']}).")
        return upgrade_durations

    upgradable_research = find_upgradable_lifeform_research(planet)

    if not upgradable_research:
        return upgrade_durations

    # Upgrade tech with the lowest level (first if a tie)
    min_level = min([t["level"] for t in upgradable_research])
    lowest_level_techs = [t for t in upgradable_research if t["level"] == min_level]
    research_to_upgrade = lowest_level_techs[0]
    tech_id = research_to_upgrade["research_id"]

    params: UpgradeTech = {
        "page": page,
        "planet_id": PlanetId(planet['id']),
        "tech_id": tech_id,
        "notifier": notifier,
        "resource_minimums": resource_minimums,
    }

    duration = upgrade_tech(**params)

    if duration > 0:
        upgrade_durations.append(duration)
        print(f"[INFO] Lifeform research upgrade: '{tech_id}' (level {min_level}) started on planet {planet['name']} (duration: {duration}s)")
        safe_notify(notifier,
            f"✅ Successfully started lifeform research for '{tech_id}' (level {min_level}) on planet {planet['name']}. Duration: {duration} seconds.")
    else:
        print(f"[ERROR] Lifeform research upgrade failed: '{tech_id}' on planet {planet['name']}")
        safe_notify(notifier, f"⚠️ Failed to upgrade lifeform research '{tech_id}' on planet {planet['name']}. Please check manually.")

    return upgrade_durations