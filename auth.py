import pylast
import os
import time
import webbrowser
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")
network = None

def is_authenticated():
    if not os.path.exists(SESSION_KEY_FILE):
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
                with open(SESSION_KEY_FILE, "w") as f:
                    f.write(session_key)
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = open(SESSION_KEY_FILE).read()

    network.session_key = session_key
    return network

def disconnect():
    os.remove(SESSION_KEY_FILE)