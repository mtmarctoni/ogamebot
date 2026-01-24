from enum import Enum

class HumanLifeformBuilding(Enum):
    RESIDENTIAL_SECTOR = 'residential_sector'
    RESEARCH_CENTER = 'research_center'
    ACADEMY = 'academy'
    FOOD_PROCESSOR = 'food_processor'
    WATER_TREATMENT = 'water_treatment'
    COMMUNICATIONS_ARRAY = 'communications_array'
    PLANETARY_SHIELD = 'planetary_shield'
    SPACEPORT = 'spaceport'
    TRADE_HUB = 'trade_hub'
    DEFENSE_GRID = 'defense_grid'
    ENERGY_GENERATOR = 'energy_generator'
    BIODOME = 'biodome'
    BIOSPHERE_FARM = 'biosphere_farm'
    ACADEMY_OF_SCIENCES = 'academy_of_sciences'
    NEURO_CALIBRATION_CENTER = 'neuro_calibration_center'
    HIGH_ENERGY_SMELTING = 'high_energy_smelting'
    FOOD_SILO = 'food_silo'
    FUSION_POWERED_PRODUCTION = 'fusion_powered_production'
    SKYSCRAPER = 'skyscraper'
    BIOTECH_LAB = 'biotech_lab'
    METROPOLIS = 'metropolis'

class HumanLifeformBuildingClass:
    """
    Utility class for mapping Human lifeform building IDs to names and back.
    Names are preserved exactly as in game/canonical source, and IDs are strings.
    """
    _id_to_enum_mapping = {
        "11101": HumanLifeformBuilding.RESIDENTIAL_SECTOR,
        "11102": HumanLifeformBuilding.BIOSPHERE_FARM,
        "11103": HumanLifeformBuilding.RESEARCH_CENTER,
        "11104": HumanLifeformBuilding.ACADEMY_OF_SCIENCES,
        "11105": HumanLifeformBuilding.NEURO_CALIBRATION_CENTER,
        "11106": HumanLifeformBuilding.HIGH_ENERGY_SMELTING,
        "11107": HumanLifeformBuilding.FOOD_SILO,
        "11108": HumanLifeformBuilding.FUSION_POWERED_PRODUCTION,
        "11109": HumanLifeformBuilding.SKYSCRAPER,
        "11110": HumanLifeformBuilding.BIOTECH_LAB,
        "11111": HumanLifeformBuilding.METROPOLIS,
        "11112": HumanLifeformBuilding.PLANETARY_SHIELD,
    }

    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}

    @classmethod
    def get_name_by_id(cls, building_id: str) -> HumanLifeformBuilding:
        """
        Look up Human building Enum by string ID. Example: '11101' → HumanLifeformBuilding.residential_sector
        Raises ValueError if not found.
        """
        if building_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Human building ID: {building_id}.")
        return cls._id_to_enum_mapping[building_id]

    @classmethod
    def get_id_by_name(cls, building: HumanLifeformBuilding) -> str:
        """
        Look up Human building string ID by Enum member. Example: HumanLifeformBuilding.residential_sector → '11101'
        Raises ValueError if not found.
        """
        if building not in cls._enum_to_id_mapping:
            raise ValueError(f"Invalid Human building enum: {building}.")
        return cls._enum_to_id_mapping[building]

    @classmethod
    def get_all_ids(cls) -> list[str]:
        """Return all valid Human building string IDs."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> list[HumanLifeformBuilding]:
        """Return all valid Human building Enum names."""
        return list(cls._enum_to_id_mapping.keys())


class KaeleshLifeformBuilding(Enum):
    SANCTUARY = 'sanctuary'
    ANTIMATTER_CONDENSER = 'antimatter_condenser'
    VORTEX_CHAMBER = 'vortex_chamber'
    HALLS_OF_REALIZATION = 'halls_of_realization'
    FORUM_OF_TRANSCENDENCE = 'forum_of_transcendence'
    ANTIMATTER_CONVECTOR = 'antimatter_convector'
    CLONING_LABORATORY = 'cloning_laboratory'
    CHRYSALIS_ACCELERATOR = 'chrysalis_accelerator'
    BIO_MODIFIER = 'bio_modifier'
    PSIONIC_MODULATOR = 'psionic_modulator'
    SHIP_MANUFACTURING_HALL = 'ship_manufacturing_hall'
    SUPRA_REFRACTOR = 'supra_refractor'

class KaeleshLifeformBuildingClass:
    """
    Utility class for mapping Kaelesh lifeform building IDs to names and back.
    Names are preserved exactly as in game/canonical source, and IDs are strings.
    """
    _id_to_enum_mapping = {
        "14101": KaeleshLifeformBuilding.SANCTUARY,
        "14102": KaeleshLifeformBuilding.ANTIMATTER_CONDENSER,
        "14103": KaeleshLifeformBuilding.VORTEX_CHAMBER,
        "14104": KaeleshLifeformBuilding.HALLS_OF_REALIZATION,
        "14105": KaeleshLifeformBuilding.FORUM_OF_TRANSCENDENCE,
        "14106": KaeleshLifeformBuilding.ANTIMATTER_CONVECTOR,
        "14107": KaeleshLifeformBuilding.CLONING_LABORATORY,
        "14108": KaeleshLifeformBuilding.CHRYSALIS_ACCELERATOR,
        "14109": KaeleshLifeformBuilding.BIO_MODIFIER,
        "14110": KaeleshLifeformBuilding.PSIONIC_MODULATOR,
        "14111": KaeleshLifeformBuilding.SHIP_MANUFACTURING_HALL,
        "14112": KaeleshLifeformBuilding.SUPRA_REFRACTOR,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}

    @classmethod
    def get_name_by_id(cls, building_id: str) -> KaeleshLifeformBuilding:
        """
        Look up Kaelesh building Enum by string ID. Example: '14101' → KaeleshLifeformBuilding.sanctuary
        Raises ValueError if not found.
        """
        if building_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Kaelesh building ID: {building_id}.")
        return cls._id_to_enum_mapping[building_id]

    @classmethod
    def get_id_by_name(cls, building: KaeleshLifeformBuilding) -> str:
        """
        Look up Kaelesh building string ID by Enum member. Example: KaeleshLifeformBuilding.sanctuary → '14101'
        Raises ValueError if not found.
        """
        if building not in cls._enum_to_id_mapping:
            raise ValueError(f"Invalid Kaelesh building enum: {building}.")
        return cls._enum_to_id_mapping[building]

    @classmethod
    def get_all_ids(cls) -> list[str]:
        """Return all valid Kaelesh building string IDs."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> list[KaeleshLifeformBuilding]:
        """Return all valid Kaelesh building Enum names."""
        return list(cls._enum_to_id_mapping.keys())


class MechaLifeformBuilding(Enum):
    ASSEMBLY_LINE = 'assembly_line'
    FUSION_CELL_FACTORY = 'fusion_cell_factory'
    ROBOTICS_RESEARCH_CENTRE = 'robotics_research_centre'
    UPDATE_NETWORK = 'update_network'
    QUANTUM_COMPUTER_CENTRE = 'quantum_computer_centre'
    AUTOMATISED_ASSEMBLY_CENTRE = 'automatised_assembly_centre'
    HIGH_PERFORMANCE_TRANSFORMER = 'high_performance_transformer'
    MICROCHIP_ASSEMBLY_LINE = 'microchip_assembly_line'
    PRODUCTION_ASSEMBLY_HALL = 'production_assembly_hall'
    HIGH_PERFORMANCE_SYNTHESISER = 'high_performance_synthesiser'
    CHIP_MASS_PRODUCTION = 'chip_mass_production'
    NANO_REPAIR_BOTS = 'nano_repair_bots'

class MechaLifeformBuildingClass:
    """
    Utility class for mapping Mecha lifeform building IDs to names and back.
    Names are preserved exactly as in game/canonical source, and IDs are strings.
    """
    _id_to_enum_mapping = {
        "13101": MechaLifeformBuilding.ASSEMBLY_LINE,
        "13102": MechaLifeformBuilding.FUSION_CELL_FACTORY,
        "13103": MechaLifeformBuilding.ROBOTICS_RESEARCH_CENTRE,
        "13104": MechaLifeformBuilding.UPDATE_NETWORK,
        "13105": MechaLifeformBuilding.QUANTUM_COMPUTER_CENTRE,
        "13106": MechaLifeformBuilding.AUTOMATISED_ASSEMBLY_CENTRE,
        "13107": MechaLifeformBuilding.HIGH_PERFORMANCE_TRANSFORMER,
        "13108": MechaLifeformBuilding.MICROCHIP_ASSEMBLY_LINE,
        "13109": MechaLifeformBuilding.PRODUCTION_ASSEMBLY_HALL,
        "13110": MechaLifeformBuilding.HIGH_PERFORMANCE_SYNTHESISER,
        "13111": MechaLifeformBuilding.CHIP_MASS_PRODUCTION,
        "13112": MechaLifeformBuilding.NANO_REPAIR_BOTS,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}

    @classmethod
    def get_name_by_id(cls, building_id: str) -> MechaLifeformBuilding:
        """
        Look up Mecha building Enum by string ID. Example: '13101' → MechaLifeformBuilding.assembly_line
        Raises ValueError if not found.
        """
        if building_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Mecha building ID: {building_id}.")
        return cls._id_to_enum_mapping[building_id]

    @classmethod
    def get_id_by_name(cls, building: MechaLifeformBuilding) -> str:
        """
        Look up Mecha building string ID by Enum member. Example: MechaLifeformBuilding.assembly_line → '13101'
        Raises ValueError if not found.
        """
        if building not in cls._enum_to_id_mapping:
            raise ValueError(f"Invalid Mecha building enum: {building}.")
        return cls._enum_to_id_mapping[building]

    @classmethod
    def get_all_ids(cls) -> list[str]:
        """Return all valid Mecha building string IDs."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> list[MechaLifeformBuilding]:
        """Return all valid Mecha building Enum names."""
        return list(cls._enum_to_id_mapping.keys())


class RocktalLifeformBuilding(Enum):
    MEDITATION_ENCLAVE = 'meditation_enclave'
    CRYSTAL_FARM = 'crystal_farm'
    RUNE_TECHNOLOGIUM = 'rune_technologium'
    ORIKTORIUM = 'oriktorium'
    MAGMA_FORGE = 'magma_forge'
    DISRUPTION_CHAMBER = 'disruption_chamber'
    METROPOLIS = 'metropolis'
    ROCKTAL_COLLECTOR = 'rocktal_collector'
    CRYSTAL_REFINERY = 'crystal_refinery'
    DEUTERIUM_FURNACE = 'deuterium_furnace'
    MEGALITH = 'megalith'
    FORUM_OF_TRANSCENDENCE = 'forum_of_transcendence'

class RocktalLifeformBuildingClass:
    """
    Utility class for mapping Rocktal lifeform building IDs to names and back.
    Names are preserved exactly as in game/canonical source, and IDs are strings.
    """
    _id_to_enum_mapping = {
        "12101": RocktalLifeformBuilding.MEDITATION_ENCLAVE,
        "12102": RocktalLifeformBuilding.CRYSTAL_FARM,
        "12103": RocktalLifeformBuilding.RUNE_TECHNOLOGIUM,
        "12104": RocktalLifeformBuilding.ORIKTORIUM,
        "12105": RocktalLifeformBuilding.MAGMA_FORGE,
        "12106": RocktalLifeformBuilding.DISRUPTION_CHAMBER,
        "12107": RocktalLifeformBuilding.METROPOLIS,
        "12108": RocktalLifeformBuilding.ROCKTAL_COLLECTOR,
        "12109": RocktalLifeformBuilding.CRYSTAL_REFINERY,
        "12110": RocktalLifeformBuilding.DEUTERIUM_FURNACE,
        "12111": RocktalLifeformBuilding.MEGALITH,
        "12112": RocktalLifeformBuilding.FORUM_OF_TRANSCENDENCE,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}

    @classmethod
    def get_name_by_id(cls, building_id: str) -> RocktalLifeformBuilding:
        """
        Look up Rocktal building Enum by string ID. Example: '12101' → RocktalLifeformBuilding.meditation_enclave
        Raises ValueError if not found.
        """
        if building_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Rocktal building ID: {building_id}.")
        return cls._id_to_enum_mapping[building_id]

    @classmethod
    def get_id_by_name(cls, building: RocktalLifeformBuilding) -> str:
        """
        Look up Rocktal building string ID by Enum member. Example: RocktalLifeformBuilding.meditation_enclave → '12101'
        Raises ValueError if not found.
        """
        if building not in cls._enum_to_id_mapping:
            raise ValueError(f"Invalid Rocktal building enum: {building}.")
        return cls._enum_to_id_mapping[building]

    @classmethod
    def get_all_ids(cls) -> list[str]:
        """Return all valid Rocktal building string IDs."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> list[RocktalLifeformBuilding]:
        """Return all valid Rocktal building Enum names."""
        return list(cls._enum_to_id_mapping.keys())
