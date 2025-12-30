from enum import Enum

from config.types import TechId

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