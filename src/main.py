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

translator.load_locale(configs.get("language"))

defaultBg = "#212120"
root = tk.Tk(screenName="main", baseName="main", className="main")
ttk.Style("darkly")
root.title("Last.Batch")
# width = root.winfo_screenwidth() 
# height = root.winfo_screenheight()
# root.geometry("%dx%d" % (width, height))
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
                title_info.config(text=translator.t("messages.track_info", artist=stream["artist"], track=stream["track"]))
                time.sleep(0.5)
                lastfm.network.scrobble(artist=stream["artist"], title=stream["track"], timestamp=unix_timestamp)
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
            streams_listbox.delete(0, tk.END)
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

def remove_selected():
    global streams
    selection = streams_listbox.curselection()
    if selection:
        index = selection[0]
        streams.pop(index)
        streams_listbox.delete(index)
        streams_label.config(text=translator.t("messages.streams_read", count=len(streams)))
        send_scrobbles_button.config(state="normal" if len(streams) > 0 else "disabled")

def process_streams():
    streams_label.config(text=translator.t("messages.streams_read", count=len(streams)))
    
    streams_listbox.delete(0, tk.END)
    
    for stream in streams:
        streams_listbox.insert(tk.END, f"{stream["artist"]} - {stream["track"]} ({stream["timestamp"]})")

    streams_listbox.bind('<Delete>', lambda e: remove_selected())

    send_scrobbles_button.config(state="normal" if len(streams) > 0 else "disabled")

def refresh():
    global label
    global button
    global streams_label
    global streams_listbox
    global send_scrobbles_button
    global disconnect_button
    global send_file_label
    global scrollbar
    global frame
    global menu

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

        send_file_label = ttk.Label(root, text=translator.t("messages.send_file"), font=("Arial", 10, "bold"), background=defaultBg, foreground="white")
        send_file_label.pack(pady=10)

        button = ttk.Button(root, text=translator.t("options.send_file"), command=upload_file, width=25)
        button.pack()
       
        streams_label = ttk.Label(root, text=translator.t("messages.no_file"), font=("Arial", 10), background=defaultBg, foreground="white")
        streams_label.pack(pady=5)

        frame = ttk.Frame(root)
        frame.pack()

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        streams_listbox = tk.Listbox(frame, width=100, height=20, yscrollcommand=scrollbar.set)
        streams_listbox.config(background=defaultBg, foreground="white", selectbackground="#375A7F")
        streams_listbox.pack(side="left", fill="both")
        
        scrollbar.config(command=streams_listbox.yview)

        label = ttk.Label(root, text=translator.t("messages.how_to_remove_stream"), font=("Arial", 8, "bold"), background=defaultBg, foreground="white")
        label.pack(pady=5)

        send_scrobbles_button = ttk.Button(root, text=translator.t("options.scrobble"), command=send_scrobbles, width=25)
        send_scrobbles_button.config(state="disabled")
        send_scrobbles_button.pack()

refresh()
root.mainloop()