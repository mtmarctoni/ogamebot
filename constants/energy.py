from enum import Enum
from typing import List

from config.types import PlanetDict, TechId, TechLevel

class EnergyBuilding(Enum):
    SOLAR_PLANT = "solarPlant"
    FUSION_PLANT = "fusionPlant"

class EnergyBuildings:
    """
    A utility class to map between EnergyBuilding names and their corresponding IDs.
    Ensures that only EnergyBuilding types are used.
    """

    _id_to_name_mapping = {
        "4": EnergyBuilding.SOLAR_PLANT,
        "12": EnergyBuilding.FUSION_PLANT,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, building_id: TechId) -> EnergyBuilding:
        """
        Get the EnergyBuilding name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if building_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid TechId: {building_id}. No corresponding EnergyBuilding found.")
        return cls._id_to_name_mapping[building_id]

    @classmethod
    def get_id_by_name(cls, building_name: EnergyBuilding) -> TechId:
        """
        Get the TechId by its EnergyBuilding name.
        Raises a ValueError if the name is invalid.
        """
        if building_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid EnergyBuilding: {building_name}. No corresponding TechId found.")
        return TechId(cls._name_to_id_mapping[building_name])
    
    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """
        Get all the EnergyBuilding TechIds in a type-safe way.
        """
        return [TechId(k) for k in cls._id_to_name_mapping.keys()]
    
    @classmethod
    def get_all_names(cls) -> List[EnergyBuilding]:
        """
        Get all the EnergyBuilding names in a type-safe way.
        """
        return list(cls._name_to_id_mapping.keys())
    
    @classmethod
    def get_levels(cls, planet: PlanetDict) -> tuple[TechLevel, TechLevel]:
        """
        Get the levels of all energy buildings on a planet.

        Args:
            planet (dict): The planet data containing building levels.

        Returns:
            tuple: A tuple containing levels of (solar_plant_level, fusion_plant_level).
        """
        solar_plant_id = cls.get_id_by_name(EnergyBuilding.SOLAR_PLANT)
        fusion_plant_id = cls.get_id_by_name(EnergyBuilding.FUSION_PLANT)

        solar_plant_level = TechLevel(planet["buildings"][solar_plant_id]["level"])
        fusion_plant_level = TechLevel(planet["buildings"][fusion_plant_id]["level"])

        return (solar_plant_level, fusion_plant_level)