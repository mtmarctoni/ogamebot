from typing import Optional
from config.types import EmpireSnapshotDict, PlanetDict, PlanetId

def get_target_planet(empire_data: EmpireSnapshotDict, planet_id: PlanetId) -> Optional[PlanetDict]:
    """
    Retrieves the planet object by planet_id from empire data.
    """
    for planet in empire_data["planets"]:
        if str(planet['id']) == planet_id:
            return planet
    return None