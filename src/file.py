from tkinter import filedialog
from typing import List, TypedDict

class StreamData(TypedDict):
    artist: str
    track: str
    timestamp: str

def upload() -> str:
    file_name = filedialog.askopenfilename(
        filetypes=[
            ("Histórico de reprodução", "*.csv;*.txt;*.json"),
        ]
    )

    if not file_name:
        return

    file = open(file_name, encoding='utf-8')
    file_content = file.read()
    file.close()

    return file_content

def process(file_content: str) -> List[StreamData]:
    lines = file_content.strip().split('\n')
    streams = []
    
    for line in lines:
        data = line.split(',')
        
        if len(data) >= 3:
            artist = data[0].strip()
            track = data[1].strip()
            timestamp = data[2].strip()
            
            streams.append({
                "artist": artist,
                "track": track,
                "timestamp": timestamp
            })

    return streams