import os
from datetime import datetime
import time
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
import auth
import pylast
import webbrowser

linesNumber = 0
defaultBg = "#212120"
root = tk.Tk(screenName="main", baseName="main", className="main")
root.title("Last.Batch")
# width = root.winfo_screenwidth() 
# height = root.winfo_screenheight()
# root.geometry("%dx%d" % (width, height))
root.config(bg=defaultBg, pady=10)

def on_authenticate():
    auth.authenticate()
    label.destroy()
    button.destroy()
    refresh()

def on_disconnect():
    auth.disconnect()
    label.destroy()
    button.destroy()
    streams_label.destroy()
    frame.destroy()
    send_scrobbles_button.destroy()
    send_file_label.destroy()
    menu.destroy()

    refresh()

def open_about_screen():
    top = Toplevel(bg=defaultBg)
    top.title('Sobre')

    label = tk.Label(top, text="v1.0.0\nDesenvolvido por luisgbr1el", bg=defaultBg, fg="white", font=("Arial", 10))
    label.pack(padx=10, pady=10)

    button = tk.Button(top, text="GitHub", command=lambda: webbrowser.open("https://github.com/luisgbr1el"), width=25, bg=defaultBg, fg="white")
    button.pack(padx=10, pady=5)

def send_scrobbles():
    global linesNumber
    confirm = messagebox.askokcancel("Enviar scrobbles", f"Deseja scrobblar {linesNumber} itens?")

    if confirm:
        top = Toplevel(bg=defaultBg)
        top.title('Scrobblando...')

        label = tk.Label(top, text="Scrobblando...", bg=defaultBg, fg="white", font=("Arial", 10))
        label.pack(pady=5)
        
        progress = ttk.Progressbar(top, orient="horizontal", length=300, mode="determinate", maximum=linesNumber)
        progress.pack(padx=10)

        title_info = tk.Label(top, text="", bg=defaultBg, fg="white", font=("Arial", 10))
        title_info.pack(pady=5, padx=10)
            
        counter = 0

        for line in lines:
            counter+= 1
            data = line.split(',')
                
            if len(data) >= 3:
                artist = data[0].strip()
                track = data[1].strip()
                timestamp = data[2].strip()
                unix_timestamp = int(time.mktime(datetime.now().timetuple()))
                
                try:
                    title_info.config(text=f"Música: {artist} - {track}")
                    auth.network.scrobble(artist=artist, title=track, timestamp=unix_timestamp)
                    progress['value'] = counter
                    top.update()
                except pylast.WSError:
                    messagebox.showerror("Erro", "Erro ao scrobblar. Tente novamente mais tarde.")

        streams_listbox.delete(first=0, last=tk.END)
        linesNumber = 0
        send_scrobbles_button.config(state="disabled")
        streams_label.config(text="Nenhum arquivo carregado")
        top.destroy()
        messagebox.showinfo("Sucesso", "Todos os scrobbles foram enviados com sucesso!") 
    else:
        return

def upload_file():
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
    process_file(file_content)

def remove_selected():
    selection = streams_listbox.curselection()
    if selection:
        streams_listbox.delete(selection[0])
        linesNumber = streams_listbox.size()
        streams_label.config(text=f"Streams lidos: {linesNumber}")

def process_file(file_content):
    global linesNumber
    global lines
    lines = file_content.strip().split('\n')
    linesNumber = sum(1 for line in lines)

    streams_label.config(text=f"Streams lidos: {linesNumber}")
    
    streams_listbox.delete(0, tk.END)
    
    for line in lines:
        data = line.split(',')
        
        if len(data) >= 3:
            artist = data[0].strip()
            track = data[1].strip()
            timestamp = data[2].strip()
            
            streams_listbox.insert(tk.END, f"{artist} - {track} ({timestamp})")

    streams_listbox.bind('<Delete>', lambda e: remove_selected())

    send_scrobbles_button.config(state="normal" if linesNumber > 0 else "disabled")

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

    if not auth.is_authenticated():
        label = tk.Label(root, text="Você não está autenticado no Last.fm!", bg=defaultBg, fg="white", font=("Arial", 10))
        label.pack(pady=10, padx=10)

        button = tk.Button(root, text="Autenticar-se", command=on_authenticate, width=25, bg=defaultBg, fg="white")
        button.pack()
    else:
        network = auth.authenticate()
        user = network.get_authenticated_user()

        menu = tk.Menu(root)
        root.config(menu=menu)

        account_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Conta", menu=account_menu)
        account_menu.add_command(label="Desconectar", command=on_disconnect)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=open_about_screen)

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