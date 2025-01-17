import tkinter as tk
from tkinter import filedialog, PhotoImage, ttk, messagebox
import webbrowser
import winsound

from constants import BACKGROUND, STYLE, STYLE_ENTRY, STYLE_BUTTON
import model

root = tk.Tk()

def main():
    root.title("Post-it for Dummies")
    root.configure(bg=BACKGROUND)

    root.iconbitmap(r"assets/rune_05_ansuz.ico")

    file_var = tk.StringVar()

    tk.Label(root, text="Steam ID:", **STYLE).grid(row=0, column=0, padx=10, pady=(16.69420,5), sticky="w")
    entry1 = tk.Entry(root, width=40, **STYLE_ENTRY)
    entry1.grid(row=0, column=1, padx=10, pady=(16.69420,5))

    tk.Label(root, text="Steam Web API key:", **STYLE).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry2 = tk.Entry(root, width=40, **STYLE_ENTRY)
    entry2.grid(row=1, column=1, padx=10, pady=5)

    questionimage = PhotoImage(file=r"assets/questionmark.png")
    tk.Button(root,image= questionimage, relief=tk.FLAT,**STYLE_BUTTON, command= open_url).grid(row=1, column= 2, padx=10, pady=5)

    tk.Label(root, text="Select Save File:", **STYLE).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(root, textvariable=file_var, width=40, **STYLE_ENTRY).grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(file_var), **STYLE_BUTTON).grid(row=2, column=2, padx=10, pady=5)

    tk.Button(
        root, text="Run Script", command=lambda: runScript(entry1.get(), entry2.get(), file_var.get()), **STYLE_BUTTON
    ).grid(row=3, column=1, pady=20)

    root.mainloop()

def open_url():
    webbrowser.open('https://github.com/agusaenz/isaac-save-auto-editor-steam?tab=readme-ov-file#4-obtain-a-steam-web-api-key')

def browse_file(var):
    file_path = filedialog.askopenfilename(filetypes=[("DAT Files", "*.dat"), ("All Files", "*.*")])
    if file_path:
        var.set(file_path)

def showCustomWindow(type_window, msg):
    if type_window == "error":
        if msg == "missing_fields":
            text = "Please fill all the fields."
        elif msg == "api_error":
            text = "An error occurred while fetching the achievements. Please make sure your Steam ID and API key are correct."
        elif msg == "private_profile":
            text = "Your profile or game details are private."
        elif msg == "id64_not_found":
            text = "Steam ID not found. Please verify your Steam ID."
        else:
            text = "No achievements found for this user."

        title = "Error"
        sound = "assets/sfx/error-sound.wav"
    else:
        text = "File saved successfully!"
        title = "Success"
        sound = "assets/sfx/success-sound.wav"

    winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    custom_window = tk.Toplevel(root)
    custom_window.title(title)
    custom_window.minsize(300, 100)
    custom_window.resizable(False, False)

    custom_window.iconbitmap(r"assets\rune_05_ansuz.ico")
    
    # message
    label = ttk.Label(custom_window, text=text, foreground="black", font=("Candara", 12, "bold"))
    label.pack(pady=20, padx=20)

    # OK button to close the dialog
    ok_button = ttk.Button(custom_window, text="OK", command=custom_window.destroy)
    ok_button.pack(pady=(0, 20))

    # center the error window on the main window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    custom_window.geometry(f"+{root_x + root_width//2 - 150}+{root_y + root_height//2 - 75}")

def runScript(steam_id, api_key, file_path):
    if steam_id == "" or api_key == "" or file_path == "":
        showCustomWindow("error", "missing_fields")
        return

    try:
        offset = 0x10
        with open(file_path, "rb") as file:
            data = file.read()
            length = len(data) - offset - 4
            checksum = model.calcAfterbirthChecksum(data, offset, length).to_bytes(5, 'little', signed=True)[:4]
            old_checksum = data[offset + length:]

        if not model.isSteamID64(steam_id):
            steam_id_64 = model.getSteamID64(steam_id, api_key)

            if steam_id_64:
                user_achievements = model.getAchievements(steam_id_64, api_key)
            else:
                showCustomWindow("error", "id64_not_found")
                return
        else:
            user_achievements = model.getAchievements(steam_id, api_key)

        if user_achievements == "api_error":
            showCustomWindow("error", "api_error")
            return
        elif user_achievements == "no_achievements":
            showCustomWindow("error", "no_achievements")
            return
        elif user_achievements == "private_profile":
            showCustomWindow("error", "private_profile")
            return
        elif isinstance(user_achievements, list):
            if len(user_achievements) != 0:
                # post-it
                data = model.updatePostIt(data, user_achievements)

                # challenges
                data = model.updateChallengesArray(data, user_achievements)

                with open(file_path, 'wb') as file:
                    file.write(model.updateChecksum(data))

                model.delUserPostIt()

                showCustomWindow("success", "")
    except Exception as e:
        showCustomWindow("error", "api_error")

if __name__ == "__main__":
    main()
