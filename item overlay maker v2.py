from PIL import Image, ImageTk
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# folders
bg_folder = "backgrounds"
itemicon_folder = "itemiconbig"
composite_folder = "composite"
output_folder = "output"

def ensure_png(name):
    if os.path.splitext(name)[1]:
        return name
    return name + ".png"

def load_image(folder, name):
    path = os.path.join(folder, ensure_png(name))
    return Image.open(path).convert("RGBA")

def scale_image(img, scale):
    if scale == 1:
        return img
    return img.resize(
        (int(img.width * scale), int(img.height * scale)),
        Image.LANCZOS
    )

# load config
with open("rarity_preset_new.json") as f:
    CONFIG = json.load(f)

def combine(mode, overlay_name, output_name=None, rarity=None, preview=False):
    mode = mode.capitalize()

    if mode not in ("Template", "Upgrade"):
        data = CONFIG[mode]

        rarity_data = data["rarities"][rarity]
        base_name = rarity_data["file"]

        x, y = data["offset"]
        scale = data["scale"]

        base = load_image(bg_folder, base_name)
        overlay = load_image(itemicon_folder, overlay_name)

        overlay = scale_image(overlay, scale)
        base.paste(overlay, (x, y), overlay)

        if data["unlock_icon"]:
            unlock = load_image(composite_folder, "item_icon_mark_unlocked")
            base.paste(unlock, (0, 0), unlock)

    elif mode == "Template":
        base = load_image(bg_folder, "item_icon_bg_blueprint")
        overlay = load_image(itemicon_folder, overlay_name)

        overlay = scale_image(overlay, 0.7)
        base.paste(overlay, (75, 40), overlay)

    elif mode == "Upgrade":
        base = load_image(itemicon_folder, overlay_name)
        upgrade = load_image(composite_folder, "item_icon_mark_upgrade")
        base.paste(upgrade, (0, 0), upgrade)

    if preview:
        return base

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, ensure_png(output_name))
    base.save(output_path)
    return output_path

# -=[ GUI ]=-

current_rarity_map = []  # [(label, key)]

def get_rarity_key(selected_label):
    for label, key in current_rarity_map:
        if label == selected_label:
            return key
    return None


def combine():
    try:
        mode = mode_var.get().capitalize()
        overlay = overlay_entry.get()
        output = output_entry.get()
        rarity_label = rarity_var.get()

        if not overlay or not output:
            messagebox.showerror("Error", "Overlay and Output are required")
            return

        if mode not in ("Template", "Upgrade"):
            rarity_key = get_rarity_key(rarity_label)
            if not rarity_key:
                messagebox.showerror("Error", "Invalid type")
                return
        else:
            rarity_key = None

        path = combine(mode, overlay, output, rarity_key)

        messagebox.showinfo("Success", f"Saved to:\n{path}") # disable this to remove messagebox

        # clear inputs
        overlay_entry.delete(0, tk.END)
        output_entry.delete(0, tk.END)
        rarity_dropdown.set("")

        preview_label.config(image="")
        preview_label.image = None

    except Exception as e:
        messagebox.showerror("Error", str(e))


def preview_image(event=None):
    try:
        mode = mode_var.get().capitalize()
        overlay = overlay_entry.get()
        rarity_label = rarity_var.get()

        if not overlay:
            return

        if mode not in ("Template", "Upgrade"):
            rarity_key = get_rarity_key(rarity_label)

            # fallback to first rarity if none selected
            if not rarity_key and current_rarity_map:
                rarity_key = current_rarity_map[0][1]
        else:
            rarity_key = None

        img = combine(mode, overlay, None, rarity_key, preview=True)

        img_preview = img.copy()
        img_preview.thumbnail((200, 200))

        tk_img = ImageTk.PhotoImage(img_preview)

        preview_label.config(image=tk_img)
        preview_label.image = tk_img

    except Exception as e:
        pass


def on_mode_change(event=None):
    global current_rarity_map

    mode = mode_var.get()

    if mode in ("Template", "Upgrade"):
        rarity_dropdown.set("")
        rarity_dropdown.config(values=[], state="disabled")
        current_rarity_map = []
    else:
        rarity_data = CONFIG[mode]["rarities"]

        current_rarity_map = []
        display_values = []

        for k, v in rarity_data.items():
            label = f'{v["name"]}'
            display_values.append(label)
            current_rarity_map.append((label, k))

        rarity_dropdown.config(values=display_values, state="readonly")

        if display_values:
            rarity_dropdown.current(0)
            rarity_var.set(display_values[0])

    # delay preview slightly so UI updates first
    root.after(50, preview_image)


# -=[ Tkinter ]=-

root = tk.Tk()
root.title("Icon Compiler")
root.geometry("600x250")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# left side for preview
left_frame = tk.Frame(main_frame, width=250, height=250, bg="#555555")
left_frame.pack(side="left", fill="both")
left_frame.pack_propagate(False)

preview_label = tk.Label(left_frame, bg="#555555")
preview_label.pack(expand=True)

# right side for input
right_frame = tk.Frame(main_frame, padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True)

# mode
tk.Label(right_frame, text="Mode").pack(anchor="w")
mode_var = tk.StringVar()
mode_dropdown = ttk.Combobox(
    right_frame,
    textvariable=mode_var,
    values=list(CONFIG.keys()) + ["Template", "Upgrade"],
    state="readonly"
)
mode_dropdown.pack(fill="x")
mode_dropdown.bind("<<ComboboxSelected>>", on_mode_change)

# rarity
tk.Label(right_frame, text="Type").pack(anchor="w")
rarity_var = tk.StringVar()
rarity_dropdown = ttk.Combobox(right_frame, textvariable=rarity_var, state="readonly")
rarity_dropdown.pack(fill="x")
rarity_dropdown.bind("<<ComboboxSelected>>", preview_image)

# overlay
tk.Label(right_frame, text="Overlay").pack(anchor="w")
overlay_entry = tk.Entry(right_frame)
overlay_entry.pack(fill="x")
overlay_entry.bind("<KeyRelease>", preview_image)

# output
tk.Label(right_frame, text="Output Name").pack(anchor="w")
output_entry = tk.Entry(right_frame)
output_entry.pack(fill="x")

# button
tk.Button(right_frame, text="Combine", command=combine).pack(pady=10)

root.mainloop()