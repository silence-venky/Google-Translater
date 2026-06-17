import tkinter as tk
from tkinter import ttk, messagebox

from googletrans import LANGUAGES, Translator

translator = Translator()

LANGUAGE_NAMES = {"Auto": "auto"}
LANGUAGE_NAMES.update({name.title(): code for code, name in LANGUAGES.items()})

sorted_names = sorted(LANGUAGE_NAMES.keys())


def translate_text():
    source = source_text.get("1.0", tk.END).strip()
    if not source:
        messagebox.showinfo("Info", "Please enter text to translate.")
        return

    src_code = LANGUAGE_NAMES[source_lang.get()]
    dest_code = LANGUAGE_NAMES[target_lang.get()]

    try:
        result = translator.translate(source, src=src_code, dest=dest_code)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.text)
        output_text.config(state=tk.DISABLED)
        status_label.config(text=f"Translated from {result.src.upper()} to {dest_code.upper()}")
    except Exception as error:
        messagebox.showerror("Translation Error", str(error))
        status_label.config(text="Translation failed.")


def swap_languages():
    source_choice = source_lang.get()
    target_choice = target_lang.get()
    source_lang.set(target_choice)
    target_lang.set(source_choice)


def clear_text():
    source_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    status_label.config(text="Ready to translate")


root = tk.Tk()
root.title("Google Translate App")
root.geometry("820x600")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TCombobox", padding=4)
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

main_frame = ttk.Frame(root, padding=14)
main_frame.pack(fill=tk.BOTH, expand=True)

header_label = ttk.Label(main_frame, text="Google Translate", style="Header.TLabel")
header_label.grid(row=0, column=0, columnspan=4, sticky=tk.W)

separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
separator.grid(row=1, column=0, columnspan=4, sticky=tk.EW, pady=(8, 16))

source_label = ttk.Label(main_frame, text="Source language:")
source_label.grid(row=2, column=0, sticky=tk.W)
source_lang = tk.StringVar(value="Auto")
source_menu = ttk.Combobox(main_frame, textvariable=source_lang, values=sorted_names, state="readonly", width=28)
source_menu.grid(row=3, column=0, sticky=tk.W)

swap_button = ttk.Button(main_frame, text="Swap", command=swap_languages)
swap_button.grid(row=3, column=1, sticky=tk.E, padx=8)

target_label = ttk.Label(main_frame, text="Target language:")
target_label.grid(row=2, column=2, sticky=tk.W)
target_lang = tk.StringVar(value="Hindi")
target_menu = ttk.Combobox(main_frame, textvariable=target_lang, values=sorted_names, state="readonly", width=28)
target_menu.grid(row=3, column=2, sticky=tk.W)

input_frame = ttk.LabelFrame(main_frame, text="Input")
input_frame.grid(row=4, column=0, columnspan=4, pady=(16, 0), sticky=tk.NSEW)

source_text = tk.Text(input_frame, height=10, wrap=tk.WORD, borderwidth=1, relief=tk.SOLID)
source_text.grid(row=0, column=0, sticky=tk.NSEW, padx=8, pady=8)

input_scroll = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=source_text.yview)
input_scroll.grid(row=0, column=1, sticky=tk.NS, pady=8)
source_text.config(yscrollcommand=input_scroll.set)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=5, column=0, columnspan=4, pady=16, sticky=tk.EW)

translate_button = ttk.Button(button_frame, text="Translate", command=translate_text)
translate_button.pack(side=tk.LEFT)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_text)
clear_button.pack(side=tk.LEFT, padx=10)

output_frame = ttk.LabelFrame(main_frame, text="Output")
output_frame.grid(row=6, column=0, columnspan=4, sticky=tk.NSEW)

output_text = tk.Text(output_frame, height=12, wrap=tk.WORD, state=tk.DISABLED, borderwidth=1, relief=tk.SOLID)
output_text.grid(row=0, column=0, sticky=tk.NSEW, padx=8, pady=8)

output_scroll = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
output_scroll.grid(row=0, column=1, sticky=tk.NS, pady=8)
output_text.config(yscrollcommand=output_scroll.set)

status_label = ttk.Label(main_frame, text="Ready to translate")
status_label.grid(row=7, column=0, columnspan=4, sticky=tk.W, pady=(12, 0))

for index in range(4):
    main_frame.columnconfigure(index, weight=1)

input_frame.columnconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

root.mainloop()
