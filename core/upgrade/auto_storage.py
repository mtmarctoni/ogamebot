from config.types import EmpireSnapshotDict
from core.upgrade.buildings import find_storages_to_upgrade

# Placeholder for navigation and upgrade logic
# You will need to implement the actual browser automation logic

def upgrade_full_storages(snapshot: EmpireSnapshotDict) -> None:
    """
    Wrapper function to find storages to upgrade and trigger the upgrade process.
    Loads the latest snapshot if not provided, finds storages to upgrade, and (in the future) upgrades them.
    """

    storages_to_upgrade =find_storages_to_upgrade(snapshot)
    if not storages_to_upgrade:
        print("No storages need upgrading.")
        return

    for storage in storages_to_upgrade:
        print(f"[UPGRADE] {storage['planet']} {storage['coordinates']}: {storage['resource']} is {storage['percent']*100:.1f}% full (level {storage['building_level']}). Should upgrade building ID {storage['building_id']}.")
        # TODO: Implement navigation and upgrade logic here
        # Example: navigate_to_planet(storage['planet'])
        #          click_upgrade_button(storage['building_id'])
