import ttkbootstrap as ttk
import webbrowser
from i18n import translator

defaultBg = "#212120"
version = "1.0.0"

def open():
    top = ttk.Toplevel(bg=defaultBg)
    top.title(translator.t("options.about"))
    top.resizable(False, False)
    top.config(padx=10, pady=10, bg=defaultBg)
    top.grab_set()
    top.transient()

    label = ttk.Label(top, text=f"{translator.t("settings.version")}: {version}\n{translator.t("messages.developer")}", background=defaultBg, foreground="white", font=("Arial", 10))
    label.pack(padx=10, pady=10)

    button = ttk.Button(top, text="GitHub", command=lambda: webbrowser.open("https://github.com/luisgbr1el/last-batch"), width=25)
    button.pack(padx=10, pady=5)