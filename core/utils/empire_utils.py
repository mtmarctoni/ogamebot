from typing import Optional
from config.types import EmpireSnapshotDict, PlanetDict, PlanetId

def get_target_planet(empire_data: EmpireSnapshotDict, planet_id: PlanetId) -> Optional[PlanetDict]:
    """
    Retrieves the planet object for 'Abyssal Nexus'.
    """
    print(f"[DEBUG] get_target_planet: Looking for planet_id={planet_id} (type: {type(planet_id)})")
    
    for planet in empire_data['planets']:
        pid = str(planet['id'])
        print(f"[DEBUG] Checking planet: {planet['name']} - ID={pid} (type: {type(pid)})")
        if pid == planet_id:
            print(f"[DEBUG] MATCH FOUND: {planet['name']}")
            return planet
    
    print(f"[DEBUG] NO MATCH: planet_id '{planet_id}' not found in empire data")
    return None