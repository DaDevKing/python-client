import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Sample list of Minecraft blocks with their corresponding image paths
minecraft_blocks = {
    "Deepslate diamond ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_diamond_ore.png", "block_id": "minecraft:deepslate_diamond_ore"},
    "Deepslate emerald ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_emerald_ore.png", "block_id": "minecraft:deepslate_emerald_ore"},
    "Deepslate lapis ore": {"image_path": "SRC/IMAGES/BLOCKS/deepslate_lapis_ore.png", "block_id": "minecraft:deepslate_lapis_ore"},
    # Add more blocks as needed
}

def create_block_widgets(frame):
    # Create widgets for each Minecraft block
    for block_name, block_info in minecraft_blocks.items():
        # Load image
        image = Image.open(block_info["image_path"])
        image = image.resize((64, 64), Image.ANTIALIAS)  # Resize image to fit widget
        photo = ImageTk.PhotoImage(image)

        # Create label with image
        label = ttk.Label(frame, image=photo, text=block_name, compound="top")
        label.image = photo  # Keep reference to image to prevent garbage collection

        # Bind click event to label
        label.bind("<Button-1>", lambda event, name=block_name: on_block_click(event, name))

        # Add label to frame
        label.pack(padx=10, pady=10, side="top")


def create_scrollable_gui(root):
    root.title("Minecraft Blocks")

    # Create a scrollable frame
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    create_block_widgets(frame)

def on_block_click(event, block_name):
    # Get the block ID
    block_id = minecraft_blocks[block_name]["block_id"]
    return block_id

def start_block_wizard():
    root = tk.Tk()  # Create the root window
    create_scrollable_gui(root)  # Pass the root window to create_scrollable_gui
    root.mainloop()  # Start the main event loop

