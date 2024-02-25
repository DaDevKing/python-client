import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyautogui
import time
import pytesseract
from pygetwindow import getWindowsWithTitle
 
# Configure pytesseract to use the appropriate path for Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract OCR path
 
def detect_baritone(mods_folder):
    baritone_identifier = None
    
    # Check if Baritone is installed by searching for its files in the mods folder
    for filename in os.listdir(mods_folder):
        if "Baritone" in filename:
            baritone_identifier = input("Enter the identifier for Baritone commands (e.g., '#'): ")
            break
    
    return baritone_identifier
 
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
        baritone_identifier = detect_baritone(mods_folder)
        if baritone_identifier:
            messagebox.showinfo("Baritone Detected", f"Baritone detected. Identifier for Baritone commands: {baritone_identifier}")
            save_config(mods_folder)
        else:
            messagebox.showinfo("Baritone Not Detected", "Baritone not detected in the selected mods folder.")
 
def send_command(command):
    if mods_folder:
        try:
            pyautogui.press('t')
            time.sleep(0.1)  # Wait for the chat window to open
            pyautogui.typewrite(command)
            pyautogui.press('enter')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send command: {e}")
    else:
        messagebox.showinfo("Mods Folder Not Selected", "Please select the mods folder first.")
 
def send_goto_command():
    if mods_folder:
        x = simpledialog.askfloat("Enter X Coordinate", "Please enter the X coordinate:")
        y = simpledialog.askfloat("Enter Y Coordinate", "Please enter the Y coordinate:")
        z = simpledialog.askfloat("Enter Z Coordinate", "Please enter the Z coordinate:")
        if x is not None and y is not None and z is not None:
            command = f"goto {x} {y} {z}"
            send_command(command)
 
def detect_task_completion():
    try:
        # Get Minecraft window
        mc_window = getWindowsWithTitle('Minecraft')[0]
 
        # Get coordinates of chat box region
        chat_box_x = mc_window.left + 8
        chat_box_y = mc_window.top + mc_window.height - 118
        chat_box_width = 830
        chat_box_height = 100
 
        # Take screenshot of chat box region
        screenshot = pyautogui.screenshot(region=(chat_box_x, chat_box_y, chat_box_width, chat_box_height))
 
        # Perform OCR on the screenshot to extract text
        chat_text = pytesseract.image_to_string(screenshot)
 
        # Check if "task complete" is found in the extracted text
        if "task complete" in chat_text.lower():
            messagebox.showinfo("Task Complete", "A task has been completed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to detect task completion: {e}")
 
def abort_action():
    if mods_folder:
        identifier = simpledialog.askstring("Enter Identifier", "Please enter the identifier for aborting the action:")
        if identifier:
            command = f"{identifier} cancel"
            send_command(command)
 
# Create the main application window
root = tk.Tk()
root.title("Baritone Control")
 
# Global variable to store the mods folder path
mods_folder = load_config()
 
# Browse Button
browse_button = tk.Button(root, text="Browse Mods Folder", command=browse_folder)
browse_button.pack(pady=10)
 
# Send Help Command Button
send_help_button = tk.Button(root, text="Send Baritone Help Command", command=lambda: send_command("#help"))
send_help_button.pack(pady=10)
 
# Baritone Command Buttons
goto_button = tk.Button(root, text="Goto", command=send_goto_command)
goto_button.pack()
 
mine_button = tk.Button(root, text="Mine", command=lambda: send_command("mine"))
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
 
# Abort Action Button
abort_button = tk.Button(root, text="Abort Action", command=abort_action)
abort_button.pack(pady=10)
 
# Detect Task Completion Button
detect_completion_button = tk.Button(root, text="Detect Task Completion", command=detect_task_completion)
detect_completion_button.pack(pady=10)
 
# Run the application
root.mainloop()