from enum import Enum
from typing import Callable, List

from config.shared_types import PlanetDict, TechId, TechLevel

class Resources(Enum):
    METAL = 'metal'
    CRYSTAL = 'crystal'
    DEUTERIUM = 'deuterium'
    ENERGY = 'energy'
    FOOD = 'food'
    POPULATION = 'population'

class ResourceClass:

    _id_to_name_mapping = {
        "1": Resources.METAL,
        "2": Resources.CRYSTAL,
        "3": Resources.DEUTERIUM,
        "E": Resources.ENERGY,
        "F": Resources.FOOD,
        "P": Resources.POPULATION,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, resource_id: TechId) -> Resources:
        """
        Get the Resource name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if resource_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Resource ID: {resource_id}. No corresponding Resource found.")
        return cls._id_to_name_mapping[resource_id]
    
    @classmethod
    def get_id_by_name(cls, resource_name: Resources) -> TechId:
        """
        Get the Resource ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if resource_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Resource Name: {resource_name}. No corresponding ID found.")
        return TechId(cls._name_to_id_mapping[resource_name])
    
    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """
        Get all the Resource IDs in a type-safe way.
        """
        return [TechId(k) for k in cls._id_to_name_mapping.keys()]
    
    @classmethod
    def get_all_names(cls) -> List[Resources]:
        """
        Get all the Resource names in a type-safe way.
        """
        return list(cls._name_to_id_mapping.keys())

    @staticmethod
    def get_levels(planet: PlanetDict) -> tuple[TechLevel, TechLevel, TechLevel]:
        """
        Get the current levels of metal, crystal, and deuterium on the planet.
        Args:
            planet (dict): The planet data containing resource information.
        Returns:
            tuple[int, int, int]: A tuple containing the levels of metal, crystal, and deuterium respectively.
        """
        metal = TechLevel(planet["buildings"][ResourceClass.get_id_by_name(Resources.METAL)]["level"])
        crystal = TechLevel(planet["buildings"][ResourceClass.get_id_by_name(Resources.CRYSTAL)]["level"])
        deut = TechLevel(planet["buildings"][ResourceClass.get_id_by_name(Resources.DEUTERIUM)]["level"])
        return metal, crystal, deut


class ResourceStorage(Enum):
    METAL_STORAGE = 'metalStorage'
    CRYSTAL_STORAGE = 'crystalStorage'
    DEUTERIUM_TANK = 'deuteriumStorage'
    FOOD_STORAGE = 'foodStorage'
    POPULATION_STORAGE = 'populationStorage'

class ResourceStorageClass:

    _id_to_name_mapping = {
        "22": ResourceStorage.METAL_STORAGE,
        "23": ResourceStorage.CRYSTAL_STORAGE,
        "24": ResourceStorage.DEUTERIUM_TANK,
        "FS": ResourceStorage.FOOD_STORAGE,
        "PS": ResourceStorage.POPULATION_STORAGE,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, storage_id: str) -> ResourceStorage:
        """
        Get the Resource Storage name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if storage_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Resource Storage ID: {storage_id}. No corresponding Resource Storage found.")
        return cls._id_to_name_mapping[storage_id]
    
    @classmethod
    def get_id_by_name(cls, storage_name: ResourceStorage) -> str:
        """
        Get the Resource Storage ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if storage_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Resource Storage Name: {storage_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[storage_name]
    
    @classmethod
    def get_all_ids(cls) -> list[str]:
        """
        Get all the Resource Storage IDs in a type-safe way.
        """
        return list(cls._id_to_name_mapping.keys())
    
    @classmethod
    def get_all_names(cls) -> list[ResourceStorage]:
        """
        Get all the Resource Storage names in a type-safe way.
        """
        return list(cls._name_to_id_mapping.keys())
    
    @classmethod
    def get_levels(cls, planet: PlanetDict) -> tuple[TechLevel, TechLevel, TechLevel]:
        """
        Get the current levels of metal storage, crystal storage, deuterium tank,
        food storage, and population storage on the planet.
        Args:
            planet (dict): The planet data containing storage information.
        Returns:
            tuple[int, int, int, int, int]: A tuple containing the levels of metal storage,
            crystal storage, deuterium tank, food storage, and population storage respectively.
        """
        metal_storage = TechLevel(planet['buildings'][ResourceStorageClass.get_id_by_name(ResourceStorage.METAL_STORAGE)]['level'])
        crystal_storage = TechLevel(planet['buildings'][ResourceStorageClass.get_id_by_name(ResourceStorage.CRYSTAL_STORAGE)]['level'])
        deut_tank = TechLevel(planet['buildings'][ResourceStorageClass.get_id_by_name(ResourceStorage.DEUTERIUM_TANK)]['level'])
        return metal_storage, crystal_storage, deut_tank
    


RESOURCE_TO_STORAGE = {
    Resources.METAL.value: ResourceStorage.METAL_STORAGE.value,
    Resources.CRYSTAL.value: ResourceStorage.CRYSTAL_STORAGE.value,
    Resources.DEUTERIUM.value: ResourceStorage.DEUTERIUM_TANK.value,
    Resources.FOOD.value: ResourceStorage.FOOD_STORAGE.value,
    Resources.POPULATION.value: ResourceStorage.POPULATION_STORAGE.value,
}

# Energy consumption formulas for mines
ENERGY_CONSUMPTION: dict[str, Callable[[int], int]] = {
    Resources.METAL.value: lambda level: int(10 * level * (1.1 ** level)),
    Resources.CRYSTAL.value: lambda level: int(10 * level * (1.1 ** level)),
    Resources.DEUTERIUM.value: lambda level: int(20 * level * (1.1 ** level)),
}
