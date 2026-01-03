from playwright.sync_api import Page
from typing import Optional, List
from config.config import FACILITIES_PRIORITY
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from config.types import PlanetDict, PlanetId, TechId
from constants.facilities import Facility, Facilities
from core.upgrade.actions import UpgradeTech, upgrade_tech

def extract_free_fields(fields: str) -> int:
    """
    Extracts the number of free fields from the "fields" string.

    Args:
        fields (str): The "fields" string in the format "used/total".

    Returns:
        int: The number of free fields.
    """
    used, total = map(int, fields.split('/'))
    return total - used

def handle_facilities_building(planet: PlanetDict, page: Page, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of facilities on a given planet.
    Dynamically prioritizes Terraformer based on free fields.
    """
    upgrade_durations: List[int] = []

    # Extract free fields from the "fields" string
    fields = planet.get('fields', "0/0")
    free_fields = extract_free_fields(fields)

    # Adjust priority dynamically based on free fields
    dynamic_priority = FACILITIES_PRIORITY.copy()
    if free_fields > 25:
        # Ignore Terraformer
        dynamic_priority.remove(Facility.TERRAFORMER)
    elif 15 < free_fields <= 25:
        # Terraformer is high priority but behind Robotics/Lab
        dynamic_priority.remove(Facility.TERRAFORMER)
        dynamic_priority.insert(2, Facility.TERRAFORMER)  # Place after Robotics/Lab
    elif free_fields <= 15:
        # Terraformer is top priority
        dynamic_priority.remove(Facility.TERRAFORMER)
        dynamic_priority.insert(0, Facility.TERRAFORMER)

    for facility_name in dynamic_priority:  # Use dynamic priority
        facility_id = Facilities.get_id_by_name(facility_name)
        facility_info = planet.get('facilities', {}).get(facility_id, {})
        if facility_info.get('upgradable', False):
            planet_id = PlanetId(planet.get('id', 'Unknown'))
            facility_id = TechId(facility_id)
            # Prepare the facility upgrade parameters
            params: UpgradeTech = {
                'page': page,
                'planet_id': planet_id,
                'tech_id': facility_id,
                'notifier': notifier
            }

            # Upgrade the facility
            print(f"[DEBUG] Upgrading {facility_name} on planet {planet.get('name')} ({planet.get('coords')})")
            duration = upgrade_tech(**params)

            if duration > 0:
                upgrade_durations.append(duration)
                safe_notify(notifier, f"Upgraded {facility_name} on planet {planet.get('name')} ({planet.get('coords')}). Duration: {duration} seconds.")
            else:
                safe_notify(notifier, f"Failed to upgrade {facility_name} on planet {planet.get('name')} ({planet.get('coords')}).")

            break  # Exit after upgrading one facility

    return upgrade_durations