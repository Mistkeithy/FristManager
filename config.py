import json
import os
from typing import Any, Dict

class Config:
    def __init__(self, config_path: str = "config.json"):
        """
        comment me in english
        """
        self.config_path = config_path
        config_dir = os.path.dirname(config_path) or '.'
        os.makedirs(config_dir, exist_ok=True)
        self.settings = self.load_config()
        self.check_and_update_config()

    def load_config(self) -> Dict[str, Any]:
        """
        comment me in english
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading configuration file: {e}. Using defaults and creating default config file.")
            default_config = self.default_config()
            self.save_config(default_config)
            return default_config

    def default_config(self) -> Dict[str, Any]:
        """
        comment me in english
        """
        return {
            "localization_code": "en",
            "voices_path": "voices.db",
            "token_path": "token.txt",
            "log_path": "bot.log",
            "log_verb_level": 3,
            "log_debug": False,
            "cmd_prefix": "/",
            "game_activity": "Powered by FristManager",
            "extension_path": "./cogs",
            "welcome": True,
            "ffmpeg_path": "ffmpeg",
            "thread_path": "thread.json",
            "reactions_path": "reactions.json"
        }
    
    def check_and_update_config(self):
        """
        comment me in english
        """
        default_config = self.default_config()
        updated = False
        for key, value in default_config.items():
            if key not in self.settings:
                self.settings[key] = value
                updated = True
                print(f"Key '{key}' was missing and has been added with the default value.")
        if updated:
            self.save_config()
            
    def save_config(self, config=None):
        """
        Saves the given configuration to the configuration file.
        If no configuration is provided, saves the current settings.
        """
        if config is None:
            config = self.settings
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Failed to save configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        comment me in english
        """
        return self.settings.get(key, default)