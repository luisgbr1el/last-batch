from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import lastfm
import pylast
from ui import about_dialog, settings_dialog
import file
import configs

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
    confirm = messagebox.askokcancel("Enviar scrobbles", f"Deseja scrobblar {len(streams)} itens?")

    if confirm:
        top = Toplevel(bg=defaultBg)
        top.title('Scrobblando...')

        label = tk.Label(top, text="Scrobblando...", bg=defaultBg, fg="white", font=("Arial", 10))
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
                title_info.config(text=f"Música: {stream["artist"]} - {stream["track"]}")
                # lastfm.network.scrobble(artist=stream["artist"], title=stream["track"], timestamp=unix_timestamp)
                progress['value'] = counter
                top.update()
            except pylast.WSError:
                messagebox.showerror("Erro", "Erro ao scrobblar. Tente novamente mais tarde.")

        streams_listbox.delete(first=0, last=tk.END)
        streams = []
        send_scrobbles_button.config(state="disabled")
        streams_label.config(text="Nenhum arquivo carregado")
        top.destroy()
        messagebox.showinfo("Sucesso", "Todos os scrobbles foram enviados com sucesso!") 
    else:
        return

def upload_file():
    global streams
    file_content = file.upload()
    if file_content:
        streams = file.process(file_content)
        process_streams()

def remove_selected():
    selection = streams_listbox.curselection()
    if selection:
        streams_listbox.delete(selection[0])
        linesNumber = streams_listbox.size()
        streams_label.config(text=f"Streams lidos: {linesNumber}")

def process_streams():
    streams_label.config(text=f"Streams lidos: {len(streams)}")
    
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
        label = tk.Label(root, text="Você não está autenticado no Last.fm!", bg=defaultBg, fg="white", font=("Arial", 10))
        label.pack(pady=10, padx=10)

        button = tk.Button(root, text="Autenticar-se", command=on_authenticate, width=25, bg=defaultBg, fg="white")
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
        main_menu.add_command(label="Configurações", command=settings_dialog.open)
        main_menu.add_command(label="Sair da conta", command=on_disconnect)
        main_menu.add_separator()
        main_menu.add_command(label="Fechar", command=root.quit)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=about_dialog.open)

        send_file_label = tk.Label(root, text="Envie um arquivo abaixo para processar.", bg=defaultBg, fg="white", font=("Arial", 10, "bold"))
        send_file_label.pack(pady=10)

        button = tk.Button(root, text="Enviar arquivo", command=upload_file, width=25, bg=defaultBg, fg="white")
        button.pack()
       
        streams_label = tk.Label(root, text="Nenhum arquivo carregado", bg=defaultBg, fg="white", font=("Arial", 10))
        streams_label.pack(pady=5)

        frame = tk.Frame(root, bg=defaultBg)
        frame.pack()

        scrollbar = tk.Scrollbar(frame, width=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        streams_listbox = tk.Listbox(frame, bg=defaultBg, fg="white", width=100, height=20, yscrollcommand=scrollbar.set)
        streams_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        scrollbar.config(command=streams_listbox.yview)

        label = tk.Label(root, text="Obs: Para remover um stream, selecione um elemento e pressione o botão Delete.", bg=defaultBg, fg="white", font=("Arial", 8, "bold"))
        label.pack(pady=5)

        send_scrobbles_button = tk.Button(root, text="Scrobblar", command=send_scrobbles, width=25, bg=defaultBg, fg="white")
        send_scrobbles_button.config(state="disabled")
        send_scrobbles_button.pack()

refresh()
root.mainloop()