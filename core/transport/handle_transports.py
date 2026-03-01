import time
from collections import defaultdict
from typing import Dict, List, Optional

from playwright.sync_api import Page

from config.types import EmpireSnapshotDict, PlanetDict, TransportsType
from core.notifications.telegram_notifier import TelegramNotifier, safe_notify
from core.transport.dispatcher import TargetType, dispatch_transport
from core.transport.fleet_planner import build_transport_fleet_for_origin
from core.transport.planner import TransportOrder, build_transport_orders
from core.utils.coords_utils import get_coords_from_planet


def _group_orders_by_origin(orders: List[TransportOrder]) -> Dict[str, List[TransportOrder]]:
    grouped: Dict[str, List[TransportOrder]] = defaultdict(list)
    for order in orders:
        grouped[str(order["origin"]["id"])].append(order)
    return grouped


def _resolve_target_type(planet: PlanetDict) -> TargetType:
    return "moon" if planet.get("type") == "moon" else "planet"


def handle_transports(
    page: Page,
    empire_data: EmpireSnapshotDict,
    notifier: Optional[TelegramNotifier],
    config: TransportsType,
) -> None:
    print("[INFO] Handling transports batch...")

    if not config["enable_transports"]:
        print("[INFO] Transports are disabled in the configuration.")
        return

    transport_orders = build_transport_orders(empire_data, config)
    if not transport_orders:
        print("[INFO] No transport orders generated for this cycle.")
        return

    grouped_orders = _group_orders_by_origin(transport_orders)

    for _, orders in grouped_orders.items():
        origin = orders[0]["origin"]
        fleet = build_transport_fleet_for_origin(origin, len(orders))
        if not fleet:
            print(f"[WARN] No fleet available for transport from {origin['name']} ({origin['coords']}).")
            continue

        print(f"[INFO] Processing {len(orders)} transports from {origin['name']} ({origin['coords']}).")

        for order in orders:
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
                time.sleep(max(0, config["dispatch_interval_seconds"]))
            else:
                print(f"[WARN] Transport not sent from {origin['name']} to {target['name']}.")
