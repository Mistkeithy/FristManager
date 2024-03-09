import json
from typing import Any, Dict

class Config:
    def __init__(self, config_path: str = "config.json"):
        """
        comment me
        """
        self.config_path = config_path
        self.settings = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        comment me
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading configuration file: {e}. Using defaults.")
            return self.default_config()

    def default_config(self) -> Dict[str, Any]:
        """
        Default config comment me
        """
        return {
            "localization_code": "en",
            "voices_path": "voices.db",
            "token_path": "token.txt",
            "log_path": "bot.log",
            "log_verb_level": 3,
            "log_debug": 1,
            "cmd_prefix": "/",
            "game_activity": "Powered by FristManager",
            "extension_path": "./cogs"
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        comment me
        """
        return self.settings.get(key, default)