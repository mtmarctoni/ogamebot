from enum import Enum
from config.shared_types import TechId, TechName, TechValue
from typing import List, Union

class Research(Enum):
    INTERGALACTIC_RESEARCH_NETWORK = "researchNetworkResearchNetwork"
    HYPERSPACE = "hyperspaceTechnology"
    HYPERSPACE_DRIVE = "hyperspaceDriveTechnology"
    IMPULSE_DRIVE = "impulseDriveTechnology"
    COMBUSTION_DRIVE = "combustionDriveTechnology"
    PLASMA = "plasmaTechnology"
    ASTROPHYSICS = "astrophysicsTechnology"
    ESPIONAGE = "espionageTechnology"
    ENERGY = "energyTechnology"
    LASER = "laserTechnology"
    ION = "ionTechnology"
    COMPUTER = "computerTechnology"
    GRAVITON = "gravitonTechnology"
    WEAPONS = "weaponsTechnology"
    SHIELDING = "shieldingTechnology"
    ARMOR = "armorTechnology"

class Researches:
    """
    A utility class to map between Research names, values and their corresponding IDs.
    Avoids enum usage in main code for clarity.
    Provides methods for all mapping conversions and full listings.
    Accepts string and Tech* types for all inputs for ergonomics.
    """

    _id_to_enum = {
        TechId("106"): Research.ESPIONAGE,
        TechId("108"): Research.COMPUTER,
        TechId("109"): Research.WEAPONS,
        TechId("110"): Research.SHIELDING,
        TechId("111"): Research.ARMOR,
        TechId("113"): Research.ENERGY,
        TechId("114"): Research.HYPERSPACE,
        TechId("115"): Research.COMBUSTION_DRIVE,
        TechId("117"): Research.IMPULSE_DRIVE,
        TechId("118"): Research.HYPERSPACE_DRIVE,
        TechId("120"): Research.LASER,
        TechId("121"): Research.ION,
        TechId("122"): Research.PLASMA,
        TechId("123"): Research.INTERGALACTIC_RESEARCH_NETWORK,
        TechId("124"): Research.ASTROPHYSICS,
        TechId("199"): Research.GRAVITON,
    }
    _enum_to_id = {v: k for k, v in _id_to_enum.items()}
    _name_to_enum = {TechName(r.name): r for r in Research}
    _value_to_enum = {TechValue(r.value): r for r in Research}

    @classmethod
    def get_value_by_id(cls, research_id: Union[str, TechId]) -> TechValue:
        """Get research value by its ID (e.g. 'energyTechnology'). Accepts str or TechId."""
        research_id = TechId(research_id)
        if research_id not in cls._id_to_enum:
            raise ValueError(f"Invalid Research ID: {research_id}. No corresponding Research found.")
        return TechValue(cls._id_to_enum[research_id].value)

    @classmethod
    def get_name_by_id(cls, research_id: Union[str, TechId]) -> TechName:
        """Get research name by its ID (e.g. 'ENERGY'). Accepts str or TechId."""
        research_id = TechId(research_id)
        if research_id not in cls._id_to_enum:
            raise ValueError(f"Invalid Research ID: {research_id}. No corresponding Research found.")
        return TechName(cls._id_to_enum[research_id].name)

    @classmethod
    def get_id_by_name(cls, research_name: Union[str, TechName]) -> TechId:
        """Get research ID by its name (e.g. 'ENERGY' → TechId('113')). Accepts str or TechName."""
        research_name = TechName(research_name)
        if research_name not in cls._name_to_enum:
            raise ValueError(f"Invalid Research name: {research_name}. No corresponding Research found.")
        enum = cls._name_to_enum[research_name]
        return cls._enum_to_id[enum]

    @classmethod
    def get_id_by_value(cls, research_value: Union[str, TechValue]) -> TechId:
        """Get research ID by its value (e.g. 'energyTechnology' → TechId('113')). Accepts str or TechValue."""
        research_value = TechValue(research_value)
        if research_value not in cls._value_to_enum:
            raise ValueError(f"Invalid Research value: {research_value}. No corresponding Research found.")
        enum = cls._value_to_enum[research_value]
        return cls._enum_to_id[enum]

    @classmethod
    def get_value_by_name(cls, research_name: Union[str, TechName]) -> TechValue:
        """Get research value by its name (e.g. 'ENERGY' → 'energyTechnology'). Accepts str or TechName."""
        research_name = TechName(research_name)
        if research_name not in cls._name_to_enum:
            raise ValueError(f"Invalid Research name: {research_name}. No corresponding Research found.")
        return TechValue(cls._name_to_enum[research_name].value)

    @classmethod
    def get_name_by_value(cls, research_value: Union[str, TechValue]) -> TechName:
        """Get research name by its value (e.g. 'energyTechnology' → 'ENERGY'). Accepts str or TechValue."""
        research_value = TechValue(research_value)
        if research_value not in cls._value_to_enum:
            raise ValueError(f"Invalid Research value: {research_value}. No corresponding Research found.")
        return TechName(cls._value_to_enum[research_value].name)

    @classmethod
    def get_enum_by_id(cls, research_id: Union[str, TechId]) -> Research:
        """(Internal) Get enum by ID, legacy/advanced only. Accepts str or TechId."""
        research_id = TechId(research_id)
        if research_id not in cls._id_to_enum:
            raise ValueError(f"Invalid Research ID: {research_id}. No corresponding Research found.")
        return cls._id_to_enum[research_id]

    @classmethod
    def get_all_ids(cls) -> List[TechId]:
        """Return all research IDs as TechId objects."""
        return list(cls._id_to_enum.keys())

    @classmethod
    def get_all_names(cls) -> List[TechName]:
        """Return all research names as TechName objects."""
        return [TechName(r.name) for r in Research]

    @classmethod
    def get_all_values(cls) -> List[TechValue]:
        """Return all research values as TechValue objects."""
        return [TechValue(r.value) for r in Research]


