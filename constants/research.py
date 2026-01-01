from enum import Enum

class Research(Enum):
    INTERGALACTIC_RESEARCH_NETWORK = "intergalacticResearchNetwork"
    HYPERSPACE_TECHNOLOGY = "hyperspaceTechnology"
    PLASMA_TECHNOLOGY = "plasmaTechnology"
    ASTROPHYSICS = "astrophysics"
    ESPIONAGE_TECHNOLOGY = "espionageTechnology"
    ENERGY_TECHNOLOGY = "energyTechnology"
    LASER_TECHNOLOGY = "laserTechnology"
    ION_TECHNOLOGY = "ionTechnology"
    COMPUTER_TECHNOLOGY = "computerTechnology"
    GRAVITON_TECHNOLOGY = "gravitonTechnology"
    WEAPON_TECHNOLOGY = "weaponTechnology"
    SHIELDING_TECHNOLOGY = "shieldingTechnology"
    ARMOUR_TECHNOLOGY = "armourTechnology"

class Researches:
    """
    A utility class to map between Research names and their corresponding IDs.
    Ensures that only Research types are used.
    """

    _id_to_name_mapping = {
        "123": Research.INTERGALACTIC_RESEARCH_NETWORK,
        "114": Research.HYPERSPACE_TECHNOLOGY,
        "122": Research.PLASMA_TECHNOLOGY,
        "124": Research.ASTROPHYSICS,
        "113": Research.ENERGY_TECHNOLOGY,
        "106": Research.ESPIONAGE_TECHNOLOGY,
        "120": Research.LASER_TECHNOLOGY,
        "121": Research.ION_TECHNOLOGY,
        "108": Research.COMPUTER_TECHNOLOGY,
        "199": Research.GRAVITON_TECHNOLOGY,
        "109": Research.WEAPON_TECHNOLOGY,
        "110": Research.SHIELDING_TECHNOLOGY,
        "111": Research.ARMOUR_TECHNOLOGY,
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