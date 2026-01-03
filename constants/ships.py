from enum import Enum

class Ship(Enum):
    SMALL_CARGO = "transporterSmall"
    LARGE_CARGO = "transporterLarge"
    LIGHT_FIGHTER = "fighterLight"
    HEAVY_FIGHTER = "fighterHeavy"
    CRUISER = "cruiser"
    BATTLESHIP = "battleship"
    COLONY_SHIP = "colonyShip"
    RECYCLER = "recycler"
    ESPIONAGE_PROBE = "espionageProbe"
    BOMBER = "bomber"
    SOLAR_SATELLITE = "solarSatellite"
    DESTROYER = "destroyer"
    DEATHSTAR = "deathstar"
    BATTLECRUISER = "interceptor"
    REAPER = "reaper"
    PATHFINDER = "explorer"


class Ships:
    """
    A utility class to map between Ship names and their corresponding IDs.
    Ensures that only Ship types are used.
    """

    _id_to_name_mapping = {
        "202": Ship.SMALL_CARGO,
        "203": Ship.LARGE_CARGO,
        "204": Ship.LIGHT_FIGHTER,
        "205": Ship.HEAVY_FIGHTER,
        "206": Ship.CRUISER,
        "207": Ship.BATTLESHIP,
        "208": Ship.COLONY_SHIP,
        "209": Ship.RECYCLER,
        "210": Ship.ESPIONAGE_PROBE,
        "211": Ship.BOMBER,
        "212": Ship.SOLAR_SATELLITE,
        "213": Ship.DESTROYER,
        "214": Ship.DEATHSTAR,
        "215": Ship.BATTLECRUISER,
        "218": Ship.REAPER,
        "219": Ship.PATHFINDER,
    }

    _name_to_id_mapping = {v: k for k, v in _id_to_name_mapping.items()}

    @classmethod
    def get_name_by_id(cls, ship_id: str) -> Ship:
        """
        Get the Ship name by its ID.
        Raises a ValueError if the ID is invalid.
        """
        if ship_id not in cls._id_to_name_mapping:
            raise ValueError(f"Invalid Ship ID: {ship_id}. No corresponding Ship found.")
        return cls._id_to_name_mapping[ship_id]

    @classmethod
    def get_id_by_name(cls, ship_name: Ship) -> str:
        """
        Get the Ship ID by its name.
        Raises a ValueError if the name is invalid.
        """
        if ship_name not in cls._name_to_id_mapping:
            raise ValueError(f"Invalid Ship: {ship_name}. No corresponding ID found.")
        return cls._name_to_id_mapping[ship_name]

