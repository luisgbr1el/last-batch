import tkinter as tk
from tkinter import Toplevel
import webbrowser

defaultBg = "#212120"

def open():
    top = Toplevel(bg=defaultBg)
    top.title('Sobre')
    top.resizable(False, False)

    label = tk.Label(top, text="v1.0.0\nDesenvolvido por luisgbr1el", bg=defaultBg, fg="white", font=("Arial", 10))
    label.pack(padx=10, pady=10)

    button = tk.Button(top, text="GitHub", command=lambda: webbrowser.open("https://github.com/luisgbr1el"), width=25, bg=defaultBg, fg="white")
    button.pack(padx=10, pady=5)