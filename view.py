import tkinter as tk
from tkinter import filedialog, PhotoImage
import webbrowser

from constants import BACKGROUND, STYLE, STYLE_ENTRY, STYLE_BUTTON
from model import runScript

def open_url():
    webbrowser.open('https://github.com/agusaenz/isaac-save-auto-editor-steam?tab=readme-ov-file#4-obtain-a-steam-web-api-key')

def browse_file(var):
    file_path = filedialog.askopenfilename(filetypes=[("DAT Files", "*.dat"), ("All Files", "*.*")])
    if file_path:
        var.set(file_path)

def main():
    root = tk.Tk()
    root.title("Post-it for Dummies")
    root.configure(bg=BACKGROUND)

    root.iconbitmap(r"assets\rune_05_ansuz.ico")

    file_var = tk.StringVar()

    tk.Label(root, text="Steam ID:", **STYLE).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry1 = tk.Entry(root, width=40, **STYLE_ENTRY)
    entry1.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Steam Web API key:", **STYLE).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry2 = tk.Entry(root, width=40, **STYLE_ENTRY)
    entry2.grid(row=1, column=1, padx=10, pady=5)

    questionimage = PhotoImage(file=r"assets\questionmark.png")
    tk.Button(root,image= questionimage, relief=tk.FLAT,**STYLE_BUTTON, command= open_url).grid(row=1, column= 2, padx=10, pady=5)

    tk.Label(root, text="Select Save File:", **STYLE).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(root, textvariable=file_var, width=40, **STYLE_ENTRY).grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(file_var), **STYLE_BUTTON).grid(row=2, column=2, padx=10, pady=5)

    tk.Button(
        root, text="Run Script", command=lambda: runScript(entry1.get(), entry2.get(), file_var.get()), **STYLE_BUTTON
    ).grid(row=3, column=1, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
