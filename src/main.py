from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import lastfm
import pylast
from ui import about_dialog, settings_dialog
import file
import configs
from i18n import translator
import requests
import webbrowser
import sys
import os
import streams_list

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

translator.load_locale(configs.get("language"))

defaultBg = "#212120"

root = ttk.Window()
ttk.Style("darkly")
root.title("Last.Batch")

root.config(bg=defaultBg, pady=10)
root.resizable(False, False)

def on_authenticate():
    lastfm.authenticate()
    refresh()

def on_disconnect():
    confirm = messagebox.askyesno(translator.t("options.logout"), translator.t("messages.confirm_logout"))
    
    if confirm == True:
        lastfm.disconnect()
        refresh()
    else:
        return

def send_scrobbles():
    global streams
    confirm = messagebox.askyesno(translator.t("options.scrobble"), translator.t("messages.scrobble_items", count=len(streams)))

    if confirm == True:
        top = ttk.Toplevel(bg=defaultBg)
        top.title(translator.t("messages.scrobbling"))

        label = ttk.Label(top, text=translator.t("messages.scrobbling"), font=("Arial", 10), background=defaultBg, foreground="white")
        label.pack(pady=5)
        
        progress = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate", maximum=len(streams))
        progress.pack(padx=10)

        title_info = ttk.Label(top, text="", font=("Arial", 10), background=defaultBg, foreground="white")
        title_info.pack(pady=5, padx=10)
            
        counter = 0
        successful_indices = []
        failed_count = 0

        for i, stream in enumerate(streams):
            counter+= 1

            timestamp = datetime.strptime(stream['timestamp'], '%Y-%m-%d %H:%M:%S')
            unix_timestamp = int(time.mktime(timestamp.timetuple()))

            try:
                title_info.config(text=translator.t("messages.track_info", artist=stream["artist"], track=stream["title"]))
                time.sleep(0.5)
                lastfm.network.scrobble(artist=stream["artist"], title=stream["title"], timestamp=unix_timestamp)
                successful_indices.append(i)
                progress['value'] = counter
                top.update()
            except pylast.WSError:
                failed_count += 1
                progress['value'] = counter
                top.update()

        for index in reversed(successful_indices):
            streams.pop(index)

        if len(streams) > 0:
            process_streams()
        else:
            streams_label.config(text=translator.t("messages.no_file"))
            send_scrobbles_button.config(state="disabled")

        top.destroy()

        if failed_count > 0:
            messagebox.showwarning(translator.t("messages.error"), translator.t("messages.success_with_errors", count=failed_count))
        if len(successful_indices) > 0:
            messagebox.showinfo(translator.t("messages.success"), translator.t("messages.success_scrobbling"))
    else:
        return

def upload_file():
    global streams
    file_content = file.upload()
    if file_content:
        streams = file.process(file_content)
        process_streams()

def process_streams():
    for widget in streams_frame.winfo_children():
        widget.destroy()
    
    streams_label.config(text=translator.t("messages.streams_read", count=len(streams)))

    index = 0
    
    for stream in streams:
        index += 1
        streams_list.add(frame=streams_frame, track=stream, index=index, streams=streams, refresh_callback=process_streams)

    send_scrobbles_button.config(state="normal" if len(streams) > 0 else "disabled")

def parse_version(name: str) -> list[int]:
    version = name.split(".")
    version = [int(number) for number in version]
    return version

def check_for_updates(user_request: bool):
    try:
        current_version = about_dialog.version
        response = requests.get("https://api.github.com/repos/luisgbr1el/last-batch/releases/latest", timeout=10)
        latest_version = parse_version(response.json()["name"])

        if latest_version > current_version:
            confirm = messagebox.askyesno(translator.t("settings.update"), translator.t("messages.update_available"))

            if confirm == True:
                webbrowser.open("https://github.com/luisgbr1el/last-batch/releases/latest")
        else:
            if user_request == True:
                messagebox.showinfo(translator.t("settings.update"), translator.t("messages.no_updates"))

        return
    except:
        if user_request == True:
            messagebox.showerror(translator.t("messages.error"), translator.t("messages.error_checking_updates"))
            
        return

def refresh():
    global label
    global button
    global streams_label
    global send_scrobbles_button
    global disconnect_button
    global send_file_label
    global scrollbar
    global frame
    global menu
    global streams_frame

    for widget in root.winfo_children():
        widget.destroy()

    if not lastfm.is_authenticated():
        label = ttk.Label(root, text=translator.t("messages.not_logged"), font=("Arial", 10), background=defaultBg, foreground="white")
        label.pack(pady=10, padx=10)

        button = ttk.Button(root, text=translator.t("options.login"), command=on_authenticate, width=25)
        button.pack()
    else:
        if lastfm.network is None:
            lastfm.network = pylast.LastFMNetwork(
                lastfm.API_KEY, 
                lastfm.API_SECRET,
                session_key=configs.get(name="session_key")
            )

        menu = ttk.Menu(root)
        root.config(menu=menu)

        main_menu = ttk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Last.Batch", menu=main_menu)
        main_menu.add_command(label=translator.t("settings.title"), command=lambda: settings_dialog.open(root, refresh))
        main_menu.add_command(label=translator.t("options.logout"), command=on_disconnect)
        main_menu.add_separator()
        main_menu.add_command(label=translator.t("options.quit"), command=root.quit)

        help_menu = ttk.Menu(menu, tearoff=0)
        menu.add_cascade(label=translator.t("options.help"), menu=help_menu)
        help_menu.add_command(label=translator.t("options.about"), command=about_dialog.open)
        help_menu.add_command(label=translator.t("options.check_for_updates"), command=lambda: check_for_updates(user_request=True))

        send_file_label = ttk.Label(root, text=translator.t("messages.send_file"), font=("Arial", 10, "bold"), background=defaultBg, foreground="white")
        send_file_label.pack(pady=10)

        button = ttk.Button(root, text=translator.t("options.send_file"), command=upload_file, width=25)
        button.pack()
       
        streams_label = ttk.Label(root, text=translator.t("messages.no_file"), font=("Arial", 10), background=defaultBg, foreground="white")
        streams_label.pack(pady=5)

        frame = ttk.Frame(root)
        frame.pack()

        canvas = tk.Canvas(frame, width=700, height=400)
        canvas.pack(pady=5)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        
        streams_frame = ttk.Frame(canvas)
        
        canvas.create_window((0, 0), window=streams_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        streams_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        send_scrobbles_button = ttk.Button(root, text=translator.t("options.scrobble"), command=send_scrobbles, width=25)
        send_scrobbles_button.config(state="disabled")
        send_scrobbles_button.pack()
        check_for_updates(user_request=False)

refresh()
root.mainloop()