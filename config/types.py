from typing import Literal, NewType, TypedDict, List, Dict, Optional
from constants.facilities import Facility
from constants.lifeforms import Lifeforms
from constants.research import Research
from constants.lifeform_buildings import HumanLifeformBuildingClass, KaeleshLifeformBuildingClass

TechId = NewType('TechId', str)
PlanetId = NewType('PlanetId', str)
PlanetName = NewType('PlanetName', str)
TechName = NewType('TechName', str)
TechLevel = NewType('TechLevel', int)
StringCoords = NewType('StringCoords', str)

UpgradeCategory = Literal[
    "facilities",
    "resources",
    "energy",
    "research",
    "lifeforms",
    "storage"
]

UpgradeGroup = Literal["facilities", "resources", "energy", "research", "lifeforms", "storage"]

# --- RAW CONFIG structure (from config.json) ---
class ExpeditionsRawType(TypedDict):
    enable_expeditions: bool
    expedition_planet_id: str

class UpgradeTogglesRawType(TypedDict):
    facilities: bool
    resources: bool
    energy: bool
    research: bool
    lifeforms: bool
    storage: bool

class UpgradesPrioritiesRawType(TypedDict):
    facilities: List[str]
    research: List[str]
    lifeform_buildings: Dict[Lifeforms, List[str]]

class UpgradesRawType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType
    priorities: UpgradesPrioritiesRawType

class ConfigRawType(TypedDict):
    check_interval: int
    expeditions: ExpeditionsRawType
    upgrades: UpgradesRawType

class UpgradesPrioritiesType(TypedDict):
    facilities: List[Facility]
    research: List[Research]
    lifeform_buildings: Dict[Lifeforms, List[HumanLifeformBuildingClass | KaeleshLifeformBuildingClass]]

class UpgradesSectionType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType  # unchanged structure
    priorities: UpgradesPrioritiesType

class ExpeditionsType(TypedDict):
    enable_expeditions: bool
    expedition_planet_id: str

class DiscoveriesType(TypedDict):
    enable_discoveries: bool
    discovery_planet_id: str

class ConfigType(TypedDict):
    check_interval: int
    expeditions: ExpeditionsType
    discoveries: DiscoveriesType
    upgrades: UpgradesSectionType


# Explicit resource and storage types for planets
class PlanetResources(TypedDict, total=False):
    metal: int
    crystal: int
    deuterium: int
    energy: int
    food: int
    population: int

class PlanetStorage(TypedDict, total=False):
    metalStorage: int
    crystalStorage: int
    deuteriumStorage: int
    foodStorage: int
    populationStorage: int

class QueueItemDict(TypedDict, total=False):
    type: str  # building, research, shipyard
    name: str
    level: Optional[int]
    count: Optional[int]
    finish_time: Optional[str]  # ISO8601

class BuildingInfoDict(TypedDict, total=False):
    level: int
    upgradable: bool
    upgrade_js: Optional[str]

class PlanetDict(TypedDict, total=False):
    id: PlanetId
    name: PlanetName
    coords: StringCoords
    type: str  # planet or moon
    specie: str
    fields: str
    temperature: str
    energy: str
    resources: PlanetResources
    storage: PlanetStorage
    buildings: Dict[str, BuildingInfoDict]
    facilities: Dict[str, BuildingInfoDict]
    defense: Dict[str, BuildingInfoDict]
    ships: Dict[str, BuildingInfoDict]
    research: Dict[str, BuildingInfoDict]
    lifeform_buildings: Dict[str, BuildingInfoDict]
    lifeform_research: Dict[str, BuildingInfoDict]
    queue: List[QueueItemDict]

class PlanetBase(TypedDict):
    id: PlanetId
    name: PlanetName
    coords: StringCoords
    specie: str

class PlayerDict(TypedDict):
    name: str
    id: Optional[str]

class EmpireSnapshotDict(TypedDict):
    timestamp: str  # ISO8601
    planets: List[PlanetDict]

class StorageUpgradeCandidate(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: StringCoords
    resource: TechName
    current: int
    max: int
    percent: float
    building_id: TechId
    building_level: TechLevel
    upgradable: bool

class UpgradableResourceBuilding(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: StringCoords
    resource: TechName
    building_id: TechId
    level: TechLevel

class UpgradableLifeformBuilding(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: StringCoords
    building_id: TechId
    building: TechName
    level: TechLevel

class UpgradableEnergyBuidling(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: StringCoords
    resource: TechName
    building_id: TechId
    level: TechLevel

class UpgradableLifeformResearch(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: StringCoords
    research_id: TechId
    level: TechLevel

class ShipToDispatch(TypedDict):
    ship_id: TechId
    count: int

FleetToDispatch = List[ShipToDispatch]
Coordinates = List[int]  # [galaxy, system, slot]

class ExpeditionConfig(TypedDict, total=False):
    target_id: str

class DiscoveriesConfig(TypedDict, total=False):
    target_id: str
