from enum import Enum
from typing import Tuple

from config.types import TechId

# Type alias for all technology tuples (id, amount/level, category)
TechnologyTuple = Tuple[int, int, str]

# OGame page components
class COMPONENTS(Enum):
    OVERVIEW = "overview"
    SUPPLIES = "supplies"
    LFBUILDINGS = "lfbuildings"
    FACILITIES = "facilities"
    TRADER_OVERVIEW = "traderOverview"
    RESEARCH = "research"
    SHIPYARD = "shipyard"
    DEFENSES = "defenses"
    FLEET_DISPATCH = "fleetdispatch"
    GALAXY = "galaxy"
    EMPIRE = "empire"
    MESSAGES = "messages"

# Lifeform classes
class LifeformClass:
    human = 'human'
    mecha = 'mecha'

    @classmethod
    def allLifeforms(cls) -> list[str]:
        return [
            cls.human,
            cls.mecha,
        ]

# Mapping of technology IDs to their respective sections
class TechIdToSection:
    mapping = {
        # Buildings
        "1": COMPONENTS.SUPPLIES,
        "2": COMPONENTS.SUPPLIES,
        "3": COMPONENTS.SUPPLIES,
        "4": COMPONENTS.SUPPLIES,
        "12": COMPONENTS.SUPPLIES,
        "22": COMPONENTS.SUPPLIES,
        "23": COMPONENTS.SUPPLIES,
        "24": COMPONENTS.SUPPLIES,

        # Station
        "14": COMPONENTS.FACILITIES,
        "15": COMPONENTS.FACILITIES,
        "21": COMPONENTS.FACILITIES,
        "31": COMPONENTS.FACILITIES,
        "33": COMPONENTS.FACILITIES,
        "34": COMPONENTS.FACILITIES,
        "44": COMPONENTS.FACILITIES,
        "36": COMPONENTS.FACILITIES,

        # Defense
        "401": COMPONENTS.DEFENSES,
        "402": COMPONENTS.DEFENSES,
        "403": COMPONENTS.DEFENSES,
        "404": COMPONENTS.DEFENSES,
        "405": COMPONENTS.DEFENSES,
        "406": COMPONENTS.DEFENSES,
        "407": COMPONENTS.DEFENSES,
        "408": COMPONENTS.DEFENSES,
        "502": COMPONENTS.DEFENSES,
        "503": COMPONENTS.DEFENSES,

        # Ships
        "204": COMPONENTS.SHIPYARD,
        "205": COMPONENTS.SHIPYARD,
        "206": COMPONENTS.SHIPYARD,
        "207": COMPONENTS.SHIPYARD,
        "215": COMPONENTS.SHIPYARD,
        "211": COMPONENTS.SHIPYARD,
        "213": COMPONENTS.SHIPYARD,
        "214": COMPONENTS.SHIPYARD,
        "218": COMPONENTS.SHIPYARD,
        "219": COMPONENTS.SHIPYARD,
        "202": COMPONENTS.SHIPYARD,
        "203": COMPONENTS.SHIPYARD,
        "208": COMPONENTS.SHIPYARD,
        "209": COMPONENTS.SHIPYARD,
        "210": COMPONENTS.SHIPYARD,
        "212": COMPONENTS.SHIPYARD,
        "217": COMPONENTS.SHIPYARD,

        # Research
        "113": COMPONENTS.RESEARCH,
        "120": COMPONENTS.RESEARCH,
        "121": COMPONENTS.RESEARCH,
        "114": COMPONENTS.RESEARCH,
        "122": COMPONENTS.RESEARCH,
        "106": COMPONENTS.RESEARCH,
        "108": COMPONENTS.RESEARCH,
        "124": COMPONENTS.RESEARCH,
        "123": COMPONENTS.RESEARCH,
        "199": COMPONENTS.RESEARCH,
        "115": COMPONENTS.RESEARCH,
        "117": COMPONENTS.RESEARCH,
        "118": COMPONENTS.RESEARCH,
        "109": COMPONENTS.RESEARCH,
        "110": COMPONENTS.RESEARCH,
        "111": COMPONENTS.RESEARCH,

        # Lifeform Buildings
        "11101": COMPONENTS.LFBUILDINGS,
        "11102": COMPONENTS.LFBUILDINGS,
        "11103": COMPONENTS.LFBUILDINGS,
        "11104": COMPONENTS.LFBUILDINGS,
        "11105": COMPONENTS.LFBUILDINGS,
        "11106": COMPONENTS.LFBUILDINGS,
        "11107": COMPONENTS.LFBUILDINGS,
        "11108": COMPONENTS.LFBUILDINGS,
        "11109": COMPONENTS.LFBUILDINGS,
        "11110": COMPONENTS.LFBUILDINGS,
        "11111": COMPONENTS.LFBUILDINGS,
        "11112": COMPONENTS.LFBUILDINGS,

        # Lifeform Research
        "11201": COMPONENTS.RESEARCH,
        "11202": COMPONENTS.RESEARCH,
        "11203": COMPONENTS.RESEARCH,
        "11204": COMPONENTS.RESEARCH,
        "11205": COMPONENTS.RESEARCH,
        "11206": COMPONENTS.RESEARCH,
        "11207": COMPONENTS.RESEARCH,
        "11208": COMPONENTS.RESEARCH,
        "11209": COMPONENTS.RESEARCH,
        "11210": COMPONENTS.RESEARCH,
        "11211": COMPONENTS.RESEARCH,
        "11212": COMPONENTS.RESEARCH,
        "11213": COMPONENTS.RESEARCH,
        "11214": COMPONENTS.RESEARCH,
        "11215": COMPONENTS.RESEARCH,
        "11216": COMPONENTS.RESEARCH,
        "11217": COMPONENTS.RESEARCH,
        "11218": COMPONENTS.RESEARCH,
    }

    @classmethod
    def get_section(cls, tech_id: TechId) -> COMPONENTS:
        """
        Get the section corresponding to a technology ID.

        Args:
            tech_id (int): The technology ID.

        Returns:
            ComponentType: The section name.
        """
        if tech_id not in cls.mapping:
            raise ValueError(f"Invalid tech_id: {tech_id}. No corresponding section found.")
        section = cls.mapping[tech_id]
        if section not in vars(COMPONENTS).values():
            raise TypeError(f"Return value {section} is not a valid Section.")
        return section  # Explicitly return the section as a COMPONENTS value

