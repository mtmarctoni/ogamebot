from flask import Flask, request, jsonify
import json
from threading import Thread
from typing import cast

from config.types import ConfigType
from config.bot import CONFIG_FILE_PATH as config_file_path, DEFAULT_CONFIG

app = Flask(__name__)

# Global variable to simulate bot runtime behavior
bot_runtime_config: ConfigType = cast(ConfigType, {})

def load_config() -> ConfigType:
    try:
        with open(config_file_path, 'r') as file:
            config = json.load(file)
            # print("[Debug] Loaded configuration:", config)  # Debug log
            return config
    except FileNotFoundError:
        print("[Error] Config file not found. Creating a default configuration.")
        default_config = DEFAULT_CONFIG
        save_config(default_config)
        return default_config
    except json.JSONDecodeError:
        print("[Error] Config file is invalid. Using default configuration.")
        return {
            "check_interval": 10,
            "enable_resource_upgrades": True,
            "enable_energy_upgrades": True,
            "enable_facility_upgrades": True,
            "enable_research_upgrades": True,
            "enable_storage_upgrades": True,
            "enable_lifeform_upgrades": True,
            "enable_expeditions": True
        }

def save_config(config: ConfigType):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

def apply_runtime_config():
    global bot_runtime_config
    bot_runtime_config = load_config()
    print("\n[Bot] Current Configuration:")
    print("[Bot] =============================")
    for key, value in bot_runtime_config.items():
         print(f"[Bot] {key}: {value}")
    print("[Bot] =============================\n")

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/config', methods=['POST'])
def update_config():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    config = load_config()
    config.update(data)
    save_config(config)
    apply_runtime_config()  # Apply changes to the bot runtime
    return jsonify({"message": "Configuration updated and applied successfully."})

@app.route('/command', methods=['POST'])
def execute_command():
    """Endpoint to execute specific commands like disabling expeditions."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    command = data.get("command")

    if command == "disable expeditions":
        bot_runtime_config["enable_expeditions"] = False
        save_config(bot_runtime_config)
        apply_runtime_config()
        return jsonify({"message": "Expeditions disabled successfully."})

    return jsonify({"error": "Unknown command."}, 400)

# Simulate the bot's main loop

def bot_main_loop():
    last_config = None

    while True:
        if bot_runtime_config != last_config:
            last_config = bot_runtime_config

if __name__ == '__main__':
    apply_runtime_config()  # Load the configuration when the app starts
    # Start the bot in a separate thread
    Thread(target=bot_main_loop, daemon=True).start()
    app.run(debug=True)