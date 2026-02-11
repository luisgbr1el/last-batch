import json
import os
import sys
from typing import Dict

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALES_DIR = os.path.join(get_base_path(), "i18n", "locales")
current_locale = "en"
translations: Dict[str, any] = {}

def _load_json_file(locale_code: str) -> Dict:
    locale_file = os.path.join(LOCALES_DIR, f"{locale_code}.json")
    if os.path.exists(locale_file):
        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler arquivo de tradução: {e}")
            return {}
    return {}

def load_locale(locale: str):
    if locale == "English":
        locale_code = "en"
    elif locale == "Português (Brasil)":
        locale_code = "pt_BR"
    elif locale is None:
        locale_code = "en"
    else:
        locale_code = locale if locale in ["en", "pt_BR"] else "en"
        
    global current_locale, translations
    
    try:
        loaded_translations = _load_json_file(locale_code)
        
        if loaded_translations:
            translations = loaded_translations
            current_locale = locale_code
        else:
            translations = _load_json_file("en")
            current_locale = "en"
            
    except Exception:
        translations = _load_json_file("en")
        current_locale = "en"

def t(key: str, **kwargs) -> str:
    keys = key.split(".")
    value = translations
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            break
    
    if isinstance(value, str) and kwargs:
        try:
            return value.format(**kwargs)
        except KeyError:
            return value
    
    return value if isinstance(value, str) else key

def get_current_locale() -> str:
    return current_locale

def get_available_locales() -> list:
    locales = []
    try:
        if os.path.exists(LOCALES_DIR):
            for file in os.listdir(LOCALES_DIR):
                if file.endswith(".json"):
                    locales.append(file.replace(".json", ""))
    except Exception:
        pass
    return locales

try:
    translations = _load_json_file("en")
except:
    translations = {}