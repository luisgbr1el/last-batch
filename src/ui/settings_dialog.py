import tkinter as tk
from tkinter import Toplevel, ttk
import webbrowser
import configs

defaultBg = "#212120"

def open():
    global lang_combo_box
    top = Toplevel(bg=defaultBg)
    top.title('Configurações')
    top.resizable(False, False)
    top.config(padx=10, pady=10)

    label = tk.Label(top, text="Idioma", bg=defaultBg, fg="white", font=("Arial", 10), anchor="w")
    label.pack(fill="x")

    lang_combo_box = ttk.Combobox(top, values=["English", "Português"], state="readonly")
    lang_combo_box.pack(fill="x")

    lang_combo_box.set(configs.get(name="language"))

    button = tk.Button(top, text="Salvar", command=lambda: (save_settings(), top.destroy()), width=25, bg=defaultBg, fg="white")
    button.pack(pady=10)

def save_settings():
    newLanguage = lang_combo_box.get()
    configs.save(name="language", value=newLanguage)