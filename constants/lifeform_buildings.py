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
        ]
    
    @classmethod
    def get_name_by_id(cls, building_id: int) -> str | None:
        mapping = {
            11101: cls.Residential_Sector,
            11102: cls.Research_Center,
            11103: cls.Academy,
            11104: cls.Food_Processor,
            11105: cls.Water_Treatment,
            11106: cls.Communications_Array,
            11107: cls.Planetary_Shield,
            11108: cls.Spaceport,
            11109: cls.Trade_Hub,
            11110: cls.Defense_Grid,
            11111: cls.Energy_Generator,
            11112: cls.Biodome,
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
            cls.Research_Center: 11102,
            cls.Academy: 11103,
            cls.Food_Processor: 11104,
            cls.Water_Treatment: 11105,
            cls.Communications_Array: 11106,
            cls.Planetary_Shield: 11107,
            cls.Spaceport: 11108,
            cls.Trade_Hub: 11109,
            cls.Defense_Grid: 11110,
            cls.Energy_Generator: 11111,
            cls.Biodome: 11112,
        }
        return mapping.get(building_name)

HumanLifeformBuilding = Literal[
    *[value for value in vars(HumanLifeformBuildingClass).values() if isinstance(value, str)]
]