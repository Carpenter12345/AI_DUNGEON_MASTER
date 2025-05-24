import random
from worlds import World,WorldManager
from combat import Combat, Enemy
from character import Character
from inventory import Inventory
from ascii_art import slow_print_art
from utils import *

class Story:
    def __init__(self, character: Character, inventory: Inventory, world_manager: WorldManager):
        self.character = character
        self.inventory = inventory
        self.world_manager = world_manager
        self.active_quests = {}
        self.completed_quests = set()
        self.bosses_defeated = set()
        self.story_flags = {}  # Track various story progress flags
        boss_data = {
            "Emberfall Caverns": {
                "boss_key": "emberfall_boss",
                "boss_info": {"name": "Flame Warden", "hp": 50, "attack": 12},
                "required_item": None,
                "reward_item": "Ash Pendant",
                "xp_reward": 100,
                "ascii_art":"flame_warden.txt"
            },
            "Glimmerfen Hollow": {
                "boss_key": "glimmerfen_boss",
                "boss_info": {"name": "Swamp Wraith", "hp": 45, "attack": 10},
                "required_item": "Ash Pendant",
                "reward_item": "Wind Fragment",
                "xp_reward": 120,
                "ascii_art":"swamp_wraith.txt"
            },
            "Obsidian Wastes": {
                "boss_key": "obsidian_boss",
                "boss_info": {"name": "Cursed Nomad", "hp": 55, "attack": 14},
                "required_item": "Wind Fragment",
                "reward_item": "Void Map",
                "xp_reward": 140,
                "ascii_art":"cursed_nomad.txt"
            },
            "Aetherreach Peaks": {
                "boss_key": "aetherreach_boss",
                "boss_info": {"name": "Sky Watcher", "hp": 60, "attack": 15},
                "required_item": "Void Map",
                "reward_item": "Feather Talisman",
                "xp_reward": 160,
                "ascii_art":"sky_watcher.txt"
            },
            "Silversong Tundra": {
                "boss_key": "silversong_boss",
                "boss_info": {"name": "Frost Revenant", "hp": 70, "attack": 18},
                "required_item": "Feather Talisman",
                "reward_item": "Mirror Shard",
                "xp_reward": 180,
                "ascii_art":"frost_revenant.txt"
            },
            "Sunken Archives": {
                "boss_key": "sunken_boss",
                "boss_info": {"name": "Tide Warden", "hp": 80, "attack": 20},
                "required_item": "Mirror Shard",
                "reward_item": "Nexus Key",
                "xp_reward": 200,
                "ascii_art":"tide_warden.txt"
            }
        }   

    def start(self):
        slow_print("\nWelcome to the adventure!\n")
        slow_print("You begin your journey in The Void, a mysterious realm of nothingness.")
        self.story_flags["in_void"] = True
        self.inventory.add_item("Starter Token", "misc")
        self.character.gain_xp(10)
        self.story_loop()
        
    def story_loop(self):
        while True:
            print("\nCurrent Level:", self.character.level)
            print("Current XP:", self.character.xp)

            accessible_worlds = [
                w for w in self.world_manager.available_worlds(self.inventory, self.character)
                if w.name not in self.completed_quests
            ]   

            if not accessible_worlds:
                slow_print("\nThere are no accessible worlds available to explore right now.")
                slow_print("Explore the Void further or come back later.")
                # Optionally: Add Void-specific actions here
                break
            
            slow_print("\nAvailable Worlds to explore:")
            for i, world in enumerate(accessible_worlds, start=1):
                slow_print(f"{world.name} - {world.description}")

            choice = input("\nChoose a world to enter (number) or 'q' to quit: ").strip()


            if choice.lower() == 'q':
                slow_print("\nThanks for playing! Goodbye.")
                break

            if not choice.isdigit():
                slow_print("Invalid input. Please enter a number corresponding to a world or 'q' to quit.")
                continue

            index = int(choice) - 1

            if index < 0 or index >= len(accessible_worlds):
                slow_print("Invalid choice, please select a valid world number.")
                continue

            selected_world = accessible_worlds[index]

            # Check if player can enter before proceeding
            if not selected_world.can_enter(self.inventory,self.character):
                slow_print(f"You do not have the required items to enter {selected_world.name}.")
                continue
            #self.enter_world(selected_world)
            self.world_manager.enter_world(selected_world.name, self.character, self.inventory)
            if self.world_manager.all_completed():
                slow_print("\nYou have explored all available worlds! Prepare for the final challenge soon.")
                break

    def enter_world(self, world):
        slow_print(f"\n--- Entering {world.name} ---")
        world.enter(self.character, self.inventory)

        # Trigger quests, bosses, and story events for the world
        self.trigger_world_story(world)
        self.completed_quests.add(world.name)


    def handle_boss_fight(self, boss_key, boss_info, required_item, reward_item, xp_reward):
    # Check if boss already defeated
        if boss_key in self.bosses_defeated:
            return False
    
    # Check if prerequisite item is needed and if player has it
        if required_item is not None and not self.inventory.has_item(required_item):
            slow_print(f"You lack the item '{required_item}' needed to confront the boss.")
            return False

        enemy = Enemy(
        name=boss_info["name"],
        level=boss_info.get("level", 1),
        health=boss_info["hp"],
        attack=boss_info["attack"]
    )
        
        slow_print(f"\nCombat begins! {self.character.name} vs {enemy.name}\n")
        #slow_print(f"\nYou encounter {boss_info['name']}!")
        combat = Combat(self.character, self.inventory)  # This sets self.player and self.inventory properly
        result = combat.start_combat(enemy)  # You must pass in an Enemy object here
        #result = Combat.start_combat(self.character, self.inventory)
        if result:
            slow_print(f"You defeated {boss_info['name']} and gained the {reward_item}!")
            self.inventory.add_item(reward_item, "quest_items")
            self.bosses_defeated.add(boss_key)
            self.character.gain_xp(xp_reward)
        else:
            slow_print(f"You were defeated by {boss_info['name']}. Game Over.")
            exit()
    def trigger_world_story(self, world):
        boss = self.boss_data.get(world.name)
        if world.name in boss:
        # slow_print the ASCII art for the boss before the fight
            slow_print("\n" + boss.get("boss_intro", f"A powerful foe blocks your path in {world.name}!"))
            '''ascii_file = boss.get("ascii_art")
            if ascii_file:
                slow_print(f"[DEBUG] Attempting to slow_print ASCII art from file: {ascii_file}")
                slow_print_art(ascii_file)
            else:
                slow_print(f"No ASCII art available for the boss in {world.name}.")'''
            self.handle_boss_fight(
                boss_key=boss["boss_key"],
                boss_info=boss["boss_info"],
                required_item=boss["required_item"],
                reward_item=boss["reward_item"],
                xp_reward=boss["xp_reward"]
            )
            return  # Boss fight occurred, skip exploration XP

        slow_print("You explore the world thoroughly, learning more and gaining experience.")
        self.character.gain_xp(50)
