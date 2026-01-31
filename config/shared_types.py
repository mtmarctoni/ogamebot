from typing import NewType, TypedDict, Optional, List, Dict

# Shared type aliases
TechId = NewType('TechId', str)
PlanetId = NewType('PlanetId', str)
PlanetName = NewType('PlanetName', str)
TechName = NewType('TechName', str)
TechLevel = NewType('TechLevel', int)
StringCoords = NewType('StringCoords', str)

# --- Core Data Structures Used Across Modules ---
class QueueItemDict(TypedDict, total=True):
    type: str  # building, research, shipyard
    name: str
    level: Optional[int]
    count: Optional[int]
    finish_time: Optional[str]

class TechInfoDict(TypedDict, total=True):
    level: int
    upgradable: bool
    upgrade_js: Optional[str]

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
