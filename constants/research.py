from enum import Enum

class Research(Enum):
    INTERGALACTIC_RESEARCH_NETWORK = "researchNetworkResearchNetwork"
    HYPERSPACE = "hyperspaceTechnology"
    IMPULSE_DRIVE = "impulseDriveTechnology"
    COMBUSTION_DRIVE = "combustionDriveTechnology"
    PLASMA = "plasma"
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
    A utility class to map between Research names and their corresponding IDs.
    Ensures that only Research types are used.
    """

    _id_to_name_mapping = {
        "106": Research.ESPIONAGE,
        "108": Research.COMPUTER,
        "109": Research.WEAPONS,
        "110": Research.SHIELDING,
        "111": Research.ARMOR,
        "113": Research.ENERGY,
        "114": Research.HYPERSPACE,
        "115": Research.COMBUSTION_DRIVE,
        "117": Research.IMPULSE_DRIVE,
        "118": Research.HYPERSPACE,
        "120": Research.LASER,
        "121": Research.ION,
        "122": Research.PLASMA,
        "123": Research.INTERGALACTIC_RESEARCH_NETWORK,
        "124": Research.ASTROPHYSICS,
        "199": Research.GRAVITON,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, research_id: str) -> Research:
        """
        Get the Research name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if research_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Research ID: {research_id}. No corresponding Research found.")
        return cls._id_to_name_mapping[research_id]

    @classmethod
    def get_id_by_name(cls, research_name: Research) -> str:
        """
        Get the Research ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if research_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Research: {research_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[research_name]