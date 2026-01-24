
from typing import Callable, Dict, List, Optional
from config.types import PlanetDict, ConfigType
from config.types import ConfigRawType
from core.notifications.telegram_notifier import TelegramNotifier
from playwright.sync_api import Page

# Config.json path
CONFIG_FILE_PATH: str = "config.json"

UpgradeHandlersType = Dict[
    str,
    Callable[
        [PlanetDict, Page, ConfigType, Optional[TelegramNotifier]], Optional[List[int]]
    ]
]

DEFAULT_CONFIG: ConfigRawType = {
    "check_interval": 10,
    "expeditions": {
        "enable_expeditions": True,
        "expedition_planet_id": "33646912"
    },
    "discoveries": {
        "enable_discoveries": True,
        "discovery_planet_id": "33646912"
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
        "human": [
          "RESEARCH_CENTER",
          "ACADEMY",
          "NEURO_CALIBRATION_CENTER",
          "HIGH_ENERGY_SMELTING",
          "SKYSCRAPER",
          "BIOSPHERE_FARM",
          "RESIDENTIAL_SECTOR",
          "FOOD_SILO",
          "FUSION_POWERED_PRODUCTION",
          "BIOTECH_LAB",
          "METROPOLIS",
          "PLANETARY_SHIELD"
        ],
        "kaelesh": [
          "SANCTUARY",
          "ANTIMATTER_CONDENSER",
          "VORTEX_CHAMBER",
          "HALLS_OF_REALIZATION",
          "FORUM_OF_TRANSCENDENCE",
          "ANTIMATTER_CONVECTOR",
          "CLONING_LABORATORY",
          "CHRYSALIS_ACCELERATOR",
          "BIO_MODIFIER",
          "PSIONIC_MODULATOR",
          "SHIP_MANUFACTURING_HALL",
          "SUPRA_REFRACTOR"
        ],
        "mecha": [
          "ASSEMBLY_LINE",
          "FUSION_CELL_FACTORY",
          "ROBOTICS_RESEARCH_CENTRE",
          "UPDATE_NETWORK",
          "QUANTUM_COMPUTER_CENTRE",
          "AUTOMATISED_ASSEMBLY_CENTRE",
          "HIGH_PERFORMANCE_TRANSFORMER",
          "MICROCHIP_ASSEMBLY_LINE",
          "PRODUCTION_ASSEMBLY_HALL",
          "HIGH_PERFORMANCE_SYNTHESISER",
          "CHIP_MASS_PRODUCTION",
          "NANO_REPAIR_BOTS"
        ],
        "rocktal": [
          "MEDITATION_ENCLAVE",
          "CRYSTAL_FARM",
          "RUNE_TECHNOLOGIUM",
          "ORIKTORIUM",
          "MAGMA_FORGE",
          "DISRUPTION_CHAMBER",
          "METROPOLIS",
          "ROCKTAL_COLLECTOR",
          "CRYSTAL_REFINERY",
          "DEUTERIUM_FURNACE",
          "MEGALITH",
          "FORUM_OF_TRANSCENDENCE"
        ]
      }
    
        }
    }
    
}
