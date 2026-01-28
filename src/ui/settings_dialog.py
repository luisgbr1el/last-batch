import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
from i18n import translator
import configs

defaultBg = "#212120"

def open(root=None):
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

    lang_combo_box.set(configs.get(name="language"))

    def save_and_reload():
        newLanguage = lang_combo_box.get()
        oldLanguage = configs.get(name="language")
        
        if newLanguage != oldLanguage:
            configs.save(name="language", value=newLanguage)
            translator.load_locale(newLanguage)
            
            messagebox.showinfo(
                translator.t("settings.title"), 
                translator.t("messages.restart_required")
            )
            
            top.destroy()
            
            if root:
                root.destroy()
                import subprocess
                import sys
                subprocess.Popen([sys.executable] + sys.argv)
        else:
            top.destroy()

    button = tk.Button(top, text=translator.t("options.save"), command=save_and_reload, width=25, bg=defaultBg, fg="white")
    button.pack(pady=10)