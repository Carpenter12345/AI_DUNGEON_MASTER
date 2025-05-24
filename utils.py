import time
import random
import sys

# ----------- Display Utilities -----------

def slow_print(text, delay=0.02):
    """slow_print text one character at a time for dramatic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_divider(char='-', length=50):
    """slow_prints a visual divider line."""
    print(char * length)

# ----------- Input Utilities -----------

def get_valid_input(prompt, options):
    """Prompt user until a valid option is chosen."""
    options = [opt.lower() for opt in options]
    while True:
        choice = input(f"{prompt} ").strip().lower()
        if choice in options:
            return choice
        else:
            print(f"Invalid choice. Options: {', '.join(options)}")

def yes_no_prompt(prompt):
    """Y/N confirmation."""
    return get_valid_input(prompt + " (y/n):", ['y', 'n']) == 'y'

# ----------- Randomization -----------

def get_random_event(events_pool):
    """Return a random event from the pool."""
    return random.choice(events_pool)

def weighted_random_choice(options):
    """
    Return an element from a list of tuples (item, weight).
    Example: [('Axe', 3), ('Sword', 1)] favors Axe.
    """
    total = sum(weight for item, weight in options)
    r = random.uniform(0, total)
    upto = 0
    for item, weight in options:
        if upto + weight >= r:
            return item
        upto += weight
    return options[-1][0]  # fallback

# ----------- XP & Level Helpers -----------

def calculate_xp_gain(difficulty_level=1, performance_multiplier=1):
    """XP gained based on difficulty and performance."""
    base_xp = 30 * difficulty_level
    return int(base_xp * performance_multiplier)

def check_level_up(character):
    """Check if character should level up based on XP."""
    required_xp = character.level * 100
    if character.xp >= required_xp:
        character.level_up()
        return True
    return False

# ----------- Inventory Management -----------

def add_to_inventory(inventory, item):
    """Adds item to inventory dictionary."""
    inventory[item] = inventory.get(item, 0) + 1

def remove_from_inventory(inventory, item):
    """Removes item from inventory if it exists."""
    if inventory.get(item, 0) > 0:
        inventory[item] -= 1
        if inventory[item] == 0:
            del inventory[item]
        return True
    return False

def has_required_items(inventory, required_items):
    """Checks if all required items exist in inventory."""
    return all(inventory.get(item, 0) >= qty for item, qty in required_items.items())

def display_inventory(inventory):
    """slow_prints out inventory contents neatly."""
    if not inventory:
        print("Inventory is empty.")
    else:
        slow_print("Inventory:")
        for item, count in inventory.items():
            slow_print(f" - {item} x{count}")

# ----------- Formatting -----------

def format_stats(character):
    """Returns a formatted string of the character's stats."""
    stats = character.stats
    return (
        f"Name: {character.name} | Class: {character.char_class}\n"
        f"Level: {character.level} | XP: {character.xp}\n"
        f"Health: {stats['health']} | Attack: {stats['attack']} | "
        f"Defense: {stats['defense']} | Intelligence: {stats['intelligence']}\n"
        f"Weapon: {character.weapon} | Abilities: {', '.join(character.abilities)}"
    )
