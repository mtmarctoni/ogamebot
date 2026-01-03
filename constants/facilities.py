from enum import Enum

class Facility(Enum):
    ROBOTICS_FACTORY = "roboticsFactory"
    SHIPYARD = "shipyard"
    RESEARCH_LAB = "researchLaboratory"
    ALLIANCE_DEPOT = "allianceDepot"
    MISSILE_SILO = "missileSilo"
    NANITE_FACTORY = "naniteFactory"
    TERRAFORMER = "terraformer"
    SPACE_DOCK = "repairDock"


class Facilities:
    """
    A utility class to map between Facility names and their corresponding IDs.
    Ensures that only Facility types are used.
    """

    _id_to_name_mapping = {
        "14": Facility.ROBOTICS_FACTORY,
        "21": Facility.SHIPYARD,
        "31": Facility.RESEARCH_LAB,
        "34": Facility.ALLIANCE_DEPOT,
        "44": Facility.MISSILE_SILO,
        "15": Facility.NANITE_FACTORY,
        "33": Facility.TERRAFORMER,
        "36": Facility.SPACE_DOCK,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, facility_id: str) -> Facility:
        """
        Get the Facility name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if facility_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Facility ID: {facility_id}. No corresponding Facility found.")
        return cls._id_to_name_mapping[facility_id]

    @classmethod
    def get_id_by_name(cls, facility_name: Facility) -> str:
        """
        Get the Facility ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if facility_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Facility: {facility_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[facility_name]