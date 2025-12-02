"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Steven Thorpe]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError

    # --- IMPLEMENTATION ADDED BELOW ---
    # Attempt to read quest file; raise custom exception if missing
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            block = []
            for line in file:
                line = line.strip()
                if line == "":
                    if block:
                        quest = parse_quest_block(block)  # parse block into dict
                        quests[quest["quest_id"]] = quest
                        block = []
                else:
                    block.append(line)

            # Handle final block if file does not end with newline
            if block:
                quest = parse_quest_block(block)
                quests[quest["quest_id"]] = quest

    except UnicodeDecodeError:
        # File unreadable or corrupted
        raise CorruptedDataError("Quest file contains unreadable characters.")

    except Exception as e:
        # Any parsing or formatting failure
        raise InvalidDataFormatError(f"Quest file format invalid: {e}")

    return quests
    #pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests

    # --- IMPLEMENTATION ADDED BELOW ---
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            block = []
            for line in file:
                line = line.strip()
                if line == "":
                    if block:
                        item = parse_item_block(block)
                        items[item["item_id"]] = item
                        block = []
                else:
                    block.append(line)

            if block:
                item = parse_item_block(block)
                items[item["item_id"]] = item

    except UnicodeDecodeError:
        raise CorruptedDataError("Item file contains unreadable characters.")

    except Exception as e:
        raise InvalidDataFormatError(f"Item file format invalid: {e}")

    return items
    #pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers

     # --- IMPLEMENTATION ADDED BELOW ---
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Validate numeric fields
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in numeric_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Quest field '{field}' must be an integer.")

    return True
   # pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    # --- IMPLEMENTATION ADDED BELOW ---
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    # Validate valid item type
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    # Validate numeric "cost"
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item 'cost' must be an integer.")

    return True
   # pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately

    # --- IMPLEMENTATION ADDED BELOW ---
    os.makedirs("data", exist_ok=True)

    # Create default quests
    if not os.path.exists("data/quests.txt"):
        try:
            with open("data/quests.txt", "w", encoding="utf-8") as f:
                f.write(
                    "QUEST_ID: quest_intro\n"
                    "TITLE: Welcome Adventurer\n"
                    "DESCRIPTION: Your first quest begins.\n"
                    "REWARD_XP: 50\n"
                    "REWARD_GOLD: 20\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n\n"
                )
        except PermissionError:
            raise CorruptedDataError("Cannot write to quests.txt due to permissions.")

    # Create default items
    if not os.path.exists("data/items.txt"):
        try:
            with open("data/items.txt", "w", encoding="utf-8") as f:
                f.write(
                    "ITEM_ID: sword_basic\n"
                    "NAME: Basic Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:5\n"
                    "COST: 100\n"
                    "DESCRIPTION: A simple blade.\n\n"
                )
        except PermissionError:
            raise CorruptedDataError("Cannot write to items.txt due to permissions.")
    #pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully

    # --- IMPLEMENTATION ADDED BELOW ---
    quest = {}
    try:
        for line in lines:
            key, value = line.split(": ", 1)

            # Normalize keys
            key = key.strip().lower().replace(":", "")

            # Convert numeric fields
            if key in ["reward_xp", "reward_gold", "required_level"]:
                value = int(value)
            else:
                value = value.strip()

            quest[key] = value

        validate_quest_data(quest)

        return quest

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")
    #pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    
# --- IMPLEMENTATION ADDED BELOW ---
    item = {}
    try:
        for line in lines:
            key, value = line.split(": ", 1)

            key = key.strip().lower()

            if key == "cost":
                value = int(value)

            elif key == "effect":
                # Format: stat:value
                stat, num = value.split(":")
                item["effect"] = {stat.strip(): int(num.strip())}
                continue

            else:
                value = value.strip()

            item[key] = value

        validate_item_data(item)

        return item

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")
    #pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")