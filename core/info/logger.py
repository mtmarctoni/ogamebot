from typing import List, Optional
from config.constants import RESOURCE_TO_STORAGE, ResourceClass
from config.config import STORAGE_WARNING_THRESHOLD, STORAGE_UPGRADE_THRESHOLD
from config.types import EmpireSnapshotDict, PlanetResources, PlanetStorage
from core.notifications.telegram_notifier import TelegramNotifier

def log_empire_view(empire_data: EmpireSnapshotDict, notifier: Optional[TelegramNotifier]) -> None:
    print("\n\033[1;36mEmpire View Planets:\033[0m")
    summary_lines: List[str] = []
    for planet in empire_data.get('planets', []):
        name = planet.get('name', 'Unknown')
        coords = planet.get('coords', '?')
        resources: PlanetResources = planet.get('resources', {}) or {}
        storage: PlanetStorage = planet.get('storage', {}) or {}
        res_map = {'metal': '🪙', 'crystal': '💎', 'deuterium': '🧪', 'food': '🍖', 'population': '👥', 'energy': '⚡'}
        resource_keys = ResourceClass.allResources()
        lines: List[str] = []
        for r in resource_keys:
            if r == 'energy':
                energy_val = planet.get('energy', 0)
                lines.append(f"⚡ {energy_val}")
                continue
            current = resources.get(r, 0)
            max_cap = storage.get(RESOURCE_TO_STORAGE[r])
            percent = (current / max_cap * 100) if max_cap else 0
            alert = ''
            upgradable = ''
            if max_cap:
                if percent >= STORAGE_UPGRADE_THRESHOLD * 100:
                    alert = '🚨'
                elif percent >= STORAGE_WARNING_THRESHOLD * 100:
                    alert = '⚠️'

                # Check if the resource is upgradable
                building_info = planet.get('buildings', {}).get(str(RESOURCE_TO_STORAGE[r]), {})
                if building_info.get('upgradable', False):
                    upgradable = '⬆️'

            lines.append(f"{res_map.get(r, r.title())} {current:,} - ({percent:.1f}%) {alert} {upgradable}")
        res_str = '\n'.join(lines)
        planet_summary = (
            f"★ {name} [{coords}]\n"
            f"{res_str}\n"
        )
        print(f"\033[1;33m★ {name} \033[0m(\033[1;32m{coords}\033[0m)")
        print(f"    \033[1;35mResources/Storage:\033[0m\n{res_str}")
        summary_lines.append(planet_summary)
    if notifier:
        try:
            message = "Empire View Planets:\n\n" + "\n\n".join(summary_lines)
            notifier.send_message(message)
        except Exception as e:
            print(f"Failed to send empire view notification: {e}")