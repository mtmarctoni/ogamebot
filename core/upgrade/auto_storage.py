
from typing import Optional
from config.types import EmpireSnapshotDict
from core.notifications.telegram_notifier import TelegramNotifier
from core.upgrade.buildings import find_storages_to_upgrade

# Placeholder for navigation and upgrade logic
# You will need to implement the actual browser automation logic

def upgrade_full_storages(snapshot: EmpireSnapshotDict, notifier: Optional[TelegramNotifier] = None) -> None:
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
        if notifier:
            try:
                notifier.send_message(
                    f"⚠️ STORAGE ALERT: {storage['planet']} {storage['coordinates']}: {storage['resource'].title()} storage at {int(storage['percent']*100)}% (Level {storage['building_level']}, {storage['current']}/{storage['max']}) needs upgrade."
                )
            except Exception as e:
                print(f"[TELEGRAM ERROR] Could not send storage alert: {e}")
