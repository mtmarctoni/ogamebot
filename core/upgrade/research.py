from typing import List, Optional
from config.types import ConfigType, PlanetDict, PlanetId, TechId
from playwright.sync_api import Page
from constants.research import Researches
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.upgrade.actions import UpgradeTech, upgrade_tech
from config.config import RESEARCH_PRIORITY

def handle_research_upgrades(planet: PlanetDict, page: Page, config: ConfigType, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of research technologies on a given planet.
    Checks if there are upgradable research technologies and upgrades the first available one based on priority.
    Returns the upgrade duration if an upgrade is performed, otherwise an empty list.
    """
    upgrade_durations: List[int] = []

    # Get config section for upgrades if needed in future enhancements
    upgrades_section = config["upgrades"]
    print(f"[DEBUG] Upgrade section: {upgrades_section}")

    for research_name in RESEARCH_PRIORITY:  # Use priority from config
        research_id = Researches.get_id_by_name(research_name)
        research_info = planet.get('research', {}).get(research_id, {})
        if research_info.get('upgradable', False):
            planet_id = PlanetId(planet.get('id', 'Unknown'))
            research_id = TechId(research_id)
            # Prepare the research upgrade parameters
            params: UpgradeTech = {
                'page': page,
                'planet_id': planet_id,
                'tech_id': research_id,
                'notifier': notifier
            }

            # Upgrade the research
            print(f"[DEBUG] Upgrading {research_name} on planet {planet.get('name')} ({planet.get('coords')})")
            duration = upgrade_tech(**params)

            if duration > 0:
                upgrade_durations.append(duration)
                safe_notify(notifier, f"Upgraded {research_name} on planet {planet.get('name')} ({planet.get('coords')}). Duration: {duration} seconds.")
            else:
                safe_notify(notifier, f"Failed to upgrade {research_name} on planet {planet.get('name')} ({planet.get('coords')}).")

            break  # Exit after upgrading one research

    return upgrade_durations