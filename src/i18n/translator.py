import json
import os
from typing import Dict

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")
current_locale = "en"
translations: Dict[str, any] = {}

def load_locale(locale: str):
    if locale == "English":
        locale = "en"
    else:
        locale = "pt_BR"
        
    global current_locale, translations
    
    locale_file = os.path.join(LOCALES_DIR, f"{locale}.json")
    
    if not os.path.exists(locale_file):
        locale = "en"
        locale_file = os.path.join(LOCALES_DIR, f"{locale}.json")
    
    with open(locale_file, "r", encoding="utf-8") as f:
        translations = json.load(f)
    
    current_locale = locale

def t(key: str, **kwargs) -> str:
    keys = key.split(".")
    value = translations
    
    for k in keys:
        value = value.get(k, key)
        if not isinstance(value, dict):
            break
    
    if isinstance(value, str) and kwargs:
        return value.format(**kwargs)
    
    return value if isinstance(value, str) else key

def get_current_locale() -> str:
    return current_locale

def get_available_locales() -> list:
    locales = []
    for file in os.listdir(LOCALES_DIR):
        if file.endswith(".json"):
            locales.append(file.replace(".json", ""))
    return locales