from typing import Callable

from config.types import PlanetDict, TechLevel

class ResourceClass:
    metal = 'metal'
    crystal = 'crystal'
    deuterium = 'deuterium'
    energy = 'energy'
    food = 'food'
    population = 'population'

    @classmethod
    def allResources(cls) -> list[str]:
        return [
            cls.metal,
            cls.crystal,
            cls.deuterium,
            cls.energy,
            cls.food,
            cls.population,
        ]
    
    @staticmethod
    def get_levels(planet: PlanetDict) -> tuple[TechLevel, TechLevel, TechLevel]:
        """
        Get the current levels of metal, crystal, and deuterium on the planet.
        Args:
            planet (dict): The planet data containing resource information.
        Returns:
            tuple[int, int, int]: A tuple containing the levels of metal, crystal, and deuterium respectively.
        """
        metal = TechLevel(planet.get('buildings', {})["1"].get('level', 0))
        crystal = TechLevel(planet.get('buildings', {})["2"].get('level', 0))
        deut = TechLevel(planet.get('buildings', {})["3"].get('level', 0))
        return metal, crystal, deut

class ResourceStorageClass:
    metal_storage = 'metalStorage'
    crystal_storage = 'crystalStorage'
    deuterium_storage = 'deuteriumStorage'
    food_storage = 'foodStorage'
    population_storage = 'populationStorage'

    @classmethod
    def allStorages(cls) -> list[str]:
        return [
            cls.metal_storage,
            cls.crystal_storage,
            cls.deuterium_storage,
            cls.food_storage,
            cls.population_storage,
        ]

RESOURCE_TO_STORAGE = {
    ResourceClass.metal: ResourceStorageClass.metal_storage,
    ResourceClass.crystal: ResourceStorageClass.crystal_storage,
    ResourceClass.deuterium: ResourceStorageClass.deuterium_storage,
    ResourceClass.food: ResourceStorageClass.food_storage,
    ResourceClass.population: ResourceStorageClass.population_storage,
}

# Energy consumption formulas for mines
ENERGY_CONSUMPTION: dict[str, Callable[[int], int]] = {
    ResourceClass.metal: lambda level: int(10 * level * (1.1 ** level)),
    ResourceClass.crystal: lambda level: int(10 * level * (1.1 ** level)),
    ResourceClass.deuterium: lambda level: int(20 * level * (1.1 ** level)),
}

# Resource upgrade preference
RESOURCE_UPGRADE_PREFERENCE = [ResourceClass.crystal, ResourceClass.deuterium, ResourceClass.metal]