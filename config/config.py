# config.py
"""
Configuration for OGame bot: server, language, universe, and URLs.
"""

SERVER_ID = "271"
LANG = "en"
DOMAIN = f"s{SERVER_ID}-{LANG}.ogame.gameforge.com"
REFRESH_TIME = 10  # seconds

# Base URL for OGame server
OGAME_BASE_URL = f"https://{DOMAIN}"

# Main page URL template (overview for a given planet)
MAIN_PAGE_URL_TEMPLATE = (
    f"https://s{SERVER_ID}-{LANG}.ogame.gameforge.com/game/index.php?page=ingame&cp={{planet_id}}"
)

# URL template for specific component navigation
COMPONENT_URL_TEMPLATE = "https://s{server}-{language}.ogame.gameforge.com/game/index.php?page=ingame&component={component}&cp={planet_id}"

# OGame page components
COMPONENTS = {
    "overview": "overview",
    "supplies": "supplies",
    "lfbuildings": "lfbuildings",
    "facilities": "facilities",
    "traderOverview": "traderOverview",
    "research": "research",
    "shipyard": "shipyard",
    "defenses": "defenses",
    "fleetdispatch": "fleetdispatch",
    "galaxy": "galaxy",
    "empire": "empire",
    "messages": "messages",
}

# Default planet ids
PLANET_IDS = {
    "default": "33625285",
    "colony1": "33629156",
    "colony2": "33630366",
}

DEFAULT_PLANET_ID = PLANET_IDS["default"]  # Main planet

# Lobby URL
LOBBY_URL = f"https://lobby.ogame.gameforge.com/en_GB/hub"
