from typing_extensions import Literal


class HumanLifeformBuildingClass:
    Residential_Sector = 'residential_sector'
    Research_Center = 'research_center'
    Academy = 'academy'
    Food_Processor = 'food_processor'
    Water_Treatment = 'water_treatment'
    Communications_Array = 'communications_array'
    Planetary_Shield = 'planetary_shield'
    Spaceport = 'spaceport'
    Trade_Hub = 'trade_hub'
    Defense_Grid = 'defense_grid'
    Energy_Generator = 'energy_generator'
    Biodome = 'biodome'
    Biosphere_Farm = 'biosphere_farm'
    Academy_of_Sciences = 'academy_of_sciences'
    Neuro_Calibration_Center = 'neuro_calibration_center'
    High_Energy_Smelting = 'high_energy_smelting'
    Food_Silo = 'food_silo'
    Fusion_Powered_Production = 'fusion_powered_production'
    Skyscraper = 'skyscraper'
    Biotech_Lab = 'biotech_lab'
    Metropolis = 'metropolis'

    @classmethod
    def allBuildings(cls) -> list[str]:
        return [
            cls.Residential_Sector,
            cls.Research_Center,
            cls.Academy,
            cls.Food_Processor,
            cls.Water_Treatment,
            cls.Communications_Array,
            cls.Planetary_Shield,
            cls.Spaceport,
            cls.Trade_Hub,
            cls.Defense_Grid,
            cls.Energy_Generator,
            cls.Biodome,
            cls.Biosphere_Farm,
            cls.Academy_of_Sciences,
            cls.Neuro_Calibration_Center,
            cls.High_Energy_Smelting,
            cls.Food_Silo,
            cls.Fusion_Powered_Production,
            cls.Skyscraper,
            cls.Biotech_Lab,
            cls.Metropolis,
        ]

    @classmethod
    def get_name_by_id(cls, building_id: int) -> str | None:
        mapping = {
            11101: cls.Residential_Sector,
            11102: cls.Biosphere_Farm,
            11103: cls.Research_Center,
            11104: cls.Academy_of_Sciences,
            11105: cls.Neuro_Calibration_Center,
            11106: cls.High_Energy_Smelting,
            11107: cls.Food_Silo,
            11108: cls.Fusion_Powered_Production,
            11109: cls.Skyscraper,
            11110: cls.Biotech_Lab,
            11111: cls.Metropolis,
            11112: cls.Planetary_Shield,
        }
        return mapping.get(building_id)

    @classmethod
    def is_human_building(cls, building_id: int) -> bool:
        return building_id in {
            11101, 11102, 11103, 11104, 11105, 11106,
            11107, 11108, 11109, 11110, 11111, 11112
        }

    @classmethod
    def get_id_by_name(cls, building_name: str) -> int | None:
        mapping = {
            cls.Residential_Sector: 11101,
            cls.Biosphere_Farm: 11102,
            cls.Research_Center: 11103,
            cls.Academy_of_Sciences: 11104,
            cls.Neuro_Calibration_Center: 11105,
            cls.High_Energy_Smelting: 11106,
            cls.Food_Silo: 11107,
            cls.Fusion_Powered_Production: 11108,
            cls.Skyscraper: 11109,
            cls.Biotech_Lab: 11110,
            cls.Metropolis: 11111,
            cls.Planetary_Shield: 11112,
        }
        return mapping.get(building_name)

HumanLifeformBuilding = Literal[
    *[value for value in vars(HumanLifeformBuildingClass).values() if isinstance(value, str)]
]