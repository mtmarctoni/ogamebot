from typing import Literal, TypeAlias, TypedDict, List, Dict, Optional, Type
from config.shared_types import TechId, TechLevel, PlanetDict, PlanetId, PlanetName, StringCoords, TechName
from constants.energy import EnergyBuilding
from constants.facilities import Facility
from constants.lifeforms import Lifeforms
from constants.lifeform_buildings import (
    HumanLifeformBuilding, KaeleshLifeformBuilding, MechaLifeformBuilding, RocktalLifeformBuilding,
    HumanLifeformBuildingClass, KaeleshLifeformBuildingClass, MechaLifeformBuildingClass, RocktalLifeformBuildingClass
)
from constants.research import Research
from constants.resources import Resources

UpgradeGroup = Literal[
      "facilities",
      "resources",
      "energy",
      "research",
      "lifeform_buildings",
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
    lifeform_buildings: bool
    lifeform_research: bool
    storage: bool

type LifeformBuildingsType = HumanLifeformBuilding | KaeleshLifeformBuilding | MechaLifeformBuilding | RocktalLifeformBuilding
type LifeformBuildingTypeClass = type[HumanLifeformBuildingClass] | type[KaeleshLifeformBuildingClass] | type[MechaLifeformBuildingClass] | type[RocktalLifeformBuildingClass]

# Mapping from Lifeform enum to corresponding building enum class
LIFEFORM_BUILDING_ENUM_MAP: Dict[Lifeforms, Type[LifeformBuildingsType]] = {
    Lifeforms.HUMAN: HumanLifeformBuilding,
    Lifeforms.KAELESH: KaeleshLifeformBuilding,
    Lifeforms.MECHA: MechaLifeformBuilding,
    Lifeforms.ROCKTAL: RocktalLifeformBuilding,
}

# Mapping from Lifeform enum to corresponding building class helper (for ID lookups)
LIFEFORM_BUILDING_CLASS_MAP: Dict[
    Lifeforms,
    LifeformBuildingTypeClass
] = {
    Lifeforms.HUMAN: HumanLifeformBuildingClass,
    Lifeforms.KAELESH: KaeleshLifeformBuildingClass,
    Lifeforms.MECHA: MechaLifeformBuildingClass,
    Lifeforms.ROCKTAL: RocktalLifeformBuildingClass,
}

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

class ResourceMinimumsType(TypedDict):
    metal: int
    crystal: int
    deuterium: int

class UpgradesRawType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType
    priorities: UpgradesPrioritiesRawType
    soft_level_caps: UpgradeSoftLevelCapsRawType
    resource_minimums: ResourceMinimumsType

class DiscoveriesRawType(TypedDict):
    enable_discoveries: bool
    discovery_planet_id: str

class ConfigRawType(TypedDict):
    check_interval: int
    expeditions: ExpeditionsRawType
    discoveries: DiscoveriesRawType
    upgrades: UpgradesRawType

class UpgradesPrioritiesType(TypedDict):
    resources: List[str]  # Runtime: strings from JSON, converted on-demand
    storage: List[str]  # Runtime: strings from JSON, converted on-demand
    facilities: List[str]  # Runtime: strings from JSON, converted on-demand
    research: List[str]  # Runtime: strings from JSON, converted on-demand
    lifeform_buildings: Dict[str, List[str]]  # Runtime: string keys and values from JSON

UpgradeCapsDict: TypeAlias = Dict[str, int]

class UpgradeSoftLevelCapsType(TypedDict):
    energy: UpgradeCapsDict  # Runtime: string keys from JSON, converted on-demand
    resources: UpgradeCapsDict  # Runtime: string keys from JSON, converted on-demand
    facilities: UpgradeCapsDict  # Runtime: string keys from JSON, converted on-demand  
    research: UpgradeCapsDict  # Runtime: string keys from JSON, converted on-demand
    storage: UpgradeCapsDict  # Runtime: string keys from JSON
    lifeform_buildings: Dict[str, UpgradeCapsDict]  # Runtime: string keys from JSON

# Type aliases for processed/converted config data used in handlers
EnergySoftLevelCaps = Dict[EnergyBuilding, TechLevel]
ResourcesSoftLevelCaps = Dict[Resources, TechLevel]
FacilitiesSoftLevelCaps = Dict[Facility, TechLevel]
ResearchSoftLevelCaps = Dict[Research, TechLevel]
LifeformBuildingsSoftLevelCaps = Dict[LifeformBuildingsType, TechLevel]

# Priority list types after conversion
ResourcesPriorityList = List[Resources]
FacilitiesPriorityList = List[Facility]
ResearchPriorityList = List[Research]
LifeformBuildingsPriorityList = List[LifeformBuildingsType]

class UpgradesSectionType(TypedDict):
    group_order: List[UpgradeGroup]
    toggles: UpgradeTogglesRawType  # unchanged structure
    priorities: UpgradesPrioritiesType
    soft_level_caps: UpgradeSoftLevelCapsType
    resource_minimums: ResourceMinimumsType

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

class TechInfoDict(TypedDict, total=True):
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
    buildings: Dict[str, TechInfoDict]
    facilities: Dict[str, TechInfoDict]
    defense: Dict[str, TechInfoDict]
    ships: Dict[str, TechInfoDict]
    research: Dict[str, TechInfoDict]
    lifeform_buildings: Dict[str, TechInfoDict]
    lifeform_research: Dict[str, TechInfoDict]
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

class ExpeditionConfig(TypedDict, total=True):
    target_id: str

class DiscoveriesConfig(TypedDict, total=True):
    target_id: str