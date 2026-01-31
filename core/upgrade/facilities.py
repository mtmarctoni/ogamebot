from playwright.sync_api import Page
from typing import Optional, List
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from config.types import ConfigType, PlanetDict, PlanetId, TechId
from constants.facilities import Facility, Facilities
from core.upgrade.actions import UpgradeTech, upgrade_tech
from core.utils.calculate import extract_free_fields

def handle_facilities_building_upgrades(planet: PlanetDict, page: Page, config: ConfigType, notifier: Optional[TelegramNotifier] = None) -> List[int]:
    """
    Handles the upgrade of facilities on a given planet.
    Dynamically prioritizes Terraformer based on free fields.
    Continues trying other facilities if one fails (e.g., Research Lab blocked by ongoing research).
    """
    upgrade_durations: List[int] = []

    # extract the config that might be needed in future enhancements
    prioritized_facilities = [Facility(f) for f in config['upgrades']['priorities']['facilities']]

    # Extract free fields from the "fields" string
    fields = planet['fields']
    free_fields = extract_free_fields(fields)

    # Adjust priority dynamically based on free fields
    dynamic_priority = prioritized_facilities.copy()
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

    if planet['type'] == 'moon':
        # Only allow moonbase (building_id=41) upgrades on moons.
        allowed_facilities = ["41"]
    else:
        allowed_facilities = [Facilities.get_id_by_name(f) for f in dynamic_priority]

    # Track if we found any upgradable facilities
    upgradable_count = 0
    
    for facility_name in dynamic_priority:  # Use dynamic priority
        facility_id = Facilities.get_id_by_name(facility_name)
        if facility_id not in allowed_facilities:
            continue
        facility_info = planet['facilities'][facility_id]
        # Facility upgrade filtering rules
        ALLIANCE_DEPOT_ID = Facilities.get_id_by_name(Facility.ALLIANCE_DEPOT)
        SPACE_DOCK_ID = Facilities.get_id_by_name(Facility.SPACE_DOCK)
        MISSILE_SILO_ID = Facilities.get_id_by_name(Facility.MISSILE_SILO)
        if facility_id == ALLIANCE_DEPOT_ID:
            continue  # Never upgrade Alliance Depot
        if facility_id == SPACE_DOCK_ID and facility_info['level'] >= 7:
            continue  # Only upgrade Repair Dock if level < 7
        if facility_id == MISSILE_SILO_ID and facility_info['level'] >= 5:
            continue  # Only upgrade Missile Silo if level < 5
        if facility_info['upgradable']:
            upgradable_count += 1
            planet_id = PlanetId(planet['id'])
            facility_id = TechId(facility_id)
            # Prepare the facility upgrade parameters
            params: UpgradeTech = {
                'page': page,
                'planet_id': planet_id,
                'tech_id': facility_id,
                'notifier': notifier
            }

            # Attempt to upgrade the facility
            print(f"[INFO] Attempting to upgrade {facility_name} on planet {planet['name']} ({planet['coords']})...")
            duration = upgrade_tech(**params)

            if duration > 0:
                upgrade_durations.append(duration)
                print(f"[INFO] ✓ Successfully upgraded {facility_name} on planet {planet['name']} ({planet['coords']}). Duration: {duration}s")
                safe_notify(notifier, f"✅ Upgraded {facility_name} on planet {planet['name']} ({planet['coords']}). Duration: {duration}s")
                break  # Exit after successful upgrade
            else:
                print(f"[WARN] ⚠ Failed to upgrade {facility_name} on planet {planet['name']} ({planet['coords']}). Button may be blocked. Trying next candidate...")
                safe_notify(notifier, f"⚠️ Could not upgrade {facility_name} on planet {planet['name']} ({planet['coords']}) - may be blocked by ongoing operation")
                continue  # Continue to next facility

    # Log if no facilities were upgradable or if all attempts failed
    if upgradable_count == 0:
        print(f"[INFO] No upgradable facilities found on planet {planet['name']} ({planet['coords']})")
    elif not upgrade_durations:
        print(f"[WARN] No facilities could be upgraded on planet {planet['name']} ({planet['coords']}) - all candidates were blocked")

    return upgrade_durations