from typing import List, Optional
from playwright.sync_api import Page

from config.bot import UpgradeHandlersType
from config.types import ConfigType, EmpireSnapshotDict
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.auto_storage import upgrade_full_storages
from core.upgrade.energy import handle_energy_buildings_upgrade
from core.upgrade.facilities import handle_facilities_building_upgrades
from core.upgrade.lifeform_buildings import handle_lifeform_buildings_upgrade
from core.upgrade.buildings import handle_building_resources_upgrade
from core.upgrade.research import handle_research_upgrades

# Map upgrade category names to their handler functions
UPGRADE_HANDLERS: UpgradeHandlersType= {
    "facilities": handle_facilities_building_upgrades,
    "resources": handle_building_resources_upgrade,
    "energy": handle_energy_buildings_upgrade,
    "research": handle_research_upgrades,
    "lifeforms": handle_lifeform_buildings_upgrade,
    "storage": upgrade_full_storages
}


def handle_upgrades(empire_data: EmpireSnapshotDict, page: Page, notifier: Optional[TelegramNotifier], config: ConfigType) -> int:
    """
    Handles upgrades for all planets in the empire data.

    Args:
        empire_data (dict): Data containing information about all planets.
        page: Playwright page object for interacting with the game.
        notifier: TelegramNotifier instance for sending notifications.
    """
    total_durations: List[int] = []

    # Use new nested upgrades config layout
    upgrades_section = config["upgrades"]
    upgrade_order = upgrades_section["group_order"]
    upgrade_toggles = upgrades_section["toggles"]


    for planet in empire_data["planets"]:
        planet_name = planet.get('name', 'Unknown')
        planet_id = planet.get('id', 'Unknown')
        print(f"\nProcessing upgrades for planet: {planet_name} (ID: {planet_id})")

        planet_durations: List[int] = []
        for upgrade in upgrade_order:
            # Legacy: fallback to old enable_X_upgrades keys if not set in upgrade_toggles
            enabled = upgrade_toggles.get(upgrade, config.get(f"enable_{upgrade}_upgrades", True))
            if not enabled:
                continue
            handler = UPGRADE_HANDLERS.get(upgrade)
            if handler:
                durations = handler(planet, page, notifier)
                planet_durations.extend(durations if durations else [])
        total_durations.extend([d for d in planet_durations if d > 0])

    if total_durations:
        return min(total_durations)
    return 0
