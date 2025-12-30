from typing import TypedDict, List, Dict, Optional



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
    id: int
    name: str
    coords: str
    coordinates: str
    type: str  # planet or moon
    fields: str
    temperature: str
    energy: str
    resources: PlanetResources
    storage: PlanetStorage
    buildings: Dict[str, BuildingInfoDict]
    station: Dict[str, BuildingInfoDict]
    defense: Dict[str, BuildingInfoDict]
    ships: Dict[str, BuildingInfoDict]
    research: Dict[str, BuildingInfoDict]
    lifeform_buildings: Dict[str, BuildingInfoDict]
    lifeform_research: Dict[str, BuildingInfoDict]
    queue: List[QueueItemDict]

class PlayerDict(TypedDict):
    name: str
    id: Optional[str]

class EmpireSnapshotDict(TypedDict):
    timestamp: str  # ISO8601
    planets: List[PlanetDict]

class StorageUpgradeCandidate(TypedDict):
    planet_id: str
    planet_name: str
    coordinates: str
    resource: str
    current: int
    max: int
    percent: float
    building_id: int
    building_level: int | str
    upgradable: bool

class UpgradableBuilding(TypedDict):
    planet_id: str
    planet_name: str
    coordinates: str
    resource: str
    building_id: int
    level: int

class UpgradableLifeformBuilding(TypedDict):
    planet_id: str
    planet_name: str
    coordinates: str
    building_id: int
    building: str
    level: int

