from typing import Tuple

# Type alias for all technology tuples (id, amount/level, category)
TechnologyTuple = Tuple[int, int, str]

# OGame page components
class COMPONENTS:
    overview = "overview"
    supplies = "supplies"
    lfbuildings = "lfbuildings"
    facilities = "facilities"
    traderOverview = "traderOverview"
    research = "research"
    shipyard = "shipyard"
    defenses = "defenses"
    fleetdispatch = "fleetdispatch"
    galaxy = "galaxy"
    empire = "empire"
    messages = "messages"

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