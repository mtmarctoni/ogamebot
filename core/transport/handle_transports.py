import time
from collections import defaultdict
from typing import Dict, List, Optional

from playwright.sync_api import Page

from config.types import EmpireSnapshotDict, PlanetDict, TransportsType
from constants.general import COMPONENTS
from core.navigation.planet import navigate_to_section
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.transport.dispatcher import TargetType, dispatch_transport
from core.transport.fleet_planner import build_transport_fleet_for_origin
from core.transport.planner import TransportOrder, build_transport_orders
from core.utils.coords_utils import get_coords_from_planet
from core.utils.fleet_slots import get_fleet_slots_info

_last_transport_dispatch_at: Dict[str, float] = {}


def _group_orders_by_origin(orders: List[TransportOrder]) -> Dict[str, List[TransportOrder]]:
    grouped: Dict[str, List[TransportOrder]] = defaultdict(list)
    for order in orders:
        grouped[str(order["origin"]["id"])].append(order)
    return grouped


def _resolve_target_type(planet: PlanetDict) -> TargetType:
    return "moon" if planet.get("type") == "moon" else "planet"


def _is_origin_in_cooldown(origin_id: str, cooldown_seconds: int) -> bool:
    if cooldown_seconds <= 0:
        return False
    last_dispatch_at = _last_transport_dispatch_at.get(origin_id)
    if last_dispatch_at is None:
        return False
    return (time.time() - last_dispatch_at) < cooldown_seconds


def handle_transports(
    page: Page,
    empire_data: EmpireSnapshotDict,
    notifier: Optional[TelegramNotifier],
    config: TransportsType,
    expedition_planet_id: str,
) -> int:
    print("[INFO] Handling transports batch...")
    next_check_seconds = 0

    if not config["enable_transports"]:
        print("[INFO] Transports are disabled in the configuration.")
        return next_check_seconds

    transport_orders = build_transport_orders(empire_data, config, expedition_planet_id)
    if not transport_orders:
        print("[INFO] No transport orders generated for this cycle.")
        return next_check_seconds

    grouped_orders = _group_orders_by_origin(transport_orders)

    for origin_id, orders in grouped_orders.items():
        origin = orders[0]["origin"]
        if _is_origin_in_cooldown(origin_id, config["cooldown_seconds"]):
            remaining_cooldown = max(0, int(config["cooldown_seconds"] - (time.time() - _last_transport_dispatch_at[origin_id])))
            if remaining_cooldown > 0:
                next_check_seconds = remaining_cooldown if next_check_seconds == 0 else min(next_check_seconds, remaining_cooldown)
            print(
                f"[INFO] Skipping transports from {origin['name']} ({origin['coords']}) due to cooldown "
                f"({config['cooldown_seconds']}s)."
            )
            continue

        try:
            navigate_to_section(page, origin["id"], COMPONENTS.FLEET_DISPATCH)
            slots_info = get_fleet_slots_info(page)
        except Exception as exc:
            print(f"[WARN] Could not read fleet slots for transport origin {origin['name']}: {exc}")
            continue

        if not slots_info:
            print(f"[WARN] Could not parse fleet slots for transport origin {origin['name']}. Skipping.")
            continue

        available_fleet_slots = slots_info["available_fleets"]
        print(
            f"[INFO] Available transport fleet slots for {origin['name']}: "
            f"{slots_info['current_fleets']}/{slots_info['max_fleets']} "
            f"(available: {available_fleet_slots})"
        )

        if available_fleet_slots <= 0:
            print(f"[INFO] No fleet slots available for transports from {origin['name']} ({origin['coords']}).")
            continue

        orders_to_dispatch = orders[:available_fleet_slots]
        if len(orders_to_dispatch) < len(orders):
            print(
                f"[INFO] Capping transports from {origin['name']} to {len(orders_to_dispatch)} "
                f"due to fleet slot availability."
            )

        fleet = build_transport_fleet_for_origin(origin, len(orders_to_dispatch))
        if not fleet:
            print(f"[WARN] No fleet available for transport from {origin['name']} ({origin['coords']}).")
            continue

        print(f"[INFO] Processing {len(orders_to_dispatch)} transports from {origin['name']} ({origin['coords']}).")
        sent_from_origin = False

        for order in orders_to_dispatch:
            target = order["target"]
            target_coords = get_coords_from_planet(target)
            target_type = _resolve_target_type(target)
            resources = order["resources"]

            if resources["metal"] + resources["crystal"] + resources["deuterium"] <= 0:
                print(f"[INFO] Skipping empty transport from {origin['name']} to {target['name']}.")
                continue

            try:
                sent_resources = dispatch_transport(
                    page=page,
                    origin_id=origin["id"],
                    ships=fleet,
                    target_coordinates=target_coords,
                    target_type=target_type,
                    resources=resources,
                )
            except Exception as exc:
                print(f"[ERROR] Transport dispatch failed from {origin['name']} to {target['name']}: {exc}")
                safe_notify(notifier, f"❌ Transport failed: {origin['name']} -> {target['name']}: {exc}")
                continue

            if sent_resources:
                message = (
                    f"✅ Transport sent: {origin['name']} ({origin['coords']}) -> "
                    f"{target['name']} ({target['coords']}) | "
                    f"M:{sent_resources['metal']:,} C:{sent_resources['crystal']:,} D:{sent_resources['deuterium']:,}"
                )
                print(message)
                safe_notify(notifier, message)
                sent_from_origin = True
                time.sleep(max(0, config["dispatch_interval_seconds"]))
            else:
                print(f"[WARN] Transport not sent from {origin['name']} to {target['name']}.")

        if sent_from_origin:
            _last_transport_dispatch_at[origin_id] = time.time()
            cooldown_seconds = max(0, config["cooldown_seconds"])
            if cooldown_seconds > 0:
                next_check_seconds = cooldown_seconds if next_check_seconds == 0 else min(next_check_seconds, cooldown_seconds)

    return next_check_seconds
