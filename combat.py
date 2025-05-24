import random
from character import Character
from inventory import Inventory
from ascii_art import slow_print_art
from utils import *
class Enemy:
    def __init__(self, name, level, health, attack):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack

    def is_defeated(self):
        return self.health <= 0

class Combat:
    def __init__(self, player: Character, inventory: Inventory):
        self.player = player
        self.inventory = inventory

    def start_combat(self,enemy: Enemy):
        slow_print(f"\nCombat begins! {self.player.name} vs {enemy.name}\n")

        while self.player.health > 0 and enemy.health > 0:
            self.display_status(enemy)
            action = self.get_player_action()

            if action == '1':
                self.basic_attack(enemy)
            elif action == '2' and self.player.abilities:
                self.use_ability(enemy)
            elif action == '3':
                self.use_item()
            elif action == '4':
                slow_print("You defend and brace for impact.")
                self.player.health -= max(0, enemy.attack // 2 - self.player.defense)
            elif action == '5':
                if random.random() < 0.3:
                    slow_print("You escaped successfully!")
                    return False
                else:
                    print("Failed to flee!")

            if enemy.health > 0:
                self.enemy_turn(enemy)

        return self.evaluate_outcome(enemy)

    def display_status(self, enemy):
        slow_print(f"\n{self.player.name} - Health: {self.player.health}, Weapon: {self.player.weapon}")
        slow_print(f"{enemy.name} - Health: {enemy.health}")
        slow_print("Choose action: 1) Attack 2) Use Ability 3) Use Item 4) Defend 5) Flee")

    def get_player_action(self):
        while True:
            choice = input("> ")
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            slow_print("Invalid choice.")

    def basic_attack(self, enemy):
        damage = max(0, self.player.attack - random.randint(0, 5))
        slow_print(f"You hit {enemy.name} for {damage} damage!")
        enemy.health = max(0, enemy.health - damage)
    def take_damage(self, amount):
        self.health -= amount
        slow_print(f"{self.name} takes {amount} damage! Remaining HP: {self.health}")
        if self.health <= 0:
            slow_print(f"{self.name} has been defeated!")

    def use_ability(self, enemy):
        ability = self.player.abilities[0]  # First unlocked ability
        damage = self.player.attack + random.randint(5, 15)
        slow_print(f"You use {ability} and deal {damage} magic damage!")
        enemy.health = max(0, enemy.health - damage)

    def use_item(self):
        for category, item_list in self.inventory.items.items():
            if item_list:
                item = item_list[0]  # Use the first available item
                slow_print(f"You used {item}!")

                if "health" in item.lower():
                    self.player.health += 30
                    slow_print(f"{self.player.name} healed for 30 HP!")
                item_list.remove(item)
                return
        slow_print("No items to use!")


    def enemy_turn(self, enemy):
        damage = max(0, enemy.attack - self.player.defense)
        slow_print(f"{enemy.name} attacks and deals {damage} damage!")
        self.player.health -= damage

    def evaluate_outcome(self, enemy):
        if self.player.health <= 0:
            if self.player.char_class == "Ashborn" and self.player.level <= 5 and not self.player.has_awakening_triggered:
                slow_print("\nDarkness takes you. The cold whispers of death begin to coil around your soul...")
                slow_print("But the Ash clings to you. Refuses to let go.")
                slow_print('"Only through death shall the fire be reborn."')
                slow_print("\n🔥 Jin-woo awakens in the Silversong Tundra...\n")

                self.player.has_awakening_triggered = True
                self.player.health = 50
                self.player.level = 5.5
                self.player.xp = 0
                self.inventory.add_item("Ashen Ember", "quest_items")

                # Optionally trigger forced transport to new world
                slow_print("New objective: Survive the Trial of Frost in the Silversong Tundra.")
                return True # Prevent Game Over
            else:
                slow_print("You have been defeated. Game Over.")
                self.player.alive = False
                return False
        elif enemy.is_defeated():
            slow_print(f"You defeated {enemy.name}!")
            base_xp = 50
            if self.player.char_class == "Ashborn" and self.player.level >= 6:
                base_xp *= 2  # Double XP from level 7 onwards
            self.player.xp += base_xp
            self.player.check_level_up()
            if enemy.name != "The Echoed Self": self.inventory.add_item(f"Loot from {enemy.name}", "quest_items")
            if self.player.level % 2 == 0:
                self.trigger_random_event()
            return True
        else:   return False

    def trigger_random_event(self):
        events = [
            "A mysterious traveler grants you a bonus item!",
            "A storm breaks out, boosting your elemental powers!",
            "You step on an ancient rune and gain temporary defense!",
            "A shadow follows you... but disappears mysteriously."
        ]
        event = random.choice(events)
        slow_print(f"Random Event: {event}")
