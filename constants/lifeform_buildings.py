from enum import Enum
from typing import Union, List

from config.shared_types import TechId, TechName

class HumanLifeformBuilding(Enum):
    RESIDENTIAL_SECTOR = 'residential_sector'
    BIOSPHERE_FARM = 'biosphere_farm'
    RESEARCH_CENTER = 'research_center'
    ACADEMY_OF_SCIENCES = 'academy_of_sciences'
    NEURO_CALIBRATION_CENTER = 'neuro_calibration_center'
    HIGH_ENERGY_SMELTING = 'high_energy_smelting'
    FOOD_SILO = 'food_silo'
    FUSION_POWERED_PRODUCTION = 'fusion_powered_production'
    SKYSCRAPER = 'skyscraper'
    BIOTECH_LAB = 'biotech_lab'
    METROPOLIS = 'metropolis'
    PLANETARY_SHIELD = 'planetary_shield'


class HumanLifeformBuildingClass:
    """
    Type-safe utility for Human lifeform buildings.
    All mapping methods accept both str and LifeformBuildingId/LifeformBuildingName for ergonomics.
    Returns strongly typed objects.
    """
    _id_to_enum_mapping = {
        TechId("11101"): HumanLifeformBuilding.RESIDENTIAL_SECTOR,
        TechId("11102"): HumanLifeformBuilding.BIOSPHERE_FARM,
        TechId("11103"): HumanLifeformBuilding.RESEARCH_CENTER,
        TechId("11104"): HumanLifeformBuilding.ACADEMY_OF_SCIENCES,
        TechId("11105"): HumanLifeformBuilding.NEURO_CALIBRATION_CENTER,
        TechId("11106"): HumanLifeformBuilding.HIGH_ENERGY_SMELTING,
        TechId("11107"): HumanLifeformBuilding.FOOD_SILO,
        TechId("11108"): HumanLifeformBuilding.FUSION_POWERED_PRODUCTION,
        TechId("11109"): HumanLifeformBuilding.SKYSCRAPER,
        TechId("11110"): HumanLifeformBuilding.BIOTECH_LAB,
        TechId("11111"): HumanLifeformBuilding.METROPOLIS,
        TechId("11112"): HumanLifeformBuilding.PLANETARY_SHIELD,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}
    _name_to_enum_mapping = {TechName(e.name): e for e in HumanLifeformBuilding}

    @classmethod
    def get_name_by_id(cls, building_id: Union[str, TechId]) -> TechName:
        """
        Get Human building name by its ID.
        Accepts str or TechId, returns TechName.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Human building ID: {building_id}.")
        return TechName(cls._id_to_enum_mapping[typed_id].name)

    @classmethod
    def get_id_by_name(cls, building_name: Union[str, TechName]) -> TechId:
        """
        Get Human building ID by its name.
        Accepts str or TechName, returns TechId.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Human building name: {building_name}.")
        enum = cls._name_to_enum_mapping[typed_name]
        return cls._enum_to_id_mapping[enum]

    @classmethod
    def get_enum_by_id(cls, building_id: Union[str, TechId]) -> HumanLifeformBuilding:
        """
        Get Enum by building ID (internal/advanced).
        Accepts str or TechId.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Human building ID: {building_id}.")
        return cls._id_to_enum_mapping[typed_id]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """Return all Human building IDs as TechId objects."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> List[TechName]:
        """Return all Human building names as TechName objects."""
        return [TechName(e.name) for e in HumanLifeformBuilding]

    @classmethod
    def get_enum_by_name(cls, building_name: Union[str, TechName]) -> HumanLifeformBuilding:
        """
        Get Enum by building name (internal/advanced).
        Accepts str or TechName.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Human building name: {building_name}.")
        return cls._name_to_enum_mapping[typed_name]

    @classmethod
    def get_name_by_value(cls, value: str) -> str:
        """
        Given a building 'value', return its Enum 'name'.
        """
        for member in HumanLifeformBuilding:
            if member.value == value:
                return member.name
        raise ValueError(f"Value '{value}' not found in HumanLifeformBuilding.")

    @classmethod
    def get_value_by_name(cls, name: str) -> str:
        """
        Given a building Enum 'name', return its 'value'.
        """
        try:
            return HumanLifeformBuilding[name].value
        except KeyError:
            raise ValueError(f"Name '{name}' not found in HumanLifeformBuilding.")


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

from config.shared_types import TechId, TechName
from typing import Union, List

class KaeleshLifeformBuildingClass:
    """
    Type-safe utility for Kaelesh lifeform buildings.
    All mapping methods accept both str and TechId/TechName for ergonomics.
    Returns strongly typed objects.
    """
    _id_to_enum_mapping = {
        TechId("14101"): KaeleshLifeformBuilding.SANCTUARY,
        TechId("14102"): KaeleshLifeformBuilding.ANTIMATTER_CONDENSER,
        TechId("14103"): KaeleshLifeformBuilding.VORTEX_CHAMBER,
        TechId("14104"): KaeleshLifeformBuilding.HALLS_OF_REALIZATION,
        TechId("14105"): KaeleshLifeformBuilding.FORUM_OF_TRANSCENDENCE,
        TechId("14106"): KaeleshLifeformBuilding.ANTIMATTER_CONVECTOR,
        TechId("14107"): KaeleshLifeformBuilding.CLONING_LABORATORY,
        TechId("14108"): KaeleshLifeformBuilding.CHRYSALIS_ACCELERATOR,
        TechId("14109"): KaeleshLifeformBuilding.BIO_MODIFIER,
        TechId("14110"): KaeleshLifeformBuilding.PSIONIC_MODULATOR,
        TechId("14111"): KaeleshLifeformBuilding.SHIP_MANUFACTURING_HALL,
        TechId("14112"): KaeleshLifeformBuilding.SUPRA_REFRACTOR,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}
    _name_to_enum_mapping = {TechName(e.name): e for e in KaeleshLifeformBuilding}

    @classmethod
    def get_name_by_value(cls, value: str) -> str:
        """
        Given a building 'value', return its Enum 'name'.
        """
        for member in KaeleshLifeformBuilding:
            if member.value == value:
                return member.name
        raise ValueError(f"Value '{value}' not found in KaeleshLifeformBuilding.")

    @classmethod
    def get_value_by_name(cls, name: str) -> str:
        """
        Given a building Enum 'name', return its 'value'.
        """
        try:
            return KaeleshLifeformBuilding[name].value
        except KeyError:
            raise ValueError(f"Name '{name}' not found in KaeleshLifeformBuilding.")

    @classmethod
    def get_name_by_id(cls, building_id: Union[str, TechId]) -> TechName:
        """
        Get Kaelesh building name by its ID.
        Accepts str or TechId, returns TechName.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Kaelesh building ID: {building_id}.")
        return TechName(cls._id_to_enum_mapping[typed_id].name)

    @classmethod
    def get_id_by_name(cls, building_name: Union[str, TechName]) -> TechId:
        """
        Get Kaelesh building ID by its name.
        Accepts str or TechName, returns TechId.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Kaelesh building name: {building_name}.")
        enum = cls._name_to_enum_mapping[typed_name]
        return cls._enum_to_id_mapping[enum]

    @classmethod
    def get_enum_by_id(cls, building_id: Union[str, TechId]) -> KaeleshLifeformBuilding:
        """
        Get Enum by building ID (internal/advanced).
        Accepts str or TechId.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Kaelesh building ID: {building_id}.")
        return cls._id_to_enum_mapping[typed_id]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """Return all Kaelesh building IDs as TechId objects."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> List[TechName]:
        """Return all Kaelesh building names as TechName objects."""
        return [TechName(e.name) for e in KaeleshLifeformBuilding]

    @classmethod
    def get_enum_by_name(cls, building_name: Union[str, TechName]) -> KaeleshLifeformBuilding:
        """
        Get Enum by building name (internal/advanced).
        Accepts str or TechName.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Kaelesh building name: {building_name}.")
        return cls._name_to_enum_mapping[typed_name]


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

from config.shared_types import TechId, TechName
from typing import Union, List

class MechaLifeformBuildingClass:
    """
    Type-safe utility for Mecha lifeform buildings.
    All mapping methods accept both str and TechId/TechName for ergonomics.
    Returns strongly typed objects.
    """
    _id_to_enum_mapping = {
        TechId("13101"): MechaLifeformBuilding.ASSEMBLY_LINE,
        TechId("13102"): MechaLifeformBuilding.FUSION_CELL_FACTORY,
        TechId("13103"): MechaLifeformBuilding.ROBOTICS_RESEARCH_CENTRE,
        TechId("13104"): MechaLifeformBuilding.UPDATE_NETWORK,
        TechId("13105"): MechaLifeformBuilding.QUANTUM_COMPUTER_CENTRE,
        TechId("13106"): MechaLifeformBuilding.AUTOMATISED_ASSEMBLY_CENTRE,
        TechId("13107"): MechaLifeformBuilding.HIGH_PERFORMANCE_TRANSFORMER,
        TechId("13108"): MechaLifeformBuilding.MICROCHIP_ASSEMBLY_LINE,
        TechId("13109"): MechaLifeformBuilding.PRODUCTION_ASSEMBLY_HALL,
        TechId("13110"): MechaLifeformBuilding.HIGH_PERFORMANCE_SYNTHESISER,
        TechId("13111"): MechaLifeformBuilding.CHIP_MASS_PRODUCTION,
        TechId("13112"): MechaLifeformBuilding.NANO_REPAIR_BOTS,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}
    _name_to_enum_mapping = {TechName(e.name): e for e in MechaLifeformBuilding}

    @classmethod
    def get_name_by_value(cls, value: str) -> str:
        """
        Given a building 'value', return its Enum 'name'.
        """
        for member in MechaLifeformBuilding:
            if member.value == value:
                return member.name
        raise ValueError(f"Value '{value}' not found in MechaLifeformBuilding.")

    @classmethod
    def get_value_by_name(cls, name: str) -> str:
        """
        Given a building Enum 'name', return its 'value'.
        """
        try:
            return MechaLifeformBuilding[name].value
        except KeyError:
            raise ValueError(f"Name '{name}' not found in MechaLifeformBuilding.")

    @classmethod
    def get_name_by_id(cls, building_id: Union[str, TechId]) -> TechName:
        """
        Get Mecha building name by its ID.
        Accepts str or TechId, returns TechName.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Mecha building ID: {building_id}.")
        return TechName(cls._id_to_enum_mapping[typed_id].name)

    @classmethod
    def get_id_by_name(cls, building_name: Union[str, TechName]) -> TechId:
        """
        Get Mecha building ID by its name.
        Accepts str or TechName, returns TechId.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Mecha building name: {building_name}.")
        enum = cls._name_to_enum_mapping[typed_name]
        return cls._enum_to_id_mapping[enum]

    @classmethod
    def get_enum_by_id(cls, building_id: Union[str, TechId]) -> MechaLifeformBuilding:
        """
        Get Enum by building ID (internal/advanced).
        Accepts str or TechId.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Mecha building ID: {building_id}.")
        return cls._id_to_enum_mapping[typed_id]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """Return all Mecha building IDs as TechId objects."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> List[TechName]:
        """Return all Mecha building names as TechName objects."""
        return [TechName(e.name) for e in MechaLifeformBuilding]

    @classmethod
    def get_enum_by_name(cls, building_name: Union[str, TechName]) -> MechaLifeformBuilding:
        """
        Get Enum by building name (internal/advanced).
        Accepts str or TechName.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Mecha building name: {building_name}.")
        return cls._name_to_enum_mapping[typed_name]


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

from config.shared_types import TechId, TechName
from typing import Union, List

class RocktalLifeformBuildingClass:
    """
    Type-safe utility for Rocktal lifeform buildings.
    All mapping methods accept both str and TechId/TechName for ergonomics.
    Returns strongly typed objects.
    """
    _id_to_enum_mapping = {
        TechId("12101"): RocktalLifeformBuilding.MEDITATION_ENCLAVE,
        TechId("12102"): RocktalLifeformBuilding.CRYSTAL_FARM,
        TechId("12103"): RocktalLifeformBuilding.RUNE_TECHNOLOGIUM,
        TechId("12104"): RocktalLifeformBuilding.ORIKTORIUM,
        TechId("12105"): RocktalLifeformBuilding.MAGMA_FORGE,
        TechId("12106"): RocktalLifeformBuilding.DISRUPTION_CHAMBER,
        TechId("12107"): RocktalLifeformBuilding.METROPOLIS,
        TechId("12108"): RocktalLifeformBuilding.ROCKTAL_COLLECTOR,
        TechId("12109"): RocktalLifeformBuilding.CRYSTAL_REFINERY,
        TechId("12110"): RocktalLifeformBuilding.DEUTERIUM_FURNACE,
        TechId("12111"): RocktalLifeformBuilding.MEGALITH,
        TechId("12112"): RocktalLifeformBuilding.FORUM_OF_TRANSCENDENCE,
    }
    _enum_to_id_mapping = {v: k for k, v in _id_to_enum_mapping.items()}
    _name_to_enum_mapping = {TechName(e.name): e for e in RocktalLifeformBuilding}

    @classmethod
    def get_name_by_value(cls, value: str) -> str:
        """
        Given a building 'value', return its Enum 'name'.
        """
        for member in RocktalLifeformBuilding:
            if member.value == value:
                return member.name
        raise ValueError(f"Value '{value}' not found in RocktalLifeformBuilding.")

    @classmethod
    def get_value_by_name(cls, name: str) -> str:
        """
        Given a building Enum 'name', return its 'value'.
        """
        try:
            return RocktalLifeformBuilding[name].value
        except KeyError:
            raise ValueError(f"Name '{name}' not found in RocktalLifeformBuilding.")

    @classmethod
    def get_name_by_id(cls, building_id: Union[str, TechId]) -> TechName:
        """
        Get Rocktal building name by its ID.
        Accepts str or TechId, returns TechName.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Rocktal building ID: {building_id}.")
        return TechName(cls._id_to_enum_mapping[typed_id].name)

    @classmethod
    def get_id_by_name(cls, building_name: Union[str, TechName]) -> TechId:
        """
        Get Rocktal building ID by its name.
        Accepts str or TechName, returns TechId.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Rocktal building name: {building_name}.")
        enum = cls._name_to_enum_mapping[typed_name]
        return cls._enum_to_id_mapping[enum]

    @classmethod
    def get_enum_by_id(cls, building_id: Union[str, TechId]) -> RocktalLifeformBuilding:
        """
        Get Enum by building ID (internal/advanced).
        Accepts str or TechId.
        Raises ValueError if not found.
        """
        typed_id = TechId(building_id)
        if typed_id not in cls._id_to_enum_mapping:
            raise ValueError(f"Invalid Rocktal building ID: {building_id}.")
        return cls._id_to_enum_mapping[typed_id]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """Return all Rocktal building IDs as TechId objects."""
        return list(cls._id_to_enum_mapping.keys())

    @classmethod
    def get_all_names(cls) -> List[TechName]:
        """Return all Rocktal building names as TechName objects."""
        return [TechName(e.name) for e in RocktalLifeformBuilding]

    @classmethod
    def get_enum_by_name(cls, building_name: Union[str, TechName]) -> RocktalLifeformBuilding:
        """
        Get Enum by building name (internal/advanced).
        Accepts str or TechName.
        Raises ValueError if not found.
        """
        typed_name = TechName(building_name)
        if typed_name not in cls._name_to_enum_mapping:
            raise ValueError(f"Invalid Rocktal building name: {building_name}.")
        return cls._name_to_enum_mapping[typed_name]
