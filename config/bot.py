
from typing import Any, Callable, Dict, List, Optional
from config.types import ConfigType
from core.notifications.telegram_notifier import TelegramNotifier
from playwright.sync_api import Page

# Config.json path
CONFIG_FILE_PATH: str = "config.json"

UpgradeHandlersType = Dict[str, Callable[[Any, Page, Optional[TelegramNotifier]], Optional[List[int]]]]

DEFAULT_CONFIG: ConfigType = {
    "check_interval": 10,
    "enable_expeditions": True,
    "expedition_planet_id": "33632165", # Nexus Sentinel
    "upgrade_order": [
        "facilities",
        "resources",
        "energy",
        "research",
        "lifeforms",
        "storage"
    ],
    "upgrade_toggles": {
        "facilities": True,
        "resources": True,
        "energy": True,
        "research": True,
        "lifeforms": True,
        "storage": True
    }
}
