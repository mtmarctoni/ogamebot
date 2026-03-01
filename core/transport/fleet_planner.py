from typing import Dict

from config.types import FleetToDispatch, PlanetDict, ShipToDispatch, TechId
from constants.ships import (
    EXCLUDED_TRANSPORT_SHIPS,
    RESERVE_ON_PLANET_TRANSPORT_SHIPS,
    Ship,
    Ships,
)


def _extract_ship_counts(planet: PlanetDict) -> Dict[Ship, int]:
    ships_data = planet.get("ships", {})
    counts: Dict[Ship, int] = {}

    for ship_id, info in ships_data.items():
        try:
            ship_type = Ships.get_name_by_id(str(ship_id))
        except ValueError:
            continue

        count = int(info.get("level", 0))
        if count <= 0:
            continue

        counts[ship_type] = count

    return counts


def _get_per_dispatch_count(ship_type: Ship, total_count: int, dispatch_count: int) -> int:
    if dispatch_count <= 0:
        return 0

    if ship_type in EXCLUDED_TRANSPORT_SHIPS:
        return 0

    if ship_type in RESERVE_ON_PLANET_TRANSPORT_SHIPS:
        return total_count // (dispatch_count + 1)

    # Attack ships: keep all flying by distributing over dispatches
    return total_count // dispatch_count


def build_transport_fleet_for_origin(origin: PlanetDict, dispatch_count: int) -> FleetToDispatch:
    ship_counts = _extract_ship_counts(origin)
    fleet: FleetToDispatch = []

    for ship_type, total_count in ship_counts.items():
        per_dispatch = _get_per_dispatch_count(ship_type, total_count, dispatch_count)
        if per_dispatch <= 0:
            continue

        ship_id = Ships.get_id_by_name(ship_type)
        fleet.append(
            ShipToDispatch(
                {
                    "ship_id": TechId(ship_id),
                    "count": per_dispatch,
                }
            )
        )

    return fleet

