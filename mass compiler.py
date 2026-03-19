import json
from Item_overlay_maker import combine

with open("item_list.json") as f:
    item_list = json.load(f)

for item in item_list:
    combine(
        item["mode"],
        item["overlay"],
        item["output"],
        item.get("rarity")
    )