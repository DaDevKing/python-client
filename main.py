import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyautogui
import time
import pytesseract
from pygetwindow import getWindowsWithTitle
from PIL import ImageOps, Image
from tkinter import ttk
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

minecraft_blocks = {
    "Deepslate diamond ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_diamond_ore.png", "block_id": "minecraft:deepslate_diamond_ore"},
    "Deepslate emerald ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_emerald_ore.png", "block_id": "minecraft:deepslate_emerald_ore"},
    "Deepslate lapis ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_lapis_ore.png", "block_id": "minecraft:deepslate_lapis_ore"},
}

def detect_baritone(mods_folder):
    baritone_identifier = None
    
    for root, dirs, files in os.walk(mods_folder):
        for filename in files:
            if "Baritone" in filename:
                baritone_identifier = simpledialog.askstring("Baritone Detected", "Enter the identifier for Baritone commands (e.g., '#'): ")
                return baritone_identifier
    return None

def save_config(mods_folder):
    with open("config.txt", "w") as f:
        f.write(mods_folder)

def load_config():
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            return f.read().strip()
    else:
        return None

def browse_folder():
    global mods_folder
    mods_folder = filedialog.askdirectory(title="Select Minecraft Mods Folder")
    if mods_folder:
        if detect_baritone(mods_folder):
            messagebox.showinfo("Baritone Detected", "Baritone detected in the selected mods folder.")
            save_config(mods_folder)
        else:
            messagebox.showinfo("Baritone Not Detected", "Baritone not detected in the selected mods folder.")

def send_command(command):
    if mods_folder:
        try:
            pyautogui.press('t')
            time.sleep(0.1)
            pyautogui.typewrite("#" + command)
            pyautogui.press('enter')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send command: {e}")
    else:
        messagebox.showinfo("Mods Folder Not Selected", "Please select the mods folder first.")

def send_goto_command():
    if mods_folder:
        try:
            x = simpledialog.askfloat("Enter X Coordinate", "Please enter the X coordinate:")
            y = simpledialog.askfloat("Enter Y Coordinate", "Please enter the Y coordinate:")
            z = simpledialog.askfloat("Enter Z Coordinate", "Please enter the Z coordinate:")
            if x is not None and y is not None and z is not None:
                command = f"goto {x} {y} {z}"
                lock_and_execute(command)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send goto command: {e}")
    else:
        messagebox.showinfo("Mods Folder Not Selected", "Please select the mods folder first.")

def lock_and_execute(command):
    button_position = pyautogui.locateOnScreen('SRC/IMAGES/back_to_game.png')
    if button_position is not None:
        button_x, button_y = pyautogui.center(button_position)
        pyautogui.click(button_x, button_y)
        time.sleep(1)
        send_command(command)
    else:
        messagebox.showerror("Error", "Failed to find the 'Back to game' button on the screen.")

def create_scrollable_gui(root):
    root.title("Minecraft Blocks")

    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    create_block_widgets(frame)

def create_block_widgets(frame):
    photo_references = []

    for block_name, block_info in minecraft_blocks.items():
        image = Image.open(block_info["image_path"])
        image = image.resize((64, 64), Image.BILINEAR)
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(frame, image=photo, text=block_name, compound="top")
        label.image = photo
        photo_references.append(photo)

        label.bind("<Button-1>", lambda event, name=block_name: on_block_click(event, block_name))

        label.pack(padx=10, pady=10, side="top")

    return photo_references

def on_block_click(event, block_name):
    block_id = minecraft_blocks[block_name]["block_id"]
    return block_id

def start_block_wizard():
    root = tk.Toplevel()
    photo_references = create_scrollable_gui(root)
    print("Click on the ores now!")
    return photo_references

root = tk.Tk()
root.title("Baritone Control")

mods_folder = load_config()

browse_button = tk.Button(root, text="Browse Mods Folder", command=browse_folder)
browse_button.pack(pady=10)

send_help_button = tk.Button(root, text="Send Baritone Help Command", command=lambda: lock_and_execute("help"))
send_help_button.pack(pady=10)

goto_button = tk.Button(root, text="Goto", command=send_goto_command)
goto_button.pack()

def start_mine():
    selected_block_id = start_block_wizard()
    print(f"Selected block ID: {selected_block_id}")

mine_button = tk.Button(root, text="Mine", command=start_mine)
mine_button.pack()

build_button = tk.Button(root, text="Build", command=lambda: send_command("build"))
build_button.pack()

follow_button = tk.Button(root, text="Follow", command=lambda: send_command("follow"))
follow_button.pack()

goto_bed_button = tk.Button(root, text="Goto Bed", command=lambda: send_command("goto bed"))
goto_bed_button.pack()

explore_button = tk.Button(root, text="Explore", command=lambda: send_command("explore"))
explore_button.pack()

farm_button = tk.Button(root, text="Farm", command=lambda: send_command("farm"))
farm_button.pack()

deposit_button = tk.Button(root, text="Deposit", command=lambda: send_command("deposit"))
deposit_button.pack()

return_button = tk.Button(root, text="Return", command=lambda: send_command("return"))
return_button.pack()

cancel_button = tk.Button(root, text="Cancel", command=lambda: send_command("cancel"))
cancel_button.pack()

root.mainloop()
