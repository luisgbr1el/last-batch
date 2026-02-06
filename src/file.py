from tkinter import filedialog
import ttkbootstrap as ttk
from typing import List, TypedDict
from i18n import translator
import configs
import json
import lastfm
import time

class StreamData(TypedDict):
    artist: str
    track: str
    timestamp: str

defaultBg = "#212120"

def upload() -> str:
    file_format = configs.get("file_format")

    file_name = filedialog.askopenfilename(
        filetypes=[
            (translator.t("messages.playback_history"), f"*{file_format}"),
        ]
    )

    if not file_name:
        return

    file = open(file_name, encoding='utf-8')
    file_content = file.read()
    file.close()

    return file_content

def process(file_content: str) -> List[StreamData]:
    file_format = configs.get("file_format")
    streams = []

    top = ttk.Toplevel(bg=defaultBg)
    top.title(translator.t("messages.fetching"))

    label = ttk.Label(top, text=translator.t("messages.fetching"), font=("Arial", 10), background=defaultBg, foreground="white")
    label.pack(pady=5)
    
    if file_format in (".csv", ".txt"):
        lines = file_content.strip().split('\n')

        progress = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate", maximum=len(lines))
        progress.pack(padx=10)

        title_info = ttk.Label(top, text="", font=("Arial", 10), background=defaultBg, foreground="white")
        title_info.pack(pady=5, padx=10)

        counter = 0

        for line in lines:
            data = line.split(f',' if file_format == ".csv" else ";")
            
            if len(data) >= 3:
                counter+= 1
                artist = data[0].strip()
                title = data[1].strip()
                timestamp = data[2].strip()

                track_data = lastfm.fetch_track(artist, title=title)
                time.sleep(0.5)
                track_data["timestamp"] = timestamp

                title_info.config(text=translator.t("messages.track_info", artist=track_data["artist"], track=track_data["title"]))

                streams.append(track_data)

                progress['value'] = counter
                top.update()
    else:
        streams = json.loads(file_content)
    
    top.destroy()
    return streams