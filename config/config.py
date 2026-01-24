# config.py
"""
Configuration for OGame bot: server, language, universe, and URLs.
"""

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
    "colony7": {
        "id": "33664045",
        "name": "Voidward Bastion",
        "coords": "[4:268:8]",
        "species": "Kaelesh",
    },
    "moon_home": {
        "id": "33645298",
        "name": "Moon",
        "coords": "[2:16:8]",
        "species": "Human",
    }
}

DEFAULT_PLANET_ID = PLANETS["home_planet"]["id"]

# Planet to use for expeditions
DEFAULT_EXPEDITION_PLANET_ID = PLANETS["colony3"]["id"]

# Target coordinates for expeditions
TARGET_COORDINATES = [
    [1, 413, 16],
    [1, 411, 16],
    [1, 414, 16],
    [1, 415, 16],
    [1, 412, 16]
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

# Constants in the Universe
MAX_SYSTEM_NUMBER = 499
MAX_GALAXY_NUMBER = 6
MAX_SLOT_NUMBER = 16
