import re
from typing import Tuple, Callable

# Type alias for all technology tuples (id, amount/level, category)
TechnologyTuple = Tuple[int, int, str]


# OGame page components
class COMPONENTS:
    overview = "overview"
    supplies = "supplies"
    lfbuildings = "lfbuildings"
    facilities = "facilities"
    traderOverview = "traderOverview"
    research = "research"
    shipyard = "shipyard"
    defenses = "defenses"
    fleetdispatch = "fleetdispatch"
    galaxy = "galaxy"
    empire = "empire"
    messages = "messages"

class ResourceStorageClass:
    metal_storage = 'metalStorage'
    crystal_storage = 'crystalStorage'
    deuterium_storage = 'deuteriumStorage'
    food_storage = 'foodStorage'
    population_storage = 'populationStorage'

    @classmethod
    def allStorages(cls) -> list[str]:
        return [
            cls.metal_storage,
            cls.crystal_storage,
            cls.deuterium_storage,
            cls.food_storage,
            cls.population_storage,
        ]
    
class ResourceClass:
    metal = 'metal'
    crystal = 'crystal'
    deuterium = 'deuterium'
    energy = 'energy'
    food = 'food'
    population = 'population'

    @classmethod
    def allResources(cls) -> list[str]:
        return [
            cls.metal,
            cls.crystal,
            cls.deuterium,
            cls.energy,
            cls.food,
            cls.population,
        ]
    
RESOURCE_TO_STORAGE = {
    ResourceClass.metal: ResourceStorageClass.metal_storage,
    ResourceClass.crystal: ResourceStorageClass.crystal_storage,
    ResourceClass.deuterium: ResourceStorageClass.deuterium_storage,
    ResourceClass.food: ResourceStorageClass.food_storage,
    ResourceClass.population: ResourceStorageClass.population_storage,
}
class destination(object):
    outer_space = 0
    planet = 1
    debris = 2
    moon = 3

# Energy consumption formulas for mines
ENERGY_CONSUMPTION: dict[str, Callable[[int], int]] = {
    ResourceClass.metal: lambda level: int(10 * level * (1.1 ** level)),
    ResourceClass.crystal: lambda level: int(10 * level * (1.1 ** level)),
    ResourceClass.deuterium: lambda level: int(20 * level * (1.1 ** level)),
}

# Resource upgrade preference
RESOURCE_UPGRADE_PREFERENCE = [ResourceClass.crystal, ResourceClass.deuterium, ResourceClass.metal]


def convert_to_destinations(dest: str | None) -> int:
    if dest is None:
        return destination.outer_space
    elif 'moon' in dest:
        return destination.moon
    elif 'tf' in dest:
        return destination.debris
    else:
        return destination.planet



def coordinates(galaxy: int, system: int, position: int = 0, dest: int = destination.planet) -> list[int]:
    return [galaxy, system, position, dest]


def convert_to_coordinates(coords: str) -> list[int]:
    match = re.search(r'\[(\d+):(\d+):(\d+)]', coords)
    if not match:
        raise ValueError(f"Invalid coordinates string: {coords}")
    return [int(match.group(1)), int(match.group(2)), int(match.group(3))]


class mission(object):
    attack = 1
    transport = 3
    park = 4
    park_ally = 5
    spy = 6
    colonize = 7
    recycle = 8
    destroy = 9
    expedition = 15
    trade = 16


class speed(object):
    _10 = 1
    _20 = 2
    _30 = 3
    _40 = 4
    _50 = 5
    _60 = 6
    _70 = 7
    _80 = 8
    _90 = 9
    _100 = 10
    max = 10
    min = 1


class buildings:
    metal_mine: TechnologyTuple = (1, 1, 'supplies')
    crystal_mine: TechnologyTuple = (2, 1, 'supplies')
    deuterium_mine: TechnologyTuple = (3, 1, 'supplies')
    solar_plant: TechnologyTuple = (4, 1, 'supplies')
    fusion_plant: TechnologyTuple = (12, 1, 'supplies')
    metal_storage: TechnologyTuple = (22, 1, 'supplies')
    crystal_storage: TechnologyTuple = (23, 1, 'supplies')
    deuterium_storage: TechnologyTuple = (24, 1, 'supplies')

    robotics_factory: TechnologyTuple = (14, 1, 'facilities')
    shipyard: TechnologyTuple = (21, 1, 'facilities')
    research_laboratory: TechnologyTuple = (31, 1, 'facilities')
    alliance_depot: TechnologyTuple = (34, 1, 'facilities')
    missile_silo: TechnologyTuple = (44, 1, 'facilities')
    nanite_factory: TechnologyTuple = (15, 1, 'facilities')
    terraformer: TechnologyTuple = (33, 1, 'facilities')
    repair_dock: TechnologyTuple = (36, 1, 'facilities')
    moon_base: TechnologyTuple = (41, 1, 'facilities')
    sensor_phalanx: TechnologyTuple = (42, 1, 'facilities')
    jump_gate: TechnologyTuple = (43, 1, 'facilities')

    @staticmethod
    def get_name(building_id: int) -> str | None:
        mapping = {
            1: 'Metal Mine',
            2: 'Crystal Mine',
            3: 'Deuterium Mine',
            4: 'Solar Plant',
            12: 'Fusion Reactor',
            22: 'Metal Storage',
            23: 'Crystal Storage',
            24: 'Deuterium Tank',
            14: 'Robotics Factory',
            21: 'Shipyard',
            31: 'Research Laboratory',
            34: 'Alliance Depot',
            44: 'Missile Silo',
            15: 'Nanite Factory',
            33: 'Terraformer',
            36: 'Repair Dock',
            41: 'Moon Base',
            42: 'Sensor Phalanx',
            43: 'Jump Gate',
        }
        return mapping.get(building_id)
    
    @staticmethod
    def get_building_id(resource_name: str) -> int | None:
        """
        Get the building ID for a given resource name (e.g., 'metal', 'crystal').
        """
        storage_class = RESOURCE_TO_STORAGE.get(resource_name)
        if not storage_class:
            return None  # Resource not found

        building = getattr(buildings, storage_class, None)
        if building:
            return building[0]  # Return the building ID (first element of the tuple)
        return None

    @staticmethod
    def solar_satellite(amount: int = 1) -> TechnologyTuple:
        return (212, amount, 'supplies')

    @staticmethod
    def crawler(amount: int = 1) -> TechnologyTuple:
        return (217, amount, 'supplies')

    @staticmethod
    def is_supplies(supplies: TechnologyTuple) -> bool:
        return supplies[2] == 'supplies'

    @staticmethod
    def is_facilities(facilities: TechnologyTuple) -> bool:
        return facilities[2] == 'facilities'

    @staticmethod
    def building_name(building: TechnologyTuple) -> str | None:
        mapping = {
            14: 'robotics_factory',
            21: 'shipyard',
            31: 'research_laboratory',
            34: 'alliance_depot',
            44: 'missile_silo',
            15: 'nanite_factory',
            33: 'terraformer',
            36: 'repair_dock',
            41: 'moon_base',
            42: 'sensor_phalanx',
            43: 'jump_gate',
            1: 'metal_mine',
            2: 'crystal_mine',
            3: 'deuterium_mine',
            4: 'solar_plant',
            12: 'fusion_plant',
            212: 'solar_satellite',
            217: 'crawler',
            22: 'metal_storage',
            23: 'crystal_storage',
            24: 'deuterium_storage',
        }
        return mapping.get(building[0])

    @staticmethod
    def rocket_launcher(amount: int = 1) -> TechnologyTuple:
        return (401, amount, 'defenses')

    @staticmethod
    def laser_cannon_light(amount: int = 1) -> TechnologyTuple:
        return (402, amount, 'defenses')

    @staticmethod
    def laser_cannon_heavy(amount: int = 1) -> TechnologyTuple:
        return (403, amount, 'defenses')

    @staticmethod
    def gauss_cannon(amount: int = 1) -> TechnologyTuple:
        return (404, amount, 'defenses')

    @staticmethod
    def ion_cannon(amount: int = 1) -> TechnologyTuple:
        return (405, amount, 'defenses')

    @staticmethod
    def plasma_cannon(amount: int = 1) -> TechnologyTuple:
        return (406, amount, 'defenses')

    @staticmethod
    def shield_dome_small(amount: int = 1) -> TechnologyTuple:
        return (407, amount, 'defenses')

    @staticmethod
    def shield_dome_large(amount: int = 1) -> TechnologyTuple:
        return (408, amount, 'defenses')

    @staticmethod
    def missile_interceptor(amount: int = 1) -> TechnologyTuple:
        return (502, amount, 'defenses')

    @staticmethod
    def missile_interplanetary(amount: int = 1) -> TechnologyTuple:
        return (503, amount, 'defenses')

    @staticmethod
    def is_defenses(defenses: TechnologyTuple) -> bool:
        return defenses[2] == 'defenses'

    @staticmethod
    def defense_name(defense: TechnologyTuple) -> str | None:
        if not buildings.is_defenses(defense):
            return None
        mapping = {
            401: 'rocket_launcher',
            402: 'laser_cannon_light',
            403: 'laser_cannon_heavy',
            404: 'gauss_cannon',
            405: 'ion_cannon',
            406: 'plasma_cannon',
            407: 'shield_dome_small',
            408: 'shield_dome_large',
            502: 'missile_interceptor',
            503: 'missile_interplanetary',
        }
        return mapping.get(defense[0])


class research(object):
    energy: TechnologyTuple = (113, 1, 'research')
    laser: TechnologyTuple = (120, 1, 'research')
    ion: TechnologyTuple = (121, 1, 'research')
    hyperspace: TechnologyTuple = (114, 1, 'research')
    plasma: TechnologyTuple = (122, 1, 'research')
    combustion_drive: TechnologyTuple = (115, 1, 'research')
    impulse_drive: TechnologyTuple = (117, 1, 'research')
    hyperspace_drive: TechnologyTuple = (118, 1, 'research')
    espionage: TechnologyTuple = (106, 1, 'research')
    computer: TechnologyTuple = (108, 1, 'research')
    astrophysics: TechnologyTuple = (124, 1, 'research')
    research_network: TechnologyTuple = (123, 1, 'research')
    graviton: TechnologyTuple = (199, 1, 'research')
    weapons: TechnologyTuple = (109, 1, 'research')
    shielding: TechnologyTuple = (110, 1, 'research')
    armor: TechnologyTuple = (111, 1, 'research')

    @staticmethod
    def is_research(research: TechnologyTuple) -> bool:
        return research[2] == 'research'

    @staticmethod
    def research_name(res: TechnologyTuple) -> str | None:
        if research.is_research(res):
            if res[0] == 113: return 'energy'
            elif res[0] == 120: return 'laser'
            elif res[0] == 121: return 'ion'
            elif res[0] == 114: return 'hyperspace'
            elif res[0] == 122: return 'plasma'
            elif res[0] == 115: return 'combustion_drive'
            elif res[0] == 117: return 'impulse_drive'
            elif res[0] == 118: return 'hyperspace_drive'
            elif res[0] == 106: return 'espionage'
            elif res[0] == 108: return 'computer'
            elif res[0] == 124: return 'astrophysics'
            elif res[0] == 123: return 'research_network'
            elif res[0] == 199: return 'graviton'
            elif res[0] == 109: return 'weapons'
            elif res[0] == 110: return 'shielding'
            elif res[0] == 111: return 'armor'

class ships(object):
    @staticmethod
    def light_fighter(amount: int = 1) -> TechnologyTuple: return (204, amount, 'shipyard')
    @staticmethod
    def heavy_fighter(amount: int = 1) -> TechnologyTuple: return (205, amount, 'shipyard')
    @staticmethod
    def cruiser(amount: int = 1) -> TechnologyTuple: return (206, amount, 'shipyard')
    @staticmethod
    def battleship(amount: int = 1) -> TechnologyTuple: return (207, amount, 'shipyard')
    @staticmethod
    def interceptor(amount: int = 1) -> TechnologyTuple: return (215, amount, 'shipyard')
    @staticmethod
    def bomber(amount: int = 1) -> TechnologyTuple: return (211, amount, 'shipyard')
    @staticmethod
    def destroyer(amount: int = 1) -> TechnologyTuple: return (213, amount, 'shipyard')
    @staticmethod
    def deathstar(amount: int = 1) -> TechnologyTuple: return (214, amount, 'shipyard')
    @staticmethod
    def reaper(amount: int = 1) -> TechnologyTuple: return (218, amount, 'shipyard')
    @staticmethod
    def explorer(amount: int = 1) -> TechnologyTuple: return (219, amount, 'shipyard')
    @staticmethod
    def small_transporter(amount: int = 1) -> TechnologyTuple: return (202, amount, 'shipyard')
    @staticmethod
    def large_transporter(amount: int = 1) -> TechnologyTuple: return (203, amount, 'shipyard')
    @staticmethod
    def colonyShip(amount: int = 1) -> TechnologyTuple: return (208, amount, 'shipyard')
    @staticmethod
    def recycler(amount: int = 1) -> TechnologyTuple: return (209, amount, 'shipyard')
    @staticmethod
    def espionage_probe(amount: int = 1) -> TechnologyTuple: return (210, amount, 'shipyard')
    @staticmethod
    def crawler(amount: int = 1) -> TechnologyTuple: return (217, amount, 'shipyard')

    @staticmethod
    def is_ship(ship: TechnologyTuple) -> bool:
        if ship[2] == 'shipyard':
            return True
        else:
            return False

    @staticmethod
    def ship_name(ship: TechnologyTuple) -> str | None:
        if ships.is_ship(ship):
            if ship[0] == 204: return 'light_fighter'
            elif ship[0] == 205: return 'heavy_fighter'
            elif ship[0] == 206: return 'cruiser'
            elif ship[0] == 207: return 'battleship'
            elif ship[0] == 215: return 'interceptor'
            elif ship[0] == 211: return 'bomber'
            elif ship[0] == 213: return 'destroyer'
            elif ship[0] == 214: return 'deathstar'
            elif ship[0] == 218: return 'reaper'
            elif ship[0] == 219: return 'explorer'
            elif ship[0] == 202: return 'small_transporter'
            elif ship[0] == 203: return 'large_transporter'
            elif ship[0] == 208: return 'colonyShip'
            elif ship[0] == 209: return 'recycler'
            elif ship[0] == 210: return 'espionage_probe'
            elif ship[0] == 217: return 'crawler'

    @staticmethod
    def ship_amount(ship: TechnologyTuple) -> int | None:
        if ships.is_ship(ship):
            return ship[1]

    @staticmethod
    def ship_id(ship: TechnologyTuple) -> int | None:
        if ships.is_ship(ship):
            return ship[0]


def fleet(
    light_fighter: int = 0,
    heavy_fighter: int = 0,
    cruiser: int = 0,
    battleship: int = 0,
    interceptor: int = 0,
    bomber: int = 0,
    destroyer: int = 0,
    deathstar: int = 0,
    reaper: int = 0,
    explorer: int = 0,
    small_transporter: int = 0,
    large_transporter: int = 0,
    colonyShip: int = 0,
    recycler: int = 0,
    espionage_probe: int = 0,
    crawler: int = 0
) -> list[TechnologyTuple]:
    fleetList: list[TechnologyTuple] = [
        ships.light_fighter(light_fighter),
        ships.heavy_fighter(heavy_fighter),
        ships.cruiser(cruiser),
        ships.battleship(battleship),
        ships.interceptor(interceptor),
        ships.bomber(bomber),
        ships.destroyer(destroyer),
        ships.deathstar(deathstar),
        ships.reaper(reaper),
        ships.explorer(explorer),
        ships.small_transporter(small_transporter),
        ships.large_transporter(large_transporter),
        ships.colonyShip(colonyShip),
        ships.recycler(recycler),
        ships.espionage_probe(espionage_probe),
        ships.crawler(crawler)
    ]
    return [ship for ship in fleetList if ship[1] != 0]

def convert_tech(code: int, category: str) -> TechnologyTuple:
    return code, 1, category


def resources(metal: float =0.0, crystal: float =0.0, deuterium: float =0.0):
    return [int(metal), int(crystal), int(deuterium)]


class status:
    active = 'active'
    inactive = 'inactive'
    vacation = 'vacation'
    noob = 'newbie'
    honorableTarget = 'strong'
    online = 'online'
    recently = 'recently'
    offline = 'offline'
    yourself = 'yourself'
    destroyed = 99999


class diplomacy:
    hostile = 'hostile'
    neutral = 'neutral'
    friendly = 'friendly'


class messages:
    spy_reports = 20


def price(technology: TechnologyTuple, level: int = 1):
    def multipli_resources(resources: list[int], multiplyer: int) -> list[int]:
        return [resource * multiplyer for resource in resources]

    if ships.is_ship(technology):
        if technology[0] == 204: return multipli_resources([3000, 1000, 0], technology[1])
        elif technology[0] == 205: return multipli_resources([6000, 4000, 0], technology[1])
        elif technology[0] == 206: return multipli_resources([20000, 7000, 2000], technology[1])
        elif technology[0] == 207: return multipli_resources([45000, 15000, 0], technology[1])
        elif technology[0] == 215: return multipli_resources([30000, 40000, 15000], technology[1])
        elif technology[0] == 211: return multipli_resources([50000, 25000, 15000], technology[1])
        elif technology[0] == 213: return multipli_resources([60000, 50000, 15000], technology[1])
        elif technology[0] == 214: return multipli_resources([5000000, 4000000, 1000000], technology[1])
        elif technology[0] == 218: return multipli_resources([85000, 55000, 20000], technology[1])
        elif technology[0] == 219: return multipli_resources([8000, 15000, 8000], technology[1])
        elif technology[0] == 202: return multipli_resources([2000, 2000, 0], technology[1])
        elif technology[0] == 203: return multipli_resources([6000, 6000, 0], technology[1])
        elif technology[0] == 208: return multipli_resources([10000, 20000, 10000], technology[1])
        elif technology[0] == 209: return multipli_resources([10000, 6000, 2000], technology[1])
        elif technology[0] == 210: return multipli_resources([0, 1000, 0], technology[1])
        elif technology[0] == 217: return multipli_resources([2000, 2000, 1000], technology[1])

    if buildings.is_supplies(technology):
        if technology[0] == 1: return resources(metal=60 * 1.5 ** level, crystal=15 * 1.5 ** level)
        elif technology[0] == 2: return resources(metal=48 * 1.6 ** level, crystal=24 * 1.6 ** level)
        elif technology[0] == 3: return resources(metal=225 * 1.5 ** level, crystal=75 * 1.5 ** level)
        elif technology[0] == 4: return resources(metal=75 * 1.5 ** level, crystal=30 * 1.5 ** level)
        elif technology[0] == 12: return resources(900 * 1.8 ** level, 360 * 1.8 ** level, 180 * 1.8 ** level)
        elif technology[0] == 22: return resources(metal=1000 * 2 ** level)
        elif technology[0] == 23: return resources(metal=1000 * 2 ** level, crystal=500 * 2 ** level)
        elif technology[0] == 24: return resources(metal=1000 * 2 ** level, crystal=1000 * 2 ** level)
        elif technology[0] == 212: return multipli_resources([0, 2000, 500], technology[1])
        elif technology[0] == 217: return multipli_resources([2000, 2000, 1000], technology[1])

    if buildings.is_facilities(technology):
        if technology[0] == 14: return resources(400 * 2 ** level, 120 * 2 ** level, 200 * 2 ** level)
        elif technology[0] == 21: return resources(200 * 2 ** level, 100 * 2 ** level, 50 * 2 ** level)
        elif technology[0] == 31: return resources(200 * 2 ** level, 400 * 2 ** level, 200 * 2 ** level)
        elif technology[0] == 34: return resources(metal=10000 * 2 ** level, crystal=20000 * 2 ** level)
        elif technology[0] == 44: return resources(20000 * 2 ** level, 20000 * 2 ** level, 1000 * 2 ** level)
        elif technology[0] == 15: return resources(1000000 * 2 ** level, 500000 * 2 ** level, 100000 * 2 ** level)
        elif technology[0] == 33: return resources(crystal=50000 * 2 ** level, deuterium=100000 * 2 ** level)
        elif technology[0] == 36: return resources(metal=40 * 5 ** level, deuterium=10 * 5 ** level)
        elif technology[0] == 41: return resources(10000 * 2 ** level, 20000 * 2 ** level, 10000 * 2 ** level)
        elif technology[0] == 42: return resources(10000 * 2 ** level, 20000 * 2 ** level, 10000 * 2 ** level)
        elif technology[0] == 43: return resources(10000 * 2 ** level, 20000 * 2 ** level, 10000 * 2 ** level)

    if buildings.is_defenses(technology):
        if technology[0] == 401: return multipli_resources([2000, 0, 0], technology[1])
        elif technology[0] == 402: return multipli_resources([1500, 500, 0], technology[1])
        elif technology[0] == 403: return multipli_resources([6000, 2000, 0], technology[1])
        elif technology[0] == 404: return multipli_resources([20000, 15000, 2000], technology[1])
        elif technology[0] == 405: return multipli_resources([5000, 3000, 0], technology[1])
        elif technology[0] == 406: return multipli_resources([50000, 50000, 30000], technology[1])
        elif technology[0] == 407: return multipli_resources([10000, 10000, 0], technology[1])
        elif technology[0] == 408: return multipli_resources([50000, 50000, 0], technology[1])
        elif technology[0] == 502: return multipli_resources([8000, 2000, 0], technology[1])
        elif technology[0] == 503: return multipli_resources([12500, 2500, 10000], technology[1])

    if research.is_research(technology):
        if technology[0] == 113: return resources(crystal=800 * 2 ** level, deuterium=400 * 2 ** level)
        elif technology[0] == 120: return resources(metal=200 * 2 ** level, crystal=100 * 2 ** level)
        elif technology[0] == 121: return resources(1000 * 2 ** level, 300 * 2 ** level, 100 * 2 ** level)
        elif technology[0] == 114: return resources(crystal=4000 * 2 ** level, deuterium=2000 * 2 ** level)
        elif technology[0] == 122: return resources(2000 * 2 ** level, 4000 * 2 ** level, 1000 * 2 ** level)
        elif technology[0] == 115: return resources(metal=400 * 2 ** level, deuterium=600 * 2 ** level)
        elif technology[0] == 117: return resources(2000 * 2 ** level, 4000 * 2 ** level, 600 * 2 ** level)
        elif technology[0] == 118: return resources(10000 * 2 ** level, 20000 * 2 ** level, 6000 * 2 ** level)
        elif technology[0] == 106: return resources(200 * 2 ** level, 1000 * 2 ** level, 200 * 2 ** level)
        elif technology[0] == 108: return resources(crystal=400 * 2 ** level, deuterium=600 * 2 ** level)
        elif technology[0] == 124: return resources(4000 * 1.75 ** level, 8000 * 1.75 ** level, 4000 * 1.75 ** level)
        elif technology[0] == 123: return resources(240000 * 2 ** level, 400000 * 2 ** level, 160000 * 2 ** level)
        elif technology[0] == 109: return resources(metal=800 * 2 ** level, crystal=200 * 2 ** level)
        elif technology[0] == 110: return resources(metal=200 * 2 ** level, crystal=600 * 2 ** level)
        elif technology[0] == 111: return resources(metal=1000 * 2 ** level)

# deposit capacity in k starting from level 0
DEPOSIT_CAPACITY = [
    10,
    20,
    40,
    75,
    140,
    255,
    470,
    865,
    1590,
    2920,
    5355,
    9820,
    18005,
    33005,
    60510,
    110925,
]

# Initial build steps based on
# https://ogame.fandom.com/wiki/Quick_Start_Guide
EARLY_STAGE_STEPS: list[object] = [
    # (building, level)
    (buildings.solar_plant, 1),
    (buildings.metal_mine, 1),
    (buildings.metal_mine, 2),
    (buildings.solar_plant, 2),
    (buildings.metal_mine, 3),
    (buildings.metal_mine, 4),
    (buildings.solar_plant, 3),
    (buildings.crystal_mine, 1),
    (buildings.solar_plant, 4),
    (buildings.metal_mine, 5),
    (buildings.crystal_mine, 2),
    (buildings.crystal_mine, 3),
    (buildings.solar_plant, 5),
    (buildings.deuterium_mine, 1),
    (buildings.crystal_mine, 4),
    (buildings.solar_plant, 6),
    (buildings.metal_mine, 6),
    (buildings.metal_mine, 7),
    (buildings.solar_plant, 7),
    (buildings.crystal_mine, 5),
    (buildings.deuterium_mine, 2),
    (buildings.solar_plant, 8),
    (buildings.deuterium_mine, 3),
    (buildings.deuterium_mine, 4),
    (buildings.solar_plant, 9),
    (buildings.deuterium_mine, 5),
    (buildings.robotics_factory, 1),
    (buildings.robotics_factory, 2),
    (buildings.research_laboratory, 1),
    (buildings.shipyard, 1),
    (buildings.crystal_mine, 6),
    (buildings.shipyard, 2),
    (buildings.solar_plant, 10),
    (buildings.deuterium_mine, 6),
    (buildings.metal_mine, 8),
    (research.energy, 1),
    (research.combustion_drive, 1),
    (buildings.solar_plant, 11),
    (buildings.crystal_mine, 7),
    (buildings.metal_mine, 9),
]
