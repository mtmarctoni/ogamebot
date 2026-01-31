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
    CRAWLER = "resbuggy"


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
        "217": Ship.CRAWLER,
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
    
    @classmethod
    def get_consumption_by_id(cls, ship_id: str) -> int:
        """
        Get the Ship consumption by its ID.
        Raises a ValueError if the ID is invalid.
        """
        consumption_lookup = {
            Ship.SMALL_CARGO: 20,   # Small Cargo
            Ship.LARGE_CARGO: 50,   # Large Cargo
            Ship.LIGHT_FIGHTER: 20,   # Light Fighter
            Ship.HEAVY_FIGHTER: 75,   # Heavy Fighter
            Ship.CRUISER: 300,   # Cruiser
            Ship.BATTLESHIP: 500,  # Battleship
            Ship.COLONY_SHIP: 1000,  # Colony Ship
            Ship.RECYCLER: 300,  # Recycler
            Ship.ESPIONAGE_PROBE: 1,    # Espionage Probe
            Ship.BOMBER: 700, # Bomber
            Ship.SOLAR_SATELLITE: 1,    # Solar Satellite
            Ship.DESTROYER: 1000, # Destroyer
            Ship.DEATHSTAR: 1,# Deathstar
            Ship.BATTLECRUISER: 250,  # Battlecruiser
            Ship.REAPER: 1100, # Reaper
            Ship.PATHFINDER: 300,   # Pathfinder
            Ship.CRAWLER: 1    # Crawler
        }
        ship_name = cls.get_name_by_id(ship_id)
        if ship_name not in consumption_lookup:
            raise ValueError(f"Invalid Ship ID: {ship_id}. No corresponding consumption found.")
        return consumption_lookup[ship_name]
    
    @classmethod
    def get_expedition_points_by_id(cls, ship_id: str) -> int:
        """
        Get the Ship expedition points by its ID.
        Raises a ValueError if the ID is invalid.
        """
        expedition_points_lookup = {
            Ship.LIGHT_FIGHTER: 20,
            Ship.HEAVY_FIGHTER: 50,
            Ship.CRUISER: 135,
            Ship.BATTLESHIP: 300,
            Ship.BATTLECRUISER: 350,
            Ship.BOMBER: 375,
            Ship.DESTROYER: 600,
            Ship.DEATHSTAR: 900,
            Ship.SMALL_CARGO: 10,
            Ship.LARGE_CARGO: 25,
            Ship.COLONY_SHIP: 100,
            Ship.RECYCLER: 40,
            Ship.REAPER: 900,
            Ship.PATHFINDER: 75,
            Ship.ESPIONAGE_PROBE: 1
        }
        ship_name = cls.get_name_by_id(ship_id)
        if ship_name not in expedition_points_lookup:
            raise ValueError(f"Invalid Ship ID: {ship_id}. No corresponding expedition points found.")
        return expedition_points_lookup[ship_name]

unwanted_ships_for_expeditions = [
    Ship.ESPIONAGE_PROBE.value,
    Ship.RECYCLER.value,
    Ship.COLONY_SHIP.value,
    Ship.DEATHSTAR.value,
    Ship.CRAWLER.value,
]