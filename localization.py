import json
from typing import Dict

class Localization:
    def __init__(self, language: str = "en"):
        """
        comment me in english
        """
        self.language = language
        self.translations = self.load_translations()

    def load_translations(self) -> Dict:
        """
        comment me in english
        """
        try:
            with open(f"locales/{self.language}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Translation file for {self.language} not found. Falling back to English.")
            self.language = "en"
            try:
                with open(f"locales/en.json", "r", encoding="utf-8") as file:
                    return json.load(file)
            except FileNotFoundError:
                raise Exception("Default translation file (en.json) not found.")
    
    def get(self, key: str, **kwargs) -> str:
        """
        comment me in english
        """
        return self.translations.get(key, key).format(**kwargs)