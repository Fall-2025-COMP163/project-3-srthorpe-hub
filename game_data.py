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
    Load quest data from file.

    Reads quest entries separated by blank lines. Each block of text contains
    several key-value pairs that get parsed into a quest dictionary.

    Handles errors such as missing files, corrupted data, or invalid formatting.
    """

    # Check if the file exists; if not, raise custom missing file exception
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            block = []  # store lines for the current quest block

            for line in file:
                line = line.strip()

                # Blank line indicates end of a quest block
                if line == "":
                    if block:
                        quest = parse_quest_block(block)
                        quests[quest["quest_id"]] = quest
                        block = []
                else:
                    block.append(line)

            # Final block (in case file doesn't end with blank line)
            if block:
                quest = parse_quest_block(block)
                quests[quest["quest_id"]] = quest

    except UnicodeDecodeError:
        # File unreadable due to corrupted encoding
        raise CorruptedDataError("Quest file contains unreadable characters.")

    except Exception as e:
        # Any other parsing error
        raise InvalidDataFormatError(f"Quest file format invalid: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file.

    Works the same way as load_quests, reading entries separated by blank
    lines and parsing them into item dictionaries.
    """

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

            # Handle leftover block
            if block:
                item = parse_item_block(block)
                items[item["item_id"]] = item

    except UnicodeDecodeError:
        raise CorruptedDataError("Item file contains unreadable characters.")

    except Exception as e:
        raise InvalidDataFormatError(f"Item file format invalid: {e}")

    return items


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    """
    Ensures that all required fields exist and that numeric fields
    are correctly formatted as integers.
    """

    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]

    # Check that all required keys exist in the dictionary
    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Validate that the numeric fields are integers
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in numeric_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Quest field '{field}' must be an integer.")

    return True


def validate_item_data(item_dict):
    """
    Ensures items contain all required fields and have valid types.
    """

    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    # Ensure item type is one of the allowed types
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    # Cost must be an integer
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item 'cost' must be an integer.")

    return True


# ============================================================================
# DEFAULT FILE CREATION
# ============================================================================

def create_default_data_files():
    """
    Generates default quests and items files if they do not already exist.
    Useful during initial setup or testing.
    """

    os.makedirs("data", exist_ok=True)  # Ensure the data directory exists

    # Create default quests file
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

    # Create default items file
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


# ============================================================================
# HELPER PARSING FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Converts a block of quest lines into a dictionary.

    Splits lines on ': ' to extract key-value pairs, converts numeric
    values to integers, and validates the final dictionary.
    """

    quest = {}
    try:
        for line in lines:
            key, value = line.split(": ", 1)

            # Normalize key formatting
            key = key.strip().lower().replace(":", "")

            # Convert integer fields
            if key in ["reward_xp", "reward_gold", "required_level"]:
                value = int(value)
            else:
                value = value.strip()

            quest[key] = value

        # Validate the completed quest dictionary
        validate_quest_data(quest)

        return quest

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")


def parse_item_block(lines):
    """
    Converts a block of item lines into a dictionary.

    Handles parsing the effect field specially since it represents
    a dictionary containing stat modifications.
    """

    item = {}
    try:
        for line in lines:
            key, value = line.split(": ", 1)
            key = key.strip().lower()

            # Convert cost to integer
            if key == "cost":
                value = int(value)

            # Handle the effect field formatted as "stat:value"
            elif key == "effect":
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