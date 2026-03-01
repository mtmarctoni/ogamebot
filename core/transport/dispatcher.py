import re
from typing import Literal, Optional

from playwright.sync_api import Page

from config.shared_types import PlanetId
from config.types import FleetToDispatch, Coordinates, TransportResourcesType
from constants.general import COMPONENTS
from constants.ships import Ships
from core.navigation.planet import navigate_to_section

TargetType = Literal["planet", "moon", "debris"]


TARGET_TYPE_SELECTOR = {
    "planet": "#pbutton",
    "moon": "#mbutton",
    "debris": "#dbutton",
}


def _go_to_fleet_dispatch(page: Page, origin_id: PlanetId) -> None:
    navigate_to_section(page, origin_id, COMPONENTS.FLEET_DISPATCH)


def _fill_ships_and_go_next(page: Page, ships: FleetToDispatch) -> bool:
    has_ships = False
    for ship in ships:
        ship_name = Ships.get_name_by_id(str(ship["ship_id"])).value
        ship_input = page.locator(f"input[name='{ship_name}']")
        if ship_input.is_visible():
            ship_input.fill(str(ship["count"]))
            has_ships = True

    if not has_ships:
        return False

    page.keyboard.press("Enter")
    page.wait_for_selector("#fleet2", state="visible", timeout=10000)
    return True


def _select_target_type(page: Page, target_type: TargetType) -> None:
    selector = TARGET_TYPE_SELECTOR[target_type]
    button = page.locator(selector)
    if button.is_visible(timeout=3000):
        button.click()


def _fill_destination_and_select_transport_mission(
    page: Page,
    coordinates: Coordinates,
    target_type: TargetType,
) -> None:
    galaxy, system, position = coordinates

    galaxy_input = page.locator("input#galaxy")
    system_input = page.locator("input#system")
    position_input = page.locator("input#position")

    galaxy_input.focus()
    galaxy_input.type(str(galaxy))

    system_input.focus()
    system_input.type(str(system))

    position_input.focus()
    position_input.type(str(position)) 

    # page.locator("input#galaxy").fill(str(galaxy))
    # page.locator("input#system").fill(str(system))
    # page.locator("input#position").fill(str(position))

    _select_target_type(page, target_type)

    mission_button = page.locator("#missionButton3")
    mission_button.click()


def _parse_int_from_text(raw_text: str) -> int:
    digits = re.sub(r"[^0-9]", "", raw_text or "")
    return int(digits) if digits else 0


def _fit_resources_to_capacity(resources: TransportResourcesType, capacity: int) -> TransportResourcesType:
    if capacity <= 0:
        return {"metal": 0, "crystal": 0, "deuterium": 0}

    total = resources["metal"] + resources["crystal"] + resources["deuterium"]
    if total <= capacity:
        return {
            "metal": int(resources["metal"]),
            "crystal": int(resources["crystal"]),
            "deuterium": int(resources["deuterium"]),
        }

    scale = capacity / total
    fitted: TransportResourcesType = {
        "metal": int(resources["metal"] * scale),
        "crystal": int(resources["crystal"] * scale),
        "deuterium": int(resources["deuterium"] * scale),
    }

    remaining = capacity - (fitted["metal"] + fitted["crystal"] + fitted["deuterium"])
    for key in ("metal", "crystal", "deuterium"):
        if remaining <= 0:
            break
        if resources[key] > 0:
            fitted[key] += 1
            remaining -= 1

    return fitted


def _fill_resources_and_send(page: Page, resources: TransportResourcesType) -> Optional[TransportResourcesType]:
    page.wait_for_selector("#metal", timeout=10000)

    max_resources_text = page.locator("#maxresources").inner_text()
    max_capacity = _parse_int_from_text(max_resources_text)
    fitted_resources = _fit_resources_to_capacity(resources, max_capacity)

    if fitted_resources["metal"] + fitted_resources["crystal"] + fitted_resources["deuterium"] <= 0:
        return None

    page.locator("#metal").fill(str(fitted_resources["metal"]))
    page.locator("#crystal").fill(str(fitted_resources["crystal"]))
    page.locator("#deuterium").fill(str(fitted_resources["deuterium"]))

    page.locator("#sendFleet").click()
    # No confirmation selector check; return immediately
    return fitted_resources


def dispatch_transport(
    page: Page,
    origin_id: PlanetId,
    ships: FleetToDispatch,
    target_coordinates: Coordinates,
    target_type: TargetType,
    resources: TransportResourcesType,
) -> Optional[TransportResourcesType]:
    _go_to_fleet_dispatch(page, origin_id)

    if not _fill_ships_and_go_next(page, ships):
        return None

    _fill_destination_and_select_transport_mission(page, target_coordinates, target_type)
    return _fill_resources_and_send(page, resources)
