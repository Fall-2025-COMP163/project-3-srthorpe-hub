""" 
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Steven Thorpe]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class.
    Returns a dictionary containing all character attributes.
    """

    # Dictionary defining allowed classes and their base stats
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    # If class isn't valid, throw custom exception
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    # Retrieve base stats for the chosen class
    base = valid_classes[character_class]

    # Create the character dictionary with all required fields
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character


def save_character(character, save_directory="data/save_games"):
    """
    Saves a character dictionary to a text file.
    Creates the directory if it does not exist.
    """

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Construct full file path
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            # Write each character field to the save file
            for key, value in character.items():
                # Convert lists into comma-separated strings
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key.upper()}: {value}\n")
        return True

    except (PermissionError, IOError) as e:
        # Let file I/O errors propagate upward
        raise e


def load_character(character_name, save_directory="data/save_games"):
    """
    Loads a character from a save file and returns it as a dictionary.
    Also validates the data format.
    """

    # Build filename
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    # Save file must exist
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save found for: {character_name}")

    # Try reading the file
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Save file exists but could not be read")

    character = {}

    try:
        # Parse each line of the save file
        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError("Invalid line format in save file")

            key, value = line.strip().split(":", 1)
            key = key.lower()
            value = value.strip()

            # Convert list fields
            if key in ["inventory", "active_quests", "completed_quests"]:
                character[key] = value.split(",") if value else []

            # Convert numeric values
            elif key in ["level", "health", "max_health", "strength", "magic",
                         "experience", "gold"]:
                character[key] = int(value)

            # Everything else is a string
            else:
                character[key] = value

        # Validate data structure
        validate_character_data(character)
        return character

    except Exception:
        raise InvalidSaveDataError("Save data is corrupted or incomplete")


def list_saved_characters(save_directory="data/save_games"):
    """
    Returns a list of saved character names (without file extensions).
    """

    # If directory does not exist, return empty list
    if not os.path.exists(save_directory):
        return []

    characters = []

    # Look through save files and extract character names
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            characters.append(filename.replace("_save.txt", ""))

    return characters


def delete_character(character_name, save_directory="data/save_games"):
    """
    Deletes a saved character file.
    Throws an error if the file does not exist.
    """

    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    # Must exist before deletion
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save exists for: {character_name}")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add XP and handle leveling up.
    Characters cannot gain XP if dead.
    """

    # Dead characters cannot receive XP
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead and cannot gain XP")

    # Add XP
    character["experience"] += xp_amount
    leveled_up = False

    # Level up repeatedly if enough XP accumulates
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1

        # Stat increases
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

        leveled_up = True

    return leveled_up


def add_gold(character, amount):
    """
    Modify gold total. Cannot go below zero.
    """

    new_total = character["gold"] + amount

    # Prevent negative gold
    if new_total < 0:
        raise ValueError("Gold cannot go below zero")

    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    """
    Heal character without exceeding max health.
    Returns how much was actually healed.
    """

    old_health = character["health"]

    # Increase health but cap at max_health
    character["health"] = min(character["max_health"], character["health"] + amount)

    return character["health"] - old_health


def is_character_dead(character):
    """
    Returns True if character is dead (health <= 0).
    """

    return character["health"] <= 0


def revive_character(character):
    """
    Revive a dead character with 50% of max health.
    Returns True if revived.
    """

    # If not dead, can't revive
    if character["health"] > 0:
        return False

    # Revive with half max health
    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Ensures a loaded character contains all required fields
    and that values are correct types.
    """

    # List of required keys for a valid character
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    # Check every required field is present
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    # Check numeric fields are integers
    numeric_fields = ["level", "health", "max_health", "strength",
                      "magic", "experience", "gold"]

    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"{field} must be an integer")

    # Check list fields are lists
    list_fields = ["inventory", "active_quests", "completed_quests"]

    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"{field} must be a list")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")


