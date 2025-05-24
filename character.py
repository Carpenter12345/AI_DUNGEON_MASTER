import random
from utils import *

class Character:
    CHARACTER_CLASSES = [
        "Knight",
        "Mage",
        "Rogue",
        "Alchemist",
        "Necromancer",
        "Ashborn"
    ]

    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.xp = 0
        self.inventory = []
        self.weapon = self.get_starting_weapon()
        self.abilities = []
        self.evolved = False
        self.evolve_class = False
        self.xp_multiplier = 1
        self.assign_base_stats()
        self.has_awakening_triggered = False
        self.status_effects = []
        self.quest_log = []
        self.location = 'Starting Area'
        self.visited_worlds = []
        self.unchosen_skills = []


    def assign_base_stats(self):
    # Combined dictionary of stats per class
        stats = {
        'Knight':      {'melee': 8, 'combat': 7, 'intelligence': 4, 'health': 70, 'attack': 15, 'defense': 10, 'speed': 5},
        'Mage':        {'melee': 3, 'combat': 5, 'intelligence': 10, 'health': 60,  'attack': 20, 'defense': 5,  'speed': 7},
        'Rogue':       {'melee': 6, 'combat': 8, 'intelligence': 5, 'health': 75,  'attack': 12, 'defense': 7,  'speed': 12},
        'Alchemist':   {'melee': 4, 'combat': 5, 'intelligence': 9, 'health': 71,  'attack': 10, 'defense': 8,  'speed': 10},
        'Necromancer': {'melee': 3, 'combat': 6, 'intelligence': 9, 'health': 65,  'attack': 18, 'defense': 6,  'speed': 6},
        'Ashborn':     {'melee': 2, 'combat': 3, 'intelligence': 5, 'health': 40,  'attack': 8,  'defense': 5,  'speed': 8},
        }

    # Get stats for this character's class, default to Knight if not found
        class_stats = stats.get(self.char_class, stats['Knight'])

    # Assign all stats to self
        self.melee = class_stats['melee']
        self.combat = class_stats['combat']
        self.intelligence = class_stats['intelligence']
        self.health = class_stats['health']
        self.attack = class_stats['attack']
        self.defense = class_stats['defense']
        self.speed = class_stats['speed']


    def get_starting_weapon(self):
        weapons = {
            'Knight': 'Steel Sword',
            'Mage': 'Arcane Staff',
            'Rogue': 'Dual Daggers',
            'Alchemist': 'Elixir Gun',
            'Necromancer': 'Bone Wand',
            'Ashborn': 'Cracked Blade',
        }
        return weapons.get(self.char_class, 'Wooden Stick')

    def gain_xp(self, amount, world_manager=None):
        self.xp += amount * self.xp_multiplier
        while self.xp >= self.level * 100:
            self.level_up()
            if world_manager:   world_manager.unlock_worlds(self.level)

    def level_up(self):
        self.level += 1
        self.health += 10
        self.melee += 1
        self.combat += 1
        self.intelligence += 1

        if self.level == 2:
            self.unlock_unique_ability()

        if self.char_class == 'Ashborn' and self.has_awakening_triggered and not self.evolved and self.level >= 5:
            self.evolve_to_strongest()

        if self.level % 2 == 0:
            self.trigger_random_event()

        self.upgrade()

    def unlock_unique_ability(self):
        abilities = {
            'Knight': ('Shield Bash', 'Holy Blade'),
            'Mage': ('Mana Surge', 'Flame Orb'),
            'Rogue': ('Shadow Step', 'Venomfang'),
            'Alchemist': ('Chemical Burst', 'Phantom Vial'),
            'Necromancer': ('Soul Drain', 'Deathgrip Wand'),
            'Ashborn': ('Ember Awakening', 'Burnt Fang'),
        }
        ability, upgraded_weapon = abilities.get(self.char_class, (None, None))
        if ability and upgraded_weapon:
            self.abilities.append(ability)
            self.weapon = upgraded_weapon

    def evolve_to_strongest(self):
        self.weapon = 'Flamebrand (Evolved Weapon)'
        self.abilities.append('Inferno Fury')
        self.evolve_class = True
        self.evolved = True
        self.xp_multiplier = 2

    def upgrade(self):
        if self.level == 10:
            if self.char_class == "Knight":
                self.weapon = "Valiant Edge"
                self.abilities.append("Unbreakable Guard")
            elif self.char_class == "Mage":
                self.weapon = "Staff of Eternity"
                self.abilities.append("Reality Rift")
            elif self.char_class == "Rogue":
                self.weapon = "Phantom Dagger"
                self.abilities.append("Shadow Step")
            elif self.char_class == "Alchemist":
                self.weapon = "Philosopher's Flask"
                self.abilities.append("Elemental Transmute")
            elif self.char_class == "Necromancer":
                self.weapon = "Soulbinder"
                self.abilities.append("Army of the Lost")
            elif self.char_class == "Ashborn":
                self.weapon = "Flamebrand (Evolved Weapon)"
                self.abilities.append("Inferno Fury")
                self.evolve_class = True

    def learn_skill(self, skill_name):
        if skill_name not in self.abilities:
            self.abilities.append(skill_name)
            slow_print(f"{self.name} has learned a new skill: {skill_name}!")
        else:
            slow_print(f"{self.name} already knows the skill: {skill_name}.")

    def trigger_random_event(self):
        events = [
            "You stumble upon a hidden merchant.",
            "A trap is triggered! You lose some health.",
            "A wandering sage offers mysterious wisdom.",
            "You find a cursed relic... will you keep it?",
        ]
        event = random.choice(events)
        slow_print(f"Random Event: {event}")

    def check_level_up(self):
        xp_threshold = 100 * self.level
        while self.xp >= xp_threshold:
            self.xp -= xp_threshold
            self.level += 1
            self.health += 10  # optional: reward player
            slow_print(f"\n🎉 {self.name} has leveled up to Level {self.level}!")
            slow_print(f"{self.name}'s max HP increased to {self.health}.")
            xp_threshold = 100 * self.level

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            slow_print(f"{self.name} takes {amount} damage! Current health: {self.health}")

            if self.char_class == 'Ashborn' and self.level < 6 and not self.has_awakening_triggered:
                slow_print("\nDarkness takes you. The cold whispers of death begin to coil around your soul...")
                slow_print("But the Ash clings to you. Refuses to let go.")
                slow_print("\"Only through death shall the fire be reborn.\"")
                
                self.health = int(0.3 * self.health)  # Revive with 30% HP
                self.level = 5.5  # Transitional level
                self.status_effects.append('Glowing Ash Mark')
                self.has_awakening_triggered = True
                self.quest_log.append("Ashborn Awakening: Complete the Trial of Ember in the Silversong Tundra")
                self.location = 'Silversong Tundra'

                slow_print(f"\n🔥 {self.name} awakens in the Silversong Tundra. The embers on your skin pulse with hidden power...")
                slow_print("A new quest has begun: The Trial of Ember.")
            else:
                slow_print(f"{self.name} has fallen in battle...")
        else:
            slow_print(f"{self.name} takes {amount} damage! Current health: {self.health}")


    def collect_item(self, item):
        self.inventory.append(item)

    def fail_gameplay_check(self, condition):
        """
        Triggers game failure if a critical condition is met such as bad choice or combat loss.
        """
        if condition:
            slow_print(f"{self.name} has failed their quest due to a crucial mistake!")
            return True
        return False

    def __str__(self):
        return (f"{self.name} the {self.char_class} | Level {self.level} | XP: {self.xp} | HP: {self.health}\n"
                f"Weapon: {self.weapon} | Abilities: {self.abilities} | Inventory: {self.inventory}")

    @classmethod
    def get_available_classes(cls):
        return cls.CHARACTER_CLASSES

    @classmethod
    def create_character(cls):
        slow_print("Fate of the world lies in the hands of these, blessed by the almighty:")
        for cclass in cls.CHARACTER_CLASSES:
            slow_print(f"- {cclass}")
        while True:
            choice = input("Choose your warrior: ").strip().lower()
            matched_classes = [c for c in cls.CHARACTER_CLASSES if c.lower() == choice]
            if matched_classes:
                chosen_class = matched_classes[0]
                break
            else:
                print("Invalid choice, try again.")
        name = input("By the Sovereign Sigil, I summon thee! ")
        return cls(name, chosen_class)
    

    @property
    def stats(self):
        return {
            'health': self.health,
            'attack': self.attack,
            'defense': self.defense,
            'intelligence': self.intelligence,
            'melee': self.melee,
            'combat': self.combat,
            'speed': self.speed
        }


'''
    def create_character(cls):
        slow_print("Choose your warrior kind:")
        for idx, cclass in enumerate(cls.CHARACTER_CLASSES, 1):
            slow_print(f"{idx}. {cclass}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(cls.CHARACTER_CLASSES):
                    break
                else:
                    slow_print("Invalid choice, try again.")
            except ValueError:
                slow_print("Please enter a valid number.")
        chosen_class = cls.CHARACTER_CLASSES[choice - 1]
        name = input("By the Sovereign Sigil, I summon thee! ")
        return cls(name, chosen_class)'''