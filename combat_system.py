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
    Create an enemy based on type.

    This function selects preset stats for a given enemy type.
    If the type is valid, it constructs and returns an enemy dictionary.
    If invalid, it raises InvalidTargetError.
    """

    # Dictionary storing stats for each enemy type
    enemy_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }

    # Check if the enemy type exists
    if enemy_type not in enemy_stats:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")

    stats = enemy_stats[enemy_type]

    # Build and return a complete enemy dictionary
    return {
        "name": enemy_type.title(),
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"]
    }


def get_random_enemy_for_level(character_level):
    """
    Returns an enemy appropriate for the player's level.
    Level ranges determine which enemy is chosen.
    """

    # Choose enemy based on level brackets
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Handles turn-based combat between the player and an enemy.
    Tracks turns, actions, damage, and battle completion.
    """

    def __init__(self, character, enemy):
        """
        Store references to the character and enemy.
        Initialize combat state and turn counter.
        """
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0

    def start_battle(self):
        """
        Main combat loop.
        Turns alternate between player and enemy until one dies.
        Raises CharacterDeadError if starting at 0 HP.
        """

        # Ensure player is alive before starting
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character cannot fight while dead.")

        # Combat loop continues until combat_active becomes False
        while self.combat_active:
            self.turn_count += 1
            display_combat_stats(self.character, self.enemy)

            # Player takes their turn
            self.player_turn()
            result = self.check_battle_end()
            if result:
                break

            # Enemy takes their turn
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                break

        # When loop ends, determine winner and grant rewards if needed
        if self.enemy["health"] <= 0:
            rewards = get_victory_rewards(self.enemy)
            return {
                "winner": "player",
                "xp_gained": rewards["xp"],
                "gold_gained": rewards["gold"]
            }

        return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        """
        Allows player to choose an action.
        Options: basic attack, special ability, or attempt to escape.
        """

        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # Display choices
        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run")

        choice = input("Select action: ")

        # Handle player input
        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You deal {dmg} damage!")

        elif choice == "2":
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(msg)

        elif choice == "3":
            # Escape attempt has 50% success chance
            if self.attempt_escape():
                display_battle_log("You escaped successfully!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")

        else:
            display_battle_log("Invalid choice (turn skipped).")

    def enemy_turn(self):
        """
        Enemy takes its action.
        For simplicity, enemies always perform a basic attack.
        """

        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # Enemy damage calculation
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"The {self.enemy['name']} hits you for {dmg} damage!")

    def calculate_damage(self, attacker, defender):
        """
        Damage formula:
        attacker_strength - (defender_strength // 4)
        Always deals at least 1 damage.
        """

        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(dmg, 1)

    def apply_damage(self, target, damage):
        """
        Subtracts HP but prevents health from dropping below zero.
        """
        target["health"] = max(0, target["health"] - damage)

    def check_battle_end(self):
        """
        Checks if either the player or enemy has reached 0 HP.
        Returns the winner string or None if combat continues.
        """

        if self.enemy["health"] <= 0:
            return "player"
        if self.character["health"] <= 0:
            return "enemy"
        return None

    def attempt_escape(self):
        """
        50% chance to escape.
        If successful, combat ends.
        """

        if random.random() < 0.5:
            self.combat_active = False
            return True
        return False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================


def use_special_ability(character, enemy):
    """
    Selects and activates the special ability for the character's class.
    """

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


def warrior_power_strike(character, enemy):
    """
    Warrior ability: deals double strength damage.
    """

    dmg = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Power Strike deals {dmg} damage!"


def mage_fireball(character, enemy):
    """
    Mage ability: deals double magic damage.
    """

    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Fireball burns the enemy for {dmg} damage!"


def rogue_critical_strike(character, enemy):
    """
    Rogue ability: 50% chance of triple strength damage,
    otherwise performs a normal hit.
    """

    if random.random() < 0.5:
        dmg = character["strength"] * 3
        message = "Critical Hit!"
    else:
        dmg = character["strength"]
        message = "Normal hit."

    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"{message} You dealt {dmg} damage!"


def cleric_heal(character):
    """
    Cleric ability: restores up to 30 HP
    without exceeding max health.
    """

    healed = min(30, character["max_health"] - character["health"])
    character["health"] += healed
    return f"You healed for {healed} HP!"


# ============================================================================
# COMBAT UTILITIES
# ============================================================================


def can_character_fight(character):
    """
    Returns True if the character is alive and able to battle.
    """
    return character["health"] > 0


def get_victory_rewards(enemy):
    """
    Returns XP and gold gained after defeating an enemy.
    """
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}


def display_combat_stats(character, enemy):
    """
    Prints the current health of both the player and the enemy.
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    """
    Prints a formatted battle message.
    """
    print(f">>> {message}")


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
