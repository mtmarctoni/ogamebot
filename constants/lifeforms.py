from enum import Enum

class Lifeforms(Enum):
    HUMAN = 'Human'
    ROCKTAL = 'Rocktal'
    MECHA = 'Mecha'
    KAELESH = 'Kaelesh' 
    
class LifeformClass:
    """
    A utility class to map between Lifeform names and their corresponding classes.
    Ensures that only Lifeform types are used.
    """

    _id_to_name_mapping = {
        "1": Lifeforms.HUMAN,
        "2": Lifeforms.ROCKTAL,
        "3": Lifeforms.MECHA,
        "4": Lifeforms.KAELESH,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_all_ids(cls) -> list[str]:
        """
        Get all the Lifeform IDs in a type-safe way.
        """
        return list(cls._id_to_name_mapping.keys())


    @classmethod
    def get_name_by_id(cls, lifeform_id: str) -> Lifeforms:
        """
        Get the Lifeform name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if lifeform_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Lifeform ID: {lifeform_id}. No corresponding Lifeform found.")
        return cls._id_to_name_mapping[lifeform_id]
    
    @classmethod
    def get_id_by_name(cls, lifeform_name: Lifeforms) -> str:
        """
        Get the Lifeform ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if lifeform_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Lifeform Name: {lifeform_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[lifeform_name]
    