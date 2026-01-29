from tkinter import filedialog
from typing import List, TypedDict
from i18n import translator
import configs
import json

class StreamData(TypedDict):
    artist: str
    track: str
    timestamp: str

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
    
    if file_format in (".csv", ".txt"):
        lines = file_content.strip().split('\n')

        for line in lines:
            data = line.split(f',' if file_format == ".csv" else ";")
            
            if len(data) >= 3:
                artist = data[0].strip()
                track = data[1].strip()
                timestamp = data[2].strip()
                
                streams.append({
                    "artist": artist,
                    "track": track,
                    "timestamp": timestamp
                })
    else:
        streams = json.loads(file_content)

    return streams