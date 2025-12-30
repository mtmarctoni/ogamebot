from constants.general import TechnologyTuple
from constants.resources import RESOURCE_TO_STORAGE


class buildings:
    metal_mine: TechnologyTuple = (1, 1, 'supplies')
    crystal_mine: TechnologyTuple = (2, 1, 'supplies')
    deuterium_mine: TechnologyTuple = (3, 1, 'supplies')
    solar_plant: TechnologyTuple = (4, 1, 'supplies')
    fusion_plant: TechnologyTuple = (12, 1, 'supplies')
    metal_storage: TechnologyTuple = (22, 1, 'supplies')
    crystal_storage: TechnologyTuple = (23, 1, 'supplies')
    deuterium_storage: TechnologyTuple = (24, 1, 'supplies')

    robotics_factory: TechnologyTuple = (14, 1, 'facilities')
    shipyard: TechnologyTuple = (21, 1, 'facilities')
    research_laboratory: TechnologyTuple = (31, 1, 'facilities')
    alliance_depot: TechnologyTuple = (34, 1, 'facilities')
    missile_silo: TechnologyTuple = (44, 1, 'facilities')
    nanite_factory: TechnologyTuple = (15, 1, 'facilities')
    terraformer: TechnologyTuple = (33, 1, 'facilities')
    repair_dock: TechnologyTuple = (36, 1, 'facilities')
    moon_base: TechnologyTuple = (41, 1, 'facilities')
    sensor_phalanx: TechnologyTuple = (42, 1, 'facilities')
    jump_gate: TechnologyTuple = (43, 1, 'facilities')

    @staticmethod
    def get_name(building_id: int) -> str | None:
        mapping = {
            1: 'Metal Mine',
            2: 'Crystal Mine',
            3: 'Deuterium Mine',
            4: 'Solar Plant',
            12: 'Fusion Reactor',
            22: 'Metal Storage',
            23: 'Crystal Storage',
            24: 'Deuterium Tank',
            14: 'Robotics Factory',
            21: 'Shipyard',
            31: 'Research Laboratory',
            34: 'Alliance Depot',
            44: 'Missile Silo',
            15: 'Nanite Factory',
            33: 'Terraformer',
            36: 'Repair Dock',
            41: 'Moon Base',
            42: 'Sensor Phalanx',
            43: 'Jump Gate',
        }
        return mapping.get(building_id)
    
    @staticmethod
    def get_building_id(resource_name: str) -> int | None:
        """
        Get the building ID for a given resource name (e.g., 'metal', 'crystal').
        """
        storage_class = RESOURCE_TO_STORAGE.get(resource_name)
        if not storage_class:
            return None  # Resource not found

        building = getattr(buildings, storage_class, None)
        if building:
            return building[0]  # Return the building ID (first element of the tuple)
        return None

    @staticmethod
    def solar_satellite(amount: int = 1) -> TechnologyTuple:
        return (212, amount, 'supplies')

    @staticmethod
    def crawler(amount: int = 1) -> TechnologyTuple:
        return (217, amount, 'supplies')

    @staticmethod
    def is_supplies(supplies: TechnologyTuple) -> bool:
        return supplies[2] == 'supplies'

    @staticmethod
    def is_facilities(facilities: TechnologyTuple) -> bool:
        return facilities[2] == 'facilities'

    @staticmethod
    def building_name(building: TechnologyTuple) -> str | None:
        mapping = {
            14: 'robotics_factory',
            21: 'shipyard',
            31: 'research_laboratory',
            34: 'alliance_depot',
            44: 'missile_silo',
            15: 'nanite_factory',
            33: 'terraformer',
            36: 'repair_dock',
            41: 'moon_base',
            42: 'sensor_phalanx',
            43: 'jump_gate',
            1: 'metal_mine',
            2: 'crystal_mine',
            3: 'deuterium_mine',
            4: 'solar_plant',
            12: 'fusion_plant',
            212: 'solar_satellite',
            217: 'crawler',
            22: 'metal_storage',
            23: 'crystal_storage',
            24: 'deuterium_storage',
        }
        return mapping.get(building[0])

    @staticmethod
    def rocket_launcher(amount: int = 1) -> TechnologyTuple:
        return (401, amount, 'defenses')

    @staticmethod
    def laser_cannon_light(amount: int = 1) -> TechnologyTuple:
        return (402, amount, 'defenses')

    @staticmethod
    def laser_cannon_heavy(amount: int = 1) -> TechnologyTuple:
        return (403, amount, 'defenses')

    @staticmethod
    def gauss_cannon(amount: int = 1) -> TechnologyTuple:
        return (404, amount, 'defenses')

    @staticmethod
    def ion_cannon(amount: int = 1) -> TechnologyTuple:
        return (405, amount, 'defenses')

    @staticmethod
    def plasma_cannon(amount: int = 1) -> TechnologyTuple:
        return (406, amount, 'defenses')

    @staticmethod
    def shield_dome_small(amount: int = 1) -> TechnologyTuple:
        return (407, amount, 'defenses')

    @staticmethod
    def shield_dome_large(amount: int = 1) -> TechnologyTuple:
        return (408, amount, 'defenses')

    @staticmethod
    def missile_interceptor(amount: int = 1) -> TechnologyTuple:
        return (502, amount, 'defenses')

    @staticmethod
    def missile_interplanetary(amount: int = 1) -> TechnologyTuple:
        return (503, amount, 'defenses')

    @staticmethod
    def is_defenses(defenses: TechnologyTuple) -> bool:
        return defenses[2] == 'defenses'

    @staticmethod
    def defense_name(defense: TechnologyTuple) -> str | None:
        if not buildings.is_defenses(defense):
            return None
        mapping = {
            401: 'rocket_launcher',
            402: 'laser_cannon_light',
            403: 'laser_cannon_heavy',
            404: 'gauss_cannon',
            405: 'ion_cannon',
            406: 'plasma_cannon',
            407: 'shield_dome_small',
            408: 'shield_dome_large',
            502: 'missile_interceptor',
            503: 'missile_interplanetary',
        }
        return mapping.get(defense[0])