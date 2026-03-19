from PIL import Image
import json
import os

bg_folder = "backgrounds" # itemiconcompositedecobig for the background images
itemicon_folder = "itemiconbig" # the item you want to make
composite_folder = "composite" # itemiconcompositedecobig for the small addon added last
output_folder = "output" # output folder

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

# load config once
with open("rarity_preset.json") as f:
    CONFIG = json.load(f)

def combine(mode, overlay_name, output_name, rarity=None):

    mode = mode.capitalize()

    if mode not in ("Template", "Upgrade"):

        data = CONFIG[mode]

        base_name = data["rarities"][str(rarity)]
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

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, ensure_png(output_name))
    base.save(output_path)

if __name__ == "__main__":
    print("Available modes: Operator/Gear/Med/Food/Blueprint/Essence/Bottle")
    mode = input("Mode: ")
    overlay = input("Overlay: ")
    output = input("Output: ")

    rarity = None
    if mode not in ("Template", "Upgrade"):
        rarity = input("Rarity: ")

    combine(mode, overlay, output, rarity)