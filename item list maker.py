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
    print("Enter item details:\n")

    mode = input("Mode: ").strip().capitalize()
    overlay = input("Overlay: ").strip()
    output = input("Output name: ").strip()
    rarity = input("Rarity/Index: ").strip()

    item = {
        "mode": mode,
        "overlay": overlay,
        "output": output,
    }
    
    item["rarity"] = int(rarity)

    items = load_items()
    items.append(item)
    save_items(items)

    print("\nAdded item:")
    print(item)
    print(f"\nTotal items: {len(items)}")

if __name__ == "__main__":
    main()