# config.py
"""
Configuration for OGame bot: server, language, universe, and URLs.
"""

from typing import Dict
from config.types import TechLevel
from constants.energy import EnergyBuilding
from constants.facilities import Facility
from constants.lifeform_buildings import HumanLifeformBuildingClass
from constants.research import Research
from constants.resources import ResourceClass
import os
from dotenv import load_dotenv

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
EXPEDITION_PLANET_ID = PLANET_IDS["default"]

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
NIGHT_MIN_SLEEP = 240  # 4 hours
NIGHT_MAX_SLEEP = 300  # 5 hours
DAY_MIN_SLEEP = 23     
DAY_MAX_SLEEP = 38     
DEFAULT_MIN_SLEEP = 45
DEFAULT_MAX_SLEEP = 75

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

# Priority configuration for Research
RESEARCH_PRIORITY = [
    Research.ENERGY,
    Research.ASTROPHYSICS,
    Research.COMPUTER,
    Research.INTERGALACTIC_RESEARCH_NETWORK,
    Research.PLASMA,
    Research.COMBUSTION_DRIVE,
    Research.IMPULSE_DRIVE,
    Research.ESPIONAGE,
    Research.WEAPONS,
    Research.SHIELDING,
    Research.ARMOR,
    Research.HYPERSPACE,
    Research.LASER,
    Research.ION,
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

# Load environment variables from .env file
load_dotenv()

UPGRADE_CONFIG = {
    "enable_resource_upgrades": os.getenv("ENABLE_RESOURCE_UPGRADES", "true").lower() == "true",
    "enable_energy_upgrades": os.getenv("ENABLE_ENERGY_UPGRADES", "true").lower() == "true",
    "enable_facility_upgrades": os.getenv("ENABLE_FACILITY_UPGRADES", "true").lower() == "true",
    "enable_research_upgrades": os.getenv("ENABLE_RESEARCH_UPGRADES", "true").lower() == "true",
    "enable_storage_upgrades": os.getenv("ENABLE_STORAGE_UPGRADES", "true").lower() == "true",
    "enable_lifeform_upgrades": os.getenv("ENABLE_LIFEFORM_UPGRADES", "true").lower() == "true",
    "enable_expeditions": os.getenv("ENABLE_EXPEDITIONS", "true").lower() == "true",
}