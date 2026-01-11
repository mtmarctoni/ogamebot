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

class KaeleshLifeformBuildingClass:
    Sanctuary = 'sanctuary'
    Antimatter_Condenser = 'antimatter_condenser'
    Vortex_Chamber = 'vortex_chamber'
    Halls_of_Realization = 'halls_of_realization'
    Forum_of_Transcendence = 'forum_of_transcendence'
    Antimatter_Convector = 'antimatter_convector'
    Cloning_Laboratory = 'cloning_laboratory'
    Chrysalis_Accelerator = 'chrysalis_accelerator'
    Bio_Modifier = 'bio_modifier'
    Psionic_Modulator = 'psionic_modulator'
    Ship_Manufacturing_Hall = 'ship_manufacturing_hall'
    Supra_Refractor = 'supra_refractor'

    @classmethod
    def allBuildings(cls) -> list[str]:
        return [
            cls.Sanctuary,
            cls.Antimatter_Condenser,
            cls.Vortex_Chamber,
            cls.Halls_of_Realization,
            cls.Forum_of_Transcendence,
            cls.Antimatter_Convector,
            cls.Cloning_Laboratory,
            cls.Chrysalis_Accelerator,
            cls.Bio_Modifier,
            cls.Psionic_Modulator,
            cls.Ship_Manufacturing_Hall,
            cls.Supra_Refractor
        ]

    @classmethod
    def getBuildingById(cls, building_id: str) -> str:
        """
        Returns the building name corresponding to the given building ID.
        """
        mapping = {
            '14101': cls.Sanctuary,
            '14102': cls.Antimatter_Condenser,
            '14103': cls.Vortex_Chamber,
            '14104': cls.Halls_of_Realization,
            '14105': cls.Forum_of_Transcendence,
            '14106': cls.Antimatter_Convector,
            '14107': cls.Cloning_Laboratory,
            '14108': cls.Chrysalis_Accelerator,
            '14109': cls.Bio_Modifier,
            '14110': cls.Psionic_Modulator,
            '14111': cls.Ship_Manufacturing_Hall,
            '14112': cls.Supra_Refractor
        }
        return mapping.get(building_id, "Unknown Building")

    @classmethod
    def getBuildingId(cls, building_name: str) -> str:
        """
        Returns the building ID corresponding to the given building name.
        """
        mapping = {
            cls.Sanctuary: '14101',
            cls.Antimatter_Condenser: '14102',
            cls.Vortex_Chamber: '14103',
            cls.Halls_of_Realization: '14104',
            cls.Forum_of_Transcendence: '14105',
            cls.Antimatter_Convector: '14106',
            cls.Cloning_Laboratory: '14107',
            cls.Chrysalis_Accelerator: '14108',
            cls.Bio_Modifier: '14109',
            cls.Psionic_Modulator: '14110',
            cls.Ship_Manufacturing_Hall: '14111',
            cls.Supra_Refractor: '14112'
        }
        return mapping.get(building_name, "Unknown ID")

    @classmethod
    def is_kaelesh(cls, building_id: str) -> bool:
        """
        Checks if the given building ID belongs to the Kaelesh lifeform.
        """
        kaelesh_building_ids = {
            '14101', '14102', '14103', '14104', '14105', '14106',
            '14107', '14108', '14109', '14110', '14111', '14112'
        }
        return building_id in kaelesh_building_ids
    
KaeleshLifeformBuilding = Literal[
    *[value for value in vars(KaeleshLifeformBuildingClass).values() if isinstance(value, str)]
]