from flask import Flask, request, jsonify
import json

from typings import ConfigType
from config import CONFIG_FILE_PATH as config_file_path

app = Flask(__name__)
config_file_path = "config.json"

def load_config():
    with open(config_file_path, 'r') as file:
        return json.load(file)


def save_config(config: ConfigType):
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/config', methods=['POST'])
def update_config():
    data = request.json
    config = load_config()
    config.update(data)
    save_config(config)
    return jsonify({"message": "Configuration updated successfully."})

if __name__ == '__main__':
    app.run(debug=True)