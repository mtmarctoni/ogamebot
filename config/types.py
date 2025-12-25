from typing import TypedDict, List, Dict, Optional

class ResourceDict(TypedDict, total=False):
    metal: int
    crystal: int
    deuterium: int
    energy: int
    food: int
    population: int

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
    resources: ResourceDict
    storage: Dict[str, int]
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

# Example usage:
# snapshot: EmpireSnapshotDict = {...}
# with open('empire_snapshot.json', 'w') as f:
#     import json
#     json.dump(snapshot, f, indent=2)
