"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Steven Thorpe]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice

    # --- IMPLEMENTATION ADDED BELOW ---
    while True:
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("Enter choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("Invalid input. Please enter 1, 2, or 3.")
    #pass

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop

    # --- IMPLEMENTATION ADDED BELOW ---
    print("\n=== NEW GAME ===")
    while True:
        name = input("Enter your character's name: ").strip()
        if name:
            break
        print("Name cannot be empty.")

    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    while True:
        print(f"Choose a class: {', '.join(valid_classes)}")
        char_class = input("Enter class: ").strip().title()
        if char_class in valid_classes:
            break
        print("Invalid class. Try again.")

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
        print(f"Character '{name}' the {char_class} created successfully!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")
    #pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop

    # --- IMPLEMENTATION ADDED BELOW ---
    saved = character_manager.list_saved_characters()
    if not saved:
        print("No saved characters found.")
        return

    print("\n=== LOAD GAME ===")
    for idx, char_name in enumerate(saved, start=1):
        print(f"{idx}. {char_name}")

    while True:
        choice = input(f"Enter number (1-{len(saved)}): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(saved):
                break
        print("Invalid choice. Try again.")

    selected_name = saved[choice - 1]

    try:
        current_character = character_manager.load_character(selected_name)
        print(f"Loaded character: {current_character['name']}")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading character: {e}")
    #pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action

    print(f"\nWelcome, {current_character['name']}!")
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting...")
            game_running = False
        else:
            print("Invalid choice.")

        # Auto-save after each action
        save_game()

    #pass

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    # --- IMPLEMENTATION ADDED BELOW ---
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in [str(i) for i in range(1, 7)]:
            return int(choice)
        print("Invalid choice. Try again.")
    #pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    # --- IMPLEMENTATION ADDED BELOW ---
    char = current_character
    print(f"\n=== {char['name']} the {char['class']} ===")
    print(f"Level: {char['level']}  HP: {char['health']}/{char['max_health']}")
    print(f"Strength: {char['strength']}  Magic: {char['magic']}")
    print(f"Experience: {char['experience']}  Gold: {char['gold']}")
    print(f"Inventory: {len(char['inventory'])} items")
    print("Active Quests:", ", ".join(char.get("active_quests", [])) or "None")
    print("Completed Quests:", ", ".join(char.get("completed_quests", [])) or "None")

   # pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system

    # --- IMPLEMENTATION ADDED BELOW ---
    inventory_system.display_inventory(current_character, all_items)

    # Simple usage menu
    while True:
        print("\nInventory Options: 1. Use 2. Equip Weapon 3. Equip Armor 4. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            item_id = input("Enter item ID to use: ").strip()
            try:
                result = inventory_system.use_item(current_character, item_id, all_items[item_id])
                print(result)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "2":
            item_id = input("Enter weapon ID to equip: ").strip()
            try:
                result = inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
                print(result)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "3":
            item_id = input("Enter armor ID to equip: ").strip()
            try:
                result = inventory_system.equip_armor(current_character, item_id, all_items[item_id])
                print(result)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

    #pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler

    # --- IMPLEMENTATION ADDED BELOW ---
    print("\nQuest Menu (simplified)")
    active = current_character.get("active_quests", [])
    completed = current_character.get("completed_quests", [])
    print("Active Quests:", active or "None")
    print("Completed Quests:", completed or "None")
    input("Press Enter to return.")
    #pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions

    # --- IMPLEMENTATION ADDED BELOW ---
    print("\nExploring...")
    try:
        enemy = combat_system.get_random_enemy_for_level(current_character["level"])
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()
        winner = result.get("winner")
        if winner == "player":
            current_character["experience"] += result.get("xp_gained", 0)
            current_character["gold"] += result.get("gold_gained", 0)
            print(f"Victory! XP +{result.get('xp_gained',0)}, Gold +{result.get('gold_gained',0)}")
        else:
            handle_character_death()
    except Exception as e:
        print(f"Combat error: {e}")
   # pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system

    # --- IMPLEMENTATION ADDED BELOW ---
    print("\nWelcome to the shop!")
    print(f"Your gold: {current_character['gold']}")
    print("Available items:")
    for item_id, data in all_items.items():
        print(f"{item_id}: {data['name']} ({data['type']}) - Cost: {data['cost']}")

    print("1. Buy  2. Sell  3. Back")
    choice = input("Choice: ").strip()
    if choice == "1":
        item_id = input("Enter item ID to buy: ").strip()
        try:
            inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            print(f"Purchased {all_items[item_id]['name']}")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "2":
        item_id = input("Enter item ID to sell: ").strip()
        try:
            gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
            print(f"Sold {all_items[item_id]['name']} for {gold} gold.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        return

    #pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions

    # --- IMPLEMENTATION ADDED BELOW ---
    try:
        character_manager.save_character(current_character)
    except Exception as e:
        print(f"Error saving game: {e}")
    #pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()

    # --- IMPLEMENTATION ADDED BELOW ---
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except (MissingDataFileError, InvalidDataFormatError):
        print("Data files missing or invalid. Creating default files.")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    #pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False

    # --- IMPLEMENTATION ADDED BELOW ---
    print("\n=== YOU HAVE DIED ===")
    choice = input("Revive for 50% health? (y/n): ").strip().lower()
    if choice == "y":
        character_manager.revive_character(current_character)
        print(f"{current_character['name']} has been revived with {current_character['health']} HP.")
    else:
        print("Game over.")
        game_running = False
    #pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
