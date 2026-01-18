
from typing import Any, Callable, Dict, List, Optional
from config.types import ConfigRawType
from core.notifications.telegram_notifier import TelegramNotifier
from playwright.sync_api import Page

# Config.json path
CONFIG_FILE_PATH: str = "config.json"

UpgradeHandlersType = Dict[str, Callable[[Any, Page, Optional[TelegramNotifier]], Optional[List[int]]]]

DEFAULT_CONFIG: ConfigRawType = {
    "check_interval": 10,
    "expeditions": {
        "enable_expeditions": True,
        "expedition_planet_id": "33646912"
    },
    "upgrades": {
        "group_order": [
        "facilities",
        "resources",
        "energy",
        "research",
        "lifeforms",
        "storage"
        ],
        "toggles": {
        "facilities": True,
        "resources": True,
        "energy": True,
        "research": True,
        "lifeforms": True,
        "storage": True
        },
        "priorities": {
        "facilities": [
            "NANITE_FACTORY",
            "ROBOTICS_FACTORY",
            "RESEARCH_LAB",
            "SHIPYARD",
            "TERRAFORMER",
            "MISSILE_SILO",
            "ALLIANCE_DEPOT",
            "SPACE_DOCK"
        ],
        "research": [
            "ASTROPHYSICS",
            "PLASMA",
            "COMBUSTION_DRIVE",
            "IMPULSE_DRIVE",
            "HYPERSPACE",
            "COMPUTER",
            "ENERGY",
            "ESPIONAGE",
            "WEAPONS",
            "SHIELDING",
            "ARMOR",
            "LASER",
            "ION",
            "INTERGALACTIC_RESEARCH_NETWORK",
            "GRAVITON"
        ],
        "lifeform_buildings": {
            "Human": [
            "Research_Center",
            "Academy",
            "Neuro_Calibration_Center",
            "High_Energy_Smelting",
            "Skyscraper",
            "Biosphere_Farm",
            "Residential_Sector",
            "Food_Silo",
            "Fusion_Powered_Production",
            "Biotech_Lab",
            "Metropolis",
            "Planetary_Shield"
            ],
            "Kaelesh": [
            "Sanctuary",
            "Antimatter_Condenser",
            "Vortex_Chamber",
            "Halls_of_Realization",
            "Forum_of_Transcendence",
            "Antimatter_Convector",
            "Cloning_Laboratory",
            "Chrysalis_Accelerator",
            "Bio_Modifier",
            "Psionic_Modulator",
            "Ship_Manufacturing_Hall",
            "Supra_Refractor"
            ]
        }
        }
    }
}
