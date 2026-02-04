import ttkbootstrap as ttk
from i18n import translator
import configs

defaultBg = "#212120"

def open(root=None, refresh_callback=None):
    top = ttk.Toplevel()
    top.title(translator.t("settings.title"))
    top.resizable(False, False)
    top.config(padx=10, pady=10, bg=defaultBg)
    top.grab_set()
    top.transient()

    label = ttk.Label(top, text=translator.t("settings.language"), background=defaultBg, foreground="white", font=("Arial", 10), anchor="w")
    label.pack(fill="x")

    lang_combo_box = ttk.Combobox(top, values=["English", "Português (Brasil)"], state="readonly")
    lang_combo_box.pack(fill="x")

    label = ttk.Label(top, text=translator.t("settings.file_format"), background=defaultBg, foreground="white", font=("Arial", 10), anchor="w")
    label.pack(fill="x")

    file_format_combo_box = ttk.Combobox(top, values=[".csv", ".json", ".txt"], state="readonly")
    file_format_combo_box.pack(fill="x")

    current_lang = configs.get(name="language")
    if current_lang is None or current_lang == "":
        current_lang = "English"
    lang_combo_box.set(current_lang)

    current_file_format = configs.get(name="file_format")
    if current_file_format is None or current_file_format == "":
        current_file_format = ".csv"
    file_format_combo_box.set(current_file_format)

    def save_and_reload():
        newLanguage = lang_combo_box.get()
        oldLanguage = configs.get(name="language")
        newFileFormat = file_format_combo_box.get()
        oldFileFormat = configs.get(name="file_format")
        
        if newLanguage != oldLanguage:
            configs.save(name="language", value=newLanguage)
            translator.load_locale(newLanguage)
            
            top.destroy()
            
            if refresh_callback:
                refresh_callback()
        elif newFileFormat != oldFileFormat:
            configs.save(name="file_format", value=newFileFormat)

            top.destroy()
        else:
            top.destroy()

    button = ttk.Button(top, text=translator.t("options.save"), command=save_and_reload, width=25)
    button.pack(pady=10)