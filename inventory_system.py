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

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list

    # --- IMPLEMENTATION ADDED BELOW --- (NO CHANGE NEEDED)
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list

    # --- IMPLEMENTATION ADDED BELOW --- (NO CHANGE NEEDED)
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check

    return item_id in character["inventory"]

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method

    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation

    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list

    # --- IMPLEMENTATION ADDED BELOW --- (NO CHANGE NEEDED)
    removed_items = character["inventory"].copy()
    character["inventory"].clear()
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory

    # --- FIXED & ANNOTATED BELOW ---
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Only consumable items can be used.")

    # Parse effect (e.g., "health:20")
    stat, value = parse_item_effect(item_data["effect"])  # ADDED COMMENT: parse effect

    apply_stat_effect(character, stat, value)             # ADDED

    remove_item_from_inventory(character, item_id)        # ADDED

    return f"Used {item_data['name']} (+{value} {stat})."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    # TODO: Implement weapon equipping

    # --- FIXED & ANNOTATED BELOW ---

    # Ensure item_data dictionary exists on character
    if "item_data" not in character:        # ADDED
        character["item_data"] = {}         # ADDED
    character["item_data"][item_id] = item_data  # ADDED - store meta

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not in inventory.")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    stat, value = parse_item_effect(item_data["effect"])

    # Unequip old weapon
    if character.get("equipped_weapon"):
        old_weapon = character["equipped_weapon"]
        old_data = character["item_data"][old_weapon]
        old_stat, old_val = parse_item_effect(old_data["effect"])  # FIXED: replaced broken dict access

        character[old_stat] -= old_val
        character["inventory"].append(old_weapon)

    # Equip new weapon
    character[stat] += value
    character["equipped_weapon"] = item_id
    remove_item_from_inventory(character, item_id)

    return f"Equipped weapon: {item_data['name']}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    # TODO: Implement armor equipping

    # --- FIXED & ANNOTATED BELOW ---

    if "item_data" not in character:      # ADDED
        character["item_data"] = {}       # ADDED
    character["item_data"][item_id] = item_data  # ADDED

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor '{item_id}' not in inventory.")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    stat, value = parse_item_effect(item_data["effect"])

    # Unequip old armor
    if character.get("equipped_armor"):
        old_armor = character["equipped_armor"]
        old_data = character["item_data"][old_armor]
        old_stat, old_val = parse_item_effect(old_data["effect"])  # FIXED

        character[old_stat] -= old_val
        character["inventory"].append(old_armor)

    character[stat] += value
    character["equipped_armor"] = item_id
    remove_item_from_inventory(character, item_id)

    return f"Equipped armor: {item_data['name']}."

def unequip_weapon(character):
    """
    Remove equipped weapon
    """
    # TODO: Implement weapon unequipping

    # --- FIXED BELOW ---

    if not character.get("equipped_weapon"):
        return None

    weapon_id = character["equipped_weapon"]
    stat, value = parse_item_effect(character["item_data"][weapon_id]["effect"])  # FIXED

    character[stat] -= value

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip: inventory full.")

    character["inventory"].append(weapon_id)
    character["equipped_weapon"] = None

    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor
    """
    # TODO: Implement armor unequipping

    # --- FIXED BELOW ---

    if not character.get("equipped_armor"):
        return None

    armor_id = character["equipped_armor"]
    stat, value = parse_item_effect(character["item_data"][armor_id]["effect"])   # FIXED

    character[stat] -= value

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Cannot unequip: inventory full.")

    character["inventory"].append(armor_id)
    character["equipped_armor"] = None

    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item
    """
    # TODO: Implement purchasing

    # --- NO CHANGES NEEDED ---
    if character["gold"] < item_data["cost"]:
        raise InsufficientResourcesError("Not enough gold.")

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")

    character["gold"] -= item_data["cost"]
    character["inventory"].append(item_id)

    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item
    """
    # TODO: Implement selling

    # --- NO CHANGES NEEDED ---
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not found.")

    sell_price = item_data["cost"] // 2

    remove_item_from_inventory(character, item_id)
    character["gold"] += sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Convert "stat:value" to ("stat", value)
    """
    # TODO: Implement effect parsing

    stat, val = effect_string.split(":")
    return stat.strip(), int(val.strip())

def apply_stat_effect(character, stat_name, value):
    """
    Modify stat safely
    """
    # TODO: Implement stat application

    character[stat_name] += value

    if stat_name == "health":
        character["health"] = min(character["health"], character["max_health"])

def display_inventory(character, item_data_dict):
    """
    Print inventory
    """
    # TODO: Implement inventory display

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

