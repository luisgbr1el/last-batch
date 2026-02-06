from tkinter import messagebox
import tkinter as tk
import ttkbootstrap as ttk
from lastfm import TrackData
import requests
from io import BytesIO
from PIL import Image, ImageTk
import threading
import webbrowser
from tksvg import SvgImage
import os
from typing import Dict, Callable, List

defaultBg = "#171716"

def add(frame: ttk.Frame, track: TrackData, index: int, streams: List[Dict[str, str]], refresh_callback: Callable) -> ttk.Frame:
    track_frame = ttk.Frame(frame)
    track_frame.pack(padx=10, pady=10, fill="x", expand=True)

    position_frame = ttk.Frame(track_frame)
    position_frame.pack(side="left", padx=(0, 10))

    position_label = tk.Label(position_frame, text=f"{index}.", bg=defaultBg, fg="white", font=("Arial", 10))
    position_label.pack()

    cover_frame = ttk.Frame(track_frame)
    cover_frame.pack(side="left", padx=(0, 10))

    cover_label = tk.Label(cover_frame, text="...", bg=defaultBg, fg="white", width=50, height=50)
    cover_label.pack()

    def load_image():
        try:
            response = requests.get(track["cover"])
            image = Image.open(BytesIO(response.content))
            image = image.resize((50, 50), Image.LANCZOS)
            cover_image = ImageTk.PhotoImage(image)
            
            cover_label.after(0, lambda: cover_label.config(image=cover_image, text=""))
            cover_label.after(0, lambda: setattr(cover_label, 'image', cover_image))
        except:
            cover_label.after(0, lambda: cover_label.config(text="X", width=7, height=3))
    
    threading.Thread(target=load_image, daemon=True).start()

    info_frame = ttk.Frame(track_frame)
    info_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

    title_label = ttk.Label(info_frame, text=track["title"], font=("Arial", 10, "bold"))
    title_label.pack(anchor="w")

    artist_label = ttk.Label(info_frame, text=track["artist"], font=("Arial", 9))
    artist_label.pack(anchor="w")

    duration_label = ttk.Label(info_frame, text=track["duration"], font=("Arial", 9), foreground="gray")
    duration_label.pack(anchor="w")

    timestamp_frame = ttk.Frame(track_frame)
    timestamp_frame.pack(side="left", fill="x", padx=(0, 20))

    timestamp_label = ttk.Label(timestamp_frame, text=track["timestamp"], font=("Arial", 9))
    timestamp_label.pack(anchor="w")

    actions_frame = ttk.Frame(track_frame)
    actions_frame.pack(side="right")

    delete_icon_path = os.path.join(os.path.dirname(__file__), "assets", "delete.svg")
    delete_icon = SvgImage(file=delete_icon_path, scaletoheight=15)
    delete_button = ttk.Button(actions_frame, bootstyle="danger", image=delete_icon, width=4, command=lambda: remove(index, streams, refresh_callback))
    delete_button.image = delete_icon
    delete_button.pack(pady=2)

    lastfm_icon_path = os.path.join(os.path.dirname(__file__), "assets", "lastfm.svg")
    lastfm_icon = SvgImage(file=lastfm_icon_path, scaletoheight=15)
    lastfm_button = ttk.Button(actions_frame, image=lastfm_icon, width=4, command=lambda: webbrowser.open(track["url"]))
    lastfm_button.image = lastfm_icon
    lastfm_button.pack(pady=2)

    return track_frame

def remove(index: int, streams: List[Dict[str, str]], refresh_callback: Callable):
    streams.pop(index-1)
    refresh_callback()