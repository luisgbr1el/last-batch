import os
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".lastbatch_config.json")

def load():
    if not os.path.exists(CONFIG_FILE):
        return {"session_key": None, "language": "English"}
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            configs = json.load(f)

            if "language" not in configs:
                configs["language"] = "English"
            if "session_key" not in configs:
                configs["session_key"] = None

            return configs
    except:
        return {"session_key": None, "language": "English"}

def save(name: str, value: str | None):
    configs = load()
    
    configs[name] = value
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(configs, f, indent=2)

def get(name: str) -> str | None:
    configs = load()
    return configs.get(name)