import json
import os

OUTPUT_FILE = "item_list.json"

def load_items():
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r") as f:
        return json.load(f)

def save_items(items):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(items, f, indent=2)

def main():
    items = load_items()

    while True:
        print("\nEnter item (or type 'q' to quit)\n")
        print("Available Modes: Operator/Gear/Med/Food/Blueprint/Essence/Bottle")
        mode = input("Mode: ").strip()
        if mode.lower() == "q":
            break

        overlay = input("Overlay: ").strip()
        rarity = input("Rarity: ").strip()
        output = input("Output name: ").strip()

        item = {
            "mode": mode.capitalize(),
            "overlay": overlay,
            "output": output
        }

        item["rarity"] = int(rarity)

        items.append(item)

    save_items(items)
    print(f"\nSaved {len(items)} items.")

if __name__ == "__main__":
    main()
