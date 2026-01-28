from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import lastfm
import pylast
from ui import about_dialog, settings_dialog
import file
import configs
from i18n import translator

translator.load_locale(configs.get("language"))

defaultBg = "#212120"
root = tk.Tk(screenName="main", baseName="main", className="main")
root.title("Last.Batch")
# width = root.winfo_screenwidth() 
# height = root.winfo_screenheight()
# root.geometry("%dx%d" % (width, height))
root.config(bg=defaultBg, pady=10)
root.resizable(False, False)

def on_authenticate():
    lastfm.authenticate()
    label.destroy()
    button.destroy()
    refresh()

def on_disconnect():
    lastfm.disconnect()
    label.destroy()
    button.destroy()
    streams_label.destroy()
    frame.destroy()
    send_scrobbles_button.destroy()
    send_file_label.destroy()
    menu.destroy()

    refresh()

def send_scrobbles():
    global streams
    confirm = messagebox.askokcancel(translator.t("options.scrobble"), translator.t("messages.scrobble_items", count=len(streams)))

    if confirm:
        top = Toplevel(bg=defaultBg)
        top.title(translator.t("messages.scrobbling"))

        label = tk.Label(top, text=translator.t("messages.scrobbling"), bg=defaultBg, fg="white", font=("Arial", 10))
        label.pack(pady=5)
        
        progress = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate", maximum=len(streams))
        progress.pack(padx=10)

        title_info = tk.Label(top, text="", bg=defaultBg, fg="white", font=("Arial", 10))
        title_info.pack(pady=5, padx=10)
            
        counter = 0

        for stream in streams:
            counter+= 1
                
            unix_timestamp = int(time.mktime(datetime.now().timetuple()))
                
            try:
                title_info.config(text=translator.t("messages.track_info", artist=stream["artist"], track=stream["track"]))
                time.sleep(1.0)
                lastfm.network.scrobble(artist=stream["artist"], title=stream["track"], timestamp=unix_timestamp)
                progress['value'] = counter
                top.update()
            except pylast.WSError:
                messagebox.showerror(translator.t("messages.error"), translator.t("messages.error_scrobbling"))

        streams_listbox.delete(first=0, last=tk.END)
        streams = []
        send_scrobbles_button.config(state="disabled")
        streams_label.config(text=translator.t("messages.no_file"))
        top.destroy()
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

    if not lastfm.is_authenticated():
        label = tk.Label(root, text=translator.t("messages.not_logged"), bg=defaultBg, fg="white", font=("Arial", 10))
        label.pack(pady=10, padx=10)

        button = tk.Button(root, text=translator.t("options.login"), command=on_authenticate, width=25, bg=defaultBg, fg="white")
        button.pack()
    else:
        if lastfm.network is None:
            lastfm.network = pylast.LastFMNetwork(
                lastfm.API_KEY, 
                lastfm.API_SECRET,
                session_key=configs.get(name="session_key")
            )

        menu = tk.Menu(root)
        root.config(menu=menu)

        main_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Last.Batch", menu=main_menu)
        main_menu.add_command(label=translator.t("settings.title"), command=lambda: settings_dialog.open(root))
        main_menu.add_command(label=translator.t("options.logout"), command=on_disconnect)
        main_menu.add_separator()
        main_menu.add_command(label=translator.t("options.quit"), command=root.quit)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label=translator.t("options.help"), menu=help_menu)
        help_menu.add_command(label=translator.t("options.about"), command=about_dialog.open)

        send_file_label = tk.Label(root, text=translator.t("messages.send_file"), bg=defaultBg, fg="white", font=("Arial", 10, "bold"))
        send_file_label.pack(pady=10)

        button = tk.Button(root, text=translator.t("options.send_file"), command=upload_file, width=25, bg=defaultBg, fg="white")
        button.pack()
       
        streams_label = tk.Label(root, text=translator.t("messages.no_file"), bg=defaultBg, fg="white", font=("Arial", 10))
        streams_label.pack(pady=5)

        frame = tk.Frame(root, bg=defaultBg)
        frame.pack()

        scrollbar = tk.Scrollbar(frame, width=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        streams_listbox = tk.Listbox(frame, bg=defaultBg, fg="white", width=100, height=20, yscrollcommand=scrollbar.set)
        streams_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        scrollbar.config(command=streams_listbox.yview)

        label = tk.Label(root, text=translator.t("messages.how_to_remove_stream"), bg=defaultBg, fg="white", font=("Arial", 8, "bold"))
        label.pack(pady=5)

        send_scrobbles_button = tk.Button(root, text=translator.t("options.scrobble"), command=send_scrobbles, width=25, bg=defaultBg, fg="white")
        send_scrobbles_button.config(state="disabled")
        send_scrobbles_button.pack()

refresh()
root.mainloop()