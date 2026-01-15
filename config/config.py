# config.py
"""
Configuration for OGame bot: server, language, universe, and URLs.
"""

from typing import Dict
from config.types import TechLevel
from constants.energy import EnergyBuilding
from constants.facilities import Facility
from constants.lifeform_buildings import HumanLifeformBuildingClass, KaeleshLifeformBuildingClass
from constants.research import Research
from constants.resources import ResourceClass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Maximum consecutive restart attempts before giving up
MAX_RESTART_ATTEMPTS = 5
# Delay between restart attempts (in seconds)
RESTART_DELAY = 30

# OGame server and universe configuration
SERVER_ID = "271"
LANG = "en"
DOMAIN = f"s{SERVER_ID}-{LANG}.ogame.gameforge.com"
REFRESH_TIME = 10  # seconds

# Added a constant for the database folder path
DB_FOLDER_PATH = "database"

# Base URL for OGame server
OGAME_BASE_URL = f"https://{DOMAIN}"

# Main game URL
OGAME_GAME_URL = f"{OGAME_BASE_URL}/game/index.php?page=ingame"

# URL template for specific component navigation
COMPONENT_URL_TEMPLATE = f"{OGAME_GAME_URL}&component={{component}}&cp={{planet_id}}"

# URL to get empire view
EMPIRE_VIEW_URL = f'{OGAME_BASE_URL}/game/index.php?page=standalone&component=empire'

# PLANETS
PLANETS = {
    "home_planet": {
        "id": "33625285",
        "name": "Abyssal Nexus",
        "coords": "[2:8:12]",
        "species": "Human",
    },
    "colony1": {
        "id": "33629156",
        "name": "Echoes of the Void",
        "coords": "[2:21:8]",
        "species": "Human",
    },
    "colony2": {
        "id": "33630366",
        "name": "Halo of the Nexus",
        "coords": "[2:8:9]",
        "species": "Human",
    },
    "colony3": {
        "id": "33632165",
        "name": "Nexus Sentinel",
        "coords": "[2:18:7]",
        "species": "Human",
    },
    "colony4": {
        "id": "33634157",
        "name": "Voidwatch Haven",
        "coords": "[1:413:9]",
        "species": "Human",
    },
    "colony5": {
        "id": "33646912",
        "name": "Haven s Veil",
        "coords": "[1:413:8]",
        "species": "Kaelesh",
    },
    "colony6": {
        "id": "33652874",
        "name": "Void Nexus",
        "coords": "[2:16:8]",
        "species": "Kaelesh",
    },
    "moon_default": {
        "id": "33645298",
        "name": "Moon",
        "coords": "[2:16:8]",
        "species": "Human",
    }
}

# Default planet ids
PLANET_IDS = {
    "default": "33625285",
    "colony1": "33629156",
    "colony2": "33630366",
    "colony3": "33632165",
    "colony4": "33634157",
    "colony5": "33646912",
    "moon_default": "33645298",
}

DEFAULT_PLANET_ID = PLANET_IDS["default"]  # Main planet

# Planet to use for expeditions
EXPEDITION_PLANET_ID = PLANET_IDS["colony3"]

# Target coordinates for expeditions
TARGET_COORDINATES = [
    [2, 8, 16],
    [2, 7, 16],
    [2, 9, 16],
    [2, 10, 16],
    [2, 6, 16]
]

# Lobby URL
LOBBY_URL = f"https://lobby.ogame.gameforge.com/en_GB/hub"

# Storage thresholds
STORAGE_WARNING_THRESHOLD = 0.90  # 90%: warn user
STORAGE_UPGRADE_THRESHOLD = 0.95  # 95%: trigger upgrade

# Sleep intervals (in minutes)
NIGHT_MIN_SLEEP = 30 # 4 hours
NIGHT_MAX_SLEEP = 40  # 5 hours
DAY_MIN_SLEEP = 13     
DAY_MAX_SLEEP = 19     
DEFAULT_MIN_SLEEP = 27
DEFAULT_MAX_SLEEP = 39

# Lifeforms species
LIFEFORM_SPECIES = {
    'Human': '1',
    'Kaelesh': '4'
}

# Priority configuration for HumanLifeformBuildings
HUMAN_LIFEFORM_BUILDING_PRIORITY = [
    HumanLifeformBuildingClass.Research_Center,
    HumanLifeformBuildingClass.Academy,
    HumanLifeformBuildingClass.Neuro_Calibration_Center,
    HumanLifeformBuildingClass.High_Energy_Smelting,
    HumanLifeformBuildingClass.Skyscraper,
    HumanLifeformBuildingClass.Biosphere_Farm,
    HumanLifeformBuildingClass.Residential_Sector,
    HumanLifeformBuildingClass.Food_Silo,
    HumanLifeformBuildingClass.Fusion_Powered_Production,
    HumanLifeformBuildingClass.Biotech_Lab,
    HumanLifeformBuildingClass.Metropolis,
    HumanLifeformBuildingClass.Planetary_Shield
]

# Priority configuration for KaeleshLifeformBuildings
KALESH_LIFEFORM_BUILDING_PRIORITY = [
    KaeleshLifeformBuildingClass.Sanctuary,
    KaeleshLifeformBuildingClass.Antimatter_Condenser,
    KaeleshLifeformBuildingClass.Vortex_Chamber,
    KaeleshLifeformBuildingClass.Halls_of_Realization,
    KaeleshLifeformBuildingClass.Forum_of_Transcendence,
    KaeleshLifeformBuildingClass.Antimatter_Convector,
    KaeleshLifeformBuildingClass.Cloning_Laboratory,
    KaeleshLifeformBuildingClass.Chrysalis_Accelerator,
    KaeleshLifeformBuildingClass.Bio_Modifier,
    KaeleshLifeformBuildingClass.Psionic_Modulator,
    KaeleshLifeformBuildingClass.Ship_Manufacturing_Hall,
    KaeleshLifeformBuildingClass.Supra_Refractor
]

# Priority configuration for Research
RESEARCH_PRIORITY = [
    Research.ASTROPHYSICS,
    Research.PLASMA,
    Research.COMBUSTION_DRIVE,
    Research.IMPULSE_DRIVE,
    Research.HYPERSPACE,
    Research.COMPUTER,
    Research.ENERGY,
    Research.ESPIONAGE,
    Research.WEAPONS,
    Research.SHIELDING,
    Research.ARMOR,
    Research.LASER,
    Research.ION,
    Research.INTERGALACTIC_RESEARCH_NETWORK,
    Research.GRAVITON,
]

# Facilities upgrade priority
FACILITIES_PRIORITY = [
    Facility.NANITE_FACTORY,
    Facility.ROBOTICS_FACTORY,
    Facility.RESEARCH_LAB,
    Facility.SHIPYARD,
    Facility.TERRAFORMER,
    Facility.MISSILE_SILO,
    Facility.ALLIANCE_DEPOT,
    Facility.SPACE_DOCK,
]

# Soft caps for resource levels (can be tuned per account stage)
SOFT_CAPS: Dict[str | EnergyBuilding, TechLevel] = {
    ResourceClass.metal: TechLevel(28),
    ResourceClass.crystal: TechLevel(25),
    ResourceClass.deuterium: TechLevel(22),
    EnergyBuilding.SOLAR_PLANT: TechLevel(20),
    EnergyBuilding.FUSION_PLANT: TechLevel(15),
}
