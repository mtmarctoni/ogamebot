import json
from config.bot import CONFIG_FILE_PATH

def reload_config():
    """Reload the configuration from the config.json file."""
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)