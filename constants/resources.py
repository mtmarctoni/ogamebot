from typing import Callable

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