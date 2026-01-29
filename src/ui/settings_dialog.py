import tkinter as tk
from tkinter import Toplevel, ttk
from i18n import translator
import configs

defaultBg = "#212120"

def open(root=None, refresh_callback=None):
    top = Toplevel(bg=defaultBg)
    top.title(translator.t("settings.title"))
    top.resizable(False, False)
    top.config(padx=10, pady=10)
    top.grab_set()
    top.transient()
    top.focus_set()

    label = tk.Label(top, text=translator.t("settings.language"), bg=defaultBg, fg="white", font=("Arial", 10), anchor="w")
    label.pack(fill="x")

    lang_combo_box = ttk.Combobox(top, values=["English", "Português (Brasil)"], state="readonly")
    lang_combo_box.pack(fill="x")

    current_lang = configs.get(name="language")
    if current_lang is None or current_lang == "":
        current_lang = "English"
    lang_combo_box.set(current_lang)

    def save_and_reload():
        newLanguage = lang_combo_box.get()
        oldLanguage = configs.get(name="language")
        
        if newLanguage != oldLanguage:
            configs.save(name="language", value=newLanguage)
            translator.load_locale(newLanguage)
            
            top.destroy()
            
            if refresh_callback:
                refresh_callback()
        else:
            top.destroy()

    button = tk.Button(top, text=translator.t("options.save"), command=save_and_reload, width=25, bg=defaultBg, fg="white")
    button.pack(pady=10)