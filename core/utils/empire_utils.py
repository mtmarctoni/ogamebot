from typing import Optional
from config.types import EmpireSnapshotDict, PlanetDict, PlanetId

def get_target_planet(empire_data: EmpireSnapshotDict, planet_id: PlanetId) -> Optional[PlanetDict]:
    """
    Retrieves the planet object for 'Abyssal Nexus'.
    """
    for planet in empire_data.get("planets", []):
        if str(planet.get("id")) == planet_id:
            return planet
    return None