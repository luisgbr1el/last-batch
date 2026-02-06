import pylast
import os
import time
import webbrowser
from dotenv import load_dotenv
import configs
from typing import TypedDict
from tkinter import messagebox
from i18n import translator

load_dotenv()

class TrackData(TypedDict):
    title: str
    artist: str
    duration: str
    cover: str
    url: str
    timestamp: str

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

def fetch_track(artist: str, title: str) -> TrackData:
    try:
        track = network.get_track(artist, title)
        title = track.get_title()
        artist = track.get_artist().get_name()
        cover = track.get_cover_image()
        url = track.get_url()

        duration = track.get_duration()
        total_seconds = duration // 1000
        minutes, seconds = divmod(total_seconds, 60)

        return {
            "title": title,
            "artist": artist,
            "duration": f"{minutes}:{seconds:02}",
            "cover": cover,
            "url": url,
            "timestamp": None
        }

    except pylast.WSError:
        messagebox.showerror(translator.t("messages.error"), translator.t("messages.error_fetching_track"))