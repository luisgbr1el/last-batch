import tkinter as tk
from tkinter import Toplevel
import webbrowser
from i18n import translator

defaultBg = "#212120"
version = "1.0.0"

def open():
    top = Toplevel(bg=defaultBg)
    top.title(translator.t("options.about"))
    top.resizable(False, False)
    top.grab_set()
    top.transient()
    top.focus_set()

    label = tk.Label(top, text=f"{translator.t("settings.version")}: {version}\n{translator.t("messages.developer")}", bg=defaultBg, fg="white", font=("Arial", 10))
    label.pack(padx=10, pady=10)

    button = tk.Button(top, text="GitHub", command=lambda: webbrowser.open("https://github.com/luisgbr1el/last-batch"), width=25, bg=defaultBg, fg="white")
    button.pack(padx=10, pady=5)