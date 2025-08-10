import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE)

    def load_settings(self):
        default_settings = {
            "round_time": 5,
            "best_of": 3
        }
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                try:
                    settings = json.load(f)
                    return settings
                except json.JSONDecodeError:
                    return default_settings
        return default_settings

    def save_settings(self, settings):
        with open(self.config_path, "w") as f:
            json.dump(settings, f, indent=4)