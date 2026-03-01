from typing import List, TypedDict

from config.types import EmpireSnapshotDict, PlanetDict, TransportResourcesType, TransportsType


class TransportOrder(TypedDict):
    origin: PlanetDict
    target: PlanetDict
    resources: TransportResourcesType


def _clamp_non_negative(value: int) -> int:
    return max(0, int(value))


def _calculate_total_resources_to_transport(
    origin: PlanetDict,
    amount_mode: str,
    requested: TransportResourcesType,
) -> TransportResourcesType:
    current_resources = origin["resources"]

    if amount_mode == "percentage":
        return {
            "metal": _clamp_non_negative(current_resources["metal"] * requested["metal"] // 100),
            "crystal": _clamp_non_negative(current_resources["crystal"] * requested["crystal"] // 100),
            "deuterium": _clamp_non_negative(current_resources["deuterium"] * requested["deuterium"] // 100),
        }

    # absolute mode
    return {
        "metal": _clamp_non_negative(min(requested["metal"], current_resources["metal"])),
        "crystal": _clamp_non_negative(min(requested["crystal"], current_resources["crystal"])),
        "deuterium": _clamp_non_negative(min(requested["deuterium"], current_resources["deuterium"])),
    }


def _split_resources_equally(resources: TransportResourcesType, count: int) -> List[TransportResourcesType]:
    if count <= 0:
        return []

    base = {
        "metal": resources["metal"] // count,
        "crystal": resources["crystal"] // count,
        "deuterium": resources["deuterium"] // count,
    }
    remainder = {
        "metal": resources["metal"] % count,
        "crystal": resources["crystal"] % count,
        "deuterium": resources["deuterium"] % count,
    }

    split: List[TransportResourcesType] = []
    for index in range(count):
        split.append(
            {
                "metal": base["metal"] + (1 if index < remainder["metal"] else 0),
                "crystal": base["crystal"] + (1 if index < remainder["crystal"] else 0),
                "deuterium": base["deuterium"] + (1 if index < remainder["deuterium"] else 0),
            }
        )

    return split


def build_transport_orders(empire_data: EmpireSnapshotDict, config: TransportsType) -> List[TransportOrder]:
    target_ids = {str(planet_id) for planet_id in config["target_planet_ids"]}
    all_planets = empire_data["planets"]
    id_to_planet = {str(planet["id"]): planet for planet in all_planets}

    target_planets = [id_to_planet[target_id] for target_id in target_ids if target_id in id_to_planet]

    if not target_planets:
        return []

    orders: List[TransportOrder] = []

    for origin in all_planets:
        # Moon resources are usually not relevant for this flow
        if origin.get("type") == "moon":
            continue

        origin_id = str(origin["id"])
        eligible_targets = [target for target in target_planets if str(target["id"]) != origin_id]
        if not eligible_targets:
            continue

        total_resources = _calculate_total_resources_to_transport(
            origin,
            config["amount_mode"],
            config["resources"],
        )

        if total_resources["metal"] + total_resources["crystal"] + total_resources["deuterium"] <= 0:
            continue

        split_resources = _split_resources_equally(total_resources, len(eligible_targets))

        for target, resources in zip(eligible_targets, split_resources):
            if resources["metal"] + resources["crystal"] + resources["deuterium"] <= 0:
                continue
            orders.append({"origin": origin, "target": target, "resources": resources})

    return orders
