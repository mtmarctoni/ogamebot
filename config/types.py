from typing import Literal, TypedDict, List, Dict, Optional
from constants.energy import EnergyBuilding
from config.shared_types import TechId, TechLevel, PlanetDict, PlanetId, PlanetName, StringCoords, TechName
from constants.facilities import Facility
from constants.lifeforms import Lifeforms
from constants.research import Research
from constants.lifeform_buildings import HumanLifeformBuilding, KaeleshLifeformBuilding, MechaLifeformBuilding, RocktalLifeformBuilding
from constants.resources import ResourceStorage, Resources


UpgradeGroup = Literal[
      "facilities",
      "resources",
      "energy",
      "research",
      "lifeforms",
      "lifeform_research",
      "storage"
    ]

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
    lifeform_research: bool
    storage: bool

type LifeformBuildingsType = HumanLifeformBuilding | KaeleshLifeformBuilding | MechaLifeformBuilding | RocktalLifeformBuilding

class UpgradesPrioritiesRawType(TypedDict):
    resources: List[str]
    storage: List[str]
    facilities: List[str]
    research: List[str]
    lifeform_buildings: Dict[str, List[str]]

class UpgradeSoftLevelCapsRawType(TypedDict):
    energy: Dict[str, int]
    resources: Dict[str, int]
    storage: Dict[str, int]
    facilities: Dict[str, int]
    research: Dict[str, int]
    lifeform_buildings: Dict[str, Dict[str, int]]

class UpgradesRawType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType
    priorities: UpgradesPrioritiesRawType
    soft_level_caps: UpgradeSoftLevelCapsRawType

class DiscoveriesRawType(TypedDict):
    enable_discoveries: bool
    discovery_planet_id: str

class ConfigRawType(TypedDict):
    check_interval: int
    expeditions: ExpeditionsRawType
    discoveries: DiscoveriesRawType
    upgrades: UpgradesRawType

class UpgradesPrioritiesType(TypedDict):
    resources: List[TechName]
    storage: List[ResourceStorage]
    facilities: List[Facility]
    research: List[Research]
    lifeform_buildings: Dict[Lifeforms, List[LifeformBuildingsType]]

class UpgradeSoftLevelCapsType(TypedDict):
    energy: Dict[EnergyBuilding, TechLevel]
    resources: Dict[Resources, TechLevel]
    facilities: Dict[Facility, TechLevel]
    research: Dict[Research, TechLevel]
    lifeform_buildings: Dict[Lifeforms, Dict[LifeformBuildingsType, TechLevel]]

class UpgradesSectionType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType  # unchanged structure
    priorities: UpgradesPrioritiesType
    soft_level_caps: UpgradeSoftLevelCapsType

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
class PlanetResources(TypedDict, total=True):
    metal: int
    crystal: int
    deuterium: int
    energy: int
    food: int
    population: int

class PlanetStorage(TypedDict, total=True):
    metalStorage: int
    crystalStorage: int
    deuteriumStorage: int
    foodStorage: int
    populationStorage: int

class QueueItemDict(TypedDict, total=True):
    type: str  # building, research, shipyard
    name: str
    level: Optional[int]
    count: Optional[int]
    finish_time: Optional[str]  # ISO8601

class BuildingInfoDict(TypedDict, total=True):
    level: int
    upgradable: bool
    upgrade_js: Optional[str]

class PlanetDict(TypedDict, total=True):
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