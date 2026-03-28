from enum import Enum
from typing import Dict, List

from config.shared_types import TechId


class Defense(Enum):
    ROCKET_LAUNCHER = "rocketLauncher"
    LIGHT_LASER = "lightLaser"
    HEAVY_LASER = "heavyLaser"
    GAUSS_CANNON = "gaussCannon"
    ION_CANNON = "ionCannon"
    PLASMA_TURRET = "plasmaTurret"
    SMALL_SHIELD_DOME = "smallShieldDome"
    LARGE_SHIELD_DOME = "largeShieldDome"
    ANTI_BALLISTIC_MISSILES = "antiBallisticMissiles"
    INTERPLANETARY_MISSILES = "interplanetaryMissiles"


class Defenses:
    _id_to_name_mapping: Dict[TechId, Defense] = {
        TechId("401"): Defense.ROCKET_LAUNCHER,
        TechId("402"): Defense.LIGHT_LASER,
        TechId("403"): Defense.HEAVY_LASER,
        TechId("404"): Defense.GAUSS_CANNON,
        TechId("405"): Defense.ION_CANNON,
        TechId("406"): Defense.PLASMA_TURRET,
        TechId("407"): Defense.SMALL_SHIELD_DOME,
        TechId("408"): Defense.LARGE_SHIELD_DOME,
        TechId("502"): Defense.ANTI_BALLISTIC_MISSILES,
        TechId("503"): Defense.INTERPLANETARY_MISSILES,
    }

    _name_to_id_mapping: Dict[Defense, TechId] = {v: k for k, v in _id_to_name_mapping.items()}

    _costs_by_id: Dict[TechId, Dict[str, int]] = {
        TechId("401"): {"metal": 2000, "crystal": 0, "deuterium": 0},
        TechId("402"): {"metal": 1500, "crystal": 500, "deuterium": 0},
        TechId("403"): {"metal": 6000, "crystal": 2000, "deuterium": 0},
        TechId("404"): {"metal": 20000, "crystal": 15000, "deuterium": 2000},
        TechId("405"): {"metal": 2000, "crystal": 6000, "deuterium": 0},
        TechId("406"): {"metal": 50000, "crystal": 50000, "deuterium": 30000},
        TechId("407"): {"metal": 10000, "crystal": 10000, "deuterium": 0},
        TechId("408"): {"metal": 50000, "crystal": 50000, "deuterium": 0},
        TechId("502"): {"metal": 8000, "crystal": 2000, "deuterium": 1000},
        TechId("503"): {"metal": 12500, "crystal": 2500, "deuterium": 10000},
    }

    REPEATABLE_DEFENSE_IDS: List[TechId] = [
        TechId("401"),
        TechId("402"),
        TechId("403"),
        TechId("404"),
        TechId("405"),
        TechId("406"),
        TechId("502"),
        TechId("503"),
    ]

    NON_REPEATABLE_DEFENSE_IDS: List[TechId] = [TechId("407"), TechId("408")]

    @classmethod
    def get_name_by_id(cls, defense_id: TechId) -> Defense:
        if defense_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Defense ID: {defense_id}. No corresponding Defense found.")
        return cls._id_to_name_mapping[defense_id]

    @classmethod
    def get_id_by_name(cls, defense_name: Defense) -> TechId:
        if defense_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Defense: {defense_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[defense_name]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        return list(cls._id_to_name_mapping.keys())

    @classmethod
    def get_repeatable_ids(cls) -> List[TechId]:
        return list(cls.REPEATABLE_DEFENSE_IDS)

    @classmethod
    def get_costs_by_id(cls, defense_id: TechId) -> Dict[str, int]:
        if defense_id not in cls._costs_by_id:
            raise ValueError(f"Invalid Defense ID: {defense_id}. No corresponding costs found.")
        return dict(cls._costs_by_id[defense_id])

    @classmethod
    def is_repeatable(cls, defense_id: TechId) -> bool:
        return defense_id in cls.REPEATABLE_DEFENSE_IDS

    @classmethod
    def is_non_repeatable(cls, defense_id: TechId) -> bool:
        return defense_id in cls.NON_REPEATABLE_DEFENSE_IDS
