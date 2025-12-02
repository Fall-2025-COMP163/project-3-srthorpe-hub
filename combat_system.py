"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Steven Thorpe Jr.]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }

    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")

    stats = enemy_stats[enemy_type]

    # Construct the enemy dictionary with max_health included
    return {
        "name": enemy_type.title(),
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"]
    }

    #pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    
     # Below: Using character level ranges to pick enemy types
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

    #pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
        # Below: Storing references and initializing battle state
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0

    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        
        # Below: Standard battle loop that continues until one side dies
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character cannot fight while dead.")

        while self.combat_active:
            self.turn_count += 1
            display_combat_stats(self.character, self.enemy)

            self.player_turn()
            result = self.check_battle_end()
            if result:
                break

            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

        # Determine winner + rewards
        if self.enemy["health"] <= 0:
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }

        return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}
       # pass
    
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
        # Below: Menu-based turn choices (basic attack, ability, run)
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run")

        choice = input("Select action: ")

        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You deal {dmg} damage!")
        elif choice == "2":
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(msg)
        elif choice == "3":
            if self.attempt_escape():
                display_battle_log("You escaped successfully!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")
        else:
            display_battle_log("Invalid choice (turn skipped).")
        #pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
        # Below: enemy always performs damage attack
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"The {self.enemy['name']} hits you for {dmg} damage!")
        #pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        
        # Below: strength minus 25% of defender strength, min damage 1
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(dmg, 1)

        #pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        
        # Below: Subtract health and prevent negative values
        target["health"] = max(0, target["health"] - damage)
        #pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        
        # Below: Returns winner string if someone dies
        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None
        #pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        
        # Below: Using 50% chance and disabling combat if successful
        if random.random() < 0.5:
            self.combat_active = False
            return True
        return False

        #pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)

    # Below: Routing abilities based on character class
    cls = character["class"]

    if cls == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "Mage":
        return mage_fireball(character, enemy)
    elif cls == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        return cleric_heal(character)
    else:
        raise InvalidTargetError("This character class has no special ability.")
    #pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage

  # Below: Deals double strength damage
    dmg = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Power Strike deals {dmg} damage!"  
   # pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage

   # Below: Deals double magic damage
    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Fireball burns the enemy for {dmg} damage!" 
    #pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage

   # Below: 50% chance for triple damage, otherwise basic strength
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        message = "Critical Hit!"
    else:
        dmg = character["strength"]
        message = "Normal hit."
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"{message} You dealt {dmg} damage!" 
    #pass

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)

    # Below: Heals 30 HP without exceeding max_health
    healed = min(30, character["max_health"] - character["health"])
    character["health"] += healed
    return f"You healed for {healed} HP!"
    #pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check

    return character["health"] > 0
    #pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation

    # Below: Returns enemy's xp and gold rewards
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}
    #pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    #pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    #pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")
