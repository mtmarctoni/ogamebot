
from config.types import ConfigType

# Config.json path
CONFIG_FILE_PATH: str = "config.json"

DEFAULT_CONFIG: ConfigType = {
    "check_interval": 10,
    "enable_resource_upgrades": True,
    "enable_energy_upgrades": True,
    "enable_facility_upgrades": True,
    "enable_research_upgrades": True,
    "enable_storage_upgrades": True,
    "enable_lifeform_upgrades": True,
    "enable_expeditions": True,
    "expedition_planet_id": "33632165" # Nexus Sentinel
}