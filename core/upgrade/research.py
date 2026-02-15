from typing import List, Optional
from config.types import ConfigType, PlanetDict, PlanetId, TechId
from playwright.sync_api import Page
from constants.research import Research, Researches
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech

def handle_research_upgrades(planet: PlanetDict, page: Page, config: ConfigType, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of research technologies on a given planet.
    Checks if there are upgradable research technologies and upgrades the first available one based on priority.
    Returns the upgrade duration if an upgrade is performed, otherwise an empty list.
    """
    upgrade_durations: List[int] = []

    # Get config section for upgrades if needed in future enhancements
    prioritized_researches = [Research(r) for r in config["upgrades"]['priorities']['research']]

    # Parse research soft level caps from config
    research_soft_caps = config["upgrades"]["soft_level_caps"]["research"]

    for research_name in prioritized_researches:
        research_id = Researches.get_id_by_name(research_name)
        research_info = planet['research'][research_id]
        current_level = research_info['level']
        cap = research_soft_caps[research_name.name]

        # Enforce cap
        if current_level >= cap:
            print(f"[WARN] Skipping {research_name}: at or above soft cap ({current_level} >= {cap}) on planet {planet['name']} ({planet['coords']}).")
            safe_notify(notifier, f"⚠️ {research_name.name} on planet {planet['name']} is at soft level cap ({cap}). Upgrade skipped.")
            continue
        if research_info.get('upgradable', False):
            planet_id = PlanetId(planet['id'])
            tech_id = TechId(research_id)
            # Prepare the research upgrade parameters
            params: UpgradeTech = {
                'page': page,
                'planet_id': planet_id,
                'tech_id': tech_id,
                'notifier': notifier
            }

            # Upgrade the research
            print(f"[DEBUG] Upgrading {research_name} on planet {planet['name']} ({planet['coords']}).")
            duration = upgrade_tech(**params)

            if duration > 0:
                upgrade_durations.append(duration)
                safe_notify(notifier, f"Upgraded {research_name} on planet {planet['name']} ({planet['coords']}).. Duration: {duration} seconds.")
            else:
                safe_notify(notifier, f"Failed to upgrade {research_name} on planet {planet['name']} ({planet['coords']})..")

            break  # Exit after upgrading one research

    return upgrade_durations