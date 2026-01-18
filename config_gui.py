from flask import Flask, request, jsonify
import json
from threading import Thread
from typing import cast

from config.types import ConfigRawType, ConfigType
from config.bot import CONFIG_FILE_PATH as config_file_path, DEFAULT_CONFIG

app = Flask(__name__)

# Global variable to simulate bot runtime behavior
bot_runtime_config: ConfigType = cast(ConfigType, {})

def load_config() -> ConfigRawType:
    """Safely load the current config, guarantee all required keys."""
    try:
        with open(config_file_path, 'r') as file:
            config = json.load(file)
            # Fill missing fields from DEFAULT_CONFIG, but never remove extras
            merged = deep_merge(DEFAULT_CONFIG, config)
            return merged
    except (FileNotFoundError, json.JSONDecodeError):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config: ConfigRawType):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def deep_merge(
    base: ConfigRawType,
    override: ConfigRawType
) -> ConfigRawType:
    """Recursively merges `override` into `base`, keeps all unknown/base keys."""
    merged = dict(base)
    for k, v in override.items():
        if (
            k in merged and
            isinstance(merged[k], dict) and
            isinstance(v, dict)
        ):
            merged[k] = deep_merge(merged[k], v)  # type: ignore
        else:
            merged[k] = v
    return merged  # type: ignore

def apply_runtime_config():
    global bot_runtime_config
    raw_config = load_config()
    # Convert raw_config (ConfigRawType) to ConfigType by mapping string IDs to enums/classes
    config: ConfigType = cast(ConfigType, dict(raw_config))


    bot_runtime_config = config
    print("\n[INFO] Current Bot Configuration:")
    print("[INFO] ==================================")
    for key, value in bot_runtime_config.items():
        print(f"[INFO] {key}: {value}")
    print("[INFO] ==================================\n")

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/config', methods=['POST'])
def update_config():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    current = load_config()
    # Deep merge so we don't lose keys
    updated = deep_merge(current, data)
    save_config(updated)
    apply_runtime_config()  # Apply changes to the bot runtime
    return jsonify({"message": "Configuration updated and applied successfully."})

@app.route('/command', methods=['POST'])
def execute_command():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    command = data.get("command")

    if command == "disable expeditions":
        current = load_config()
        expeditions = current.get("expeditions", {})
        expeditions["enable_expeditions"] = False
        current["expeditions"] = expeditions
        save_config(current)
        apply_runtime_config()
        return jsonify({"message": "Expeditions disabled successfully."})
    return jsonify({"error": "Unknown command."}), 400

# Simulate the bot's main loop (does nothing)
def bot_main_loop():
    last_config = None
    while True:
        if bot_runtime_config != last_config:
            last_config = bot_runtime_config
        # Could add a sleep or status check if needed

if __name__ == '__main__':
    apply_runtime_config()
    Thread(target=bot_main_loop, daemon=True).start()
    app.run(debug=True)
