import pylast
import os
import time
import webbrowser
from dotenv import load_dotenv
import configs

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
network = None

def is_authenticated():
    if configs.get("session_key") == None:
        return False
    else:
        return True

def authenticate():
    global network
    network = pylast.LastFMNetwork(API_KEY, API_SECRET)

    if not is_authenticated():
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()    

        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                configs.save(name="session_key", value=session_key)
                network.session_key = session_key
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = configs.get(name="session_key")

    network.session_key = session_key
    return network

def disconnect():
    configs.save(name="session_key", value=None)