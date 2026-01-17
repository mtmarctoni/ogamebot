from typing import Literal, NewType, TypedDict, List, Dict, Optional

TechId = NewType('TechId', str)
PlanetId = NewType('PlanetId', str)
PlanetName = NewType('PlanetName', str)
TechName = NewType('TechName', str)
TechLevel = NewType('TechLevel', int)
Coordinates = NewType('Coordinates', str)

UpgradeCategory = Literal[
    "facilities",
    "resources",
    "energy",
    "research",
    "lifeforms",
    "storage"
]

class UpgradeTogglesType(TypedDict, total=False):
    facilities: bool
    resources: bool
    energy: bool
    research: bool
    lifeforms: bool
    storage: bool

# Config types
class ConfigType(TypedDict, total=False):
    check_interval: int
    enable_resource_upgrades: bool
    enable_energy_upgrades: bool
    enable_facility_upgrades: bool
    enable_research_upgrades: bool
    enable_storage_upgrades: bool
    enable_lifeform_upgrades: bool
    enable_expeditions: bool
    expedition_planet_id: str
    upgrade_order: List[UpgradeCategory]
    upgrade_toggles: UpgradeTogglesType

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
    coords: Coordinates
    coordinates: str
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
    coords: Coordinates
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
    coordinates: Coordinates
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
    coordinates: Coordinates
    resource: TechName
    building_id: TechId
    level: TechLevel

class UpgradableLifeformBuilding(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: Coordinates
    building_id: TechId
    building: TechName
    level: TechLevel

class UpgradableEnergyBuidling(TypedDict):
    planet_id: PlanetId
    planet_name: PlanetName
    coordinates: Coordinates
    resource: TechName
    building_id: TechId
    level: TechLevel

class ShipToDispatch(TypedDict):
    ship_id: TechId
    count: int

FleetToDispatch = List[ShipToDispatch]

class ExpeditionConfig(TypedDict, total=False):
    target_id: str
