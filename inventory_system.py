"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Steven Thorpe]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================

def add_item_to_inventory(character, item_id):
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character["inventory"]

def count_item(character, item_id):
    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    removed_items = character["inventory"].copy()
    character["inventory"].clear()
    return removed_items

# ============================================================================

def use_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")
    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Only consumable items can be used.")
    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)
    remove_item_from_inventory(character, item_id)
    return f"Used {item_data['name']} (+{value} {stat})."

def equip_weapon(character, item_id, item_data):
    if "item_data" not in character:
        character["item_data"] = {}
    character["item_data"][item_id] = item_data
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not in inventory.")
    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")
    stat, value = parse_item_effect(item_data["effect"])
    if character.get("equipped_weapon"):
        old_weapon = character["equipped_weapon"]
        old_data = character["item_data"].get(old_weapon, {"effect": "strength:0"})
        old_stat, old_val = parse_item_effect(old_data["effect"])
        character[old_stat] -= old_val
        character["inventory"].append(old_weapon)
    character[stat] += value
    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)
    return f"Equipped weapon: {item_data['name']}."

def equip_armor(character, item_id, item_data):
    if "item_data" not in character:
        character["item_data"] = {}
    character["item_data"][item_id] = item_data
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor '{item_id}' not in inventory.")
    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")
    stat, value = parse_item_effect(item_data["effect"])
    if character.get("equipped_armor"):
        old_armor = character["equipped_armor"]
        old_data = character["item_data"].get(old_armor, {"effect": "defense:0"})
        old_stat, old_val = parse_item_effect(old_data["effect"])
        character[old_stat] -= old_val
        character["inventory"].append(old_armor)
    character[stat] += value
    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)
    return f"Equipped armor: {item_data['name']}."

def unequip_weapon(character):
    if not character.get("equipped_weapon"):
        return None
    weapon_id = character["equipped_weapon"]
    effect = character["item_data"].get(weapon_id, {"effect": "strength:0"})["effect"]
    stat, value = parse_item_effect(effect)
    character[stat] -= value
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip: inventory full.")
    character["inventory"].append(weapon_id)
    character["equipped_weapon"] = None
    return weapon_id

def unequip_armor(character):
    if not character.get("equipped_armor"):
        return None
    armor_id = character["equipped_armor"]
    effect = character["item_data"].get(armor_id, {"effect": "defense:0"})["effect"]
    stat, value = parse_item_effect(effect)
    character[stat] -= value
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip: inventory full.")
    character["inventory"].append(armor_id)
    character["equipped_armor"] = None
    return armor_id

# ============================================================================

def purchase_item(character, item_id, item_data):
    if character["gold"] < item_data["cost"]:
        raise InsufficientResourcesError("Not enough gold.")
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")
    character["gold"] -= item_data["cost"]
    character["inventory"].append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not found.")
    sell_price = item_data["cost"] // 2
    remove_item_from_inventory(character, item_id)
    character["gold"] += sell_price
    return sell_price

# ============================================================================

def parse_item_effect(effect_string):
    stat, val = effect_string.split(":")
    return stat.strip(), int(val.strip())

def apply_stat_effect(character, stat_name, value):
    character[stat_name] += value
    if stat_name == "health":
        character["health"] = min(character["health"], character["max_health"])

def display_inventory(character, item_data_dict):
    inventory = character["inventory"]
    counts = {}
    for item_id in inventory:
        counts[item_id] = counts.get(item_id, 0) + 1
    print("=== INVENTORY ===")
    for item_id, qty in counts.items():
        item = item_data_dict[item_id]
        print(f"{item['name']} (x{qty})  — {item['type']}")
    print("=================")



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

