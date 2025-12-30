
# config.py
"""
Configuration for OGame bot: server, language, universe, and URLs.
"""

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
}

DEFAULT_PLANET_ID = PLANET_IDS["default"]  # Main planet

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

# Set lifeform building priority

