import random
from character import Character
from inventory import Inventory
from combat import Combat, Enemy
from ascii_art import slow_print_art
#from story import Story
from final_realm import FracturedNexus
from utils import *

class World:
    def __init__(self, name, description, entry_item=None, enemies=None, items=None, xp_reward=100,required_level=1,ascii_art=None):
        self.name = name
        self.description = description
        self.entry_item = entry_item  # Item required to access the world
        self.enemies = enemies or []
        self.items = items or []
        self.required_level = required_level
        self.xp_reward = xp_reward
        self.completed = False
        self.ascii_art = ascii_art


    def can_enter(self, inventory,character):
        has_item = self.entry_item is None or inventory.has_item(self.entry_item)
        meets_level = character.level >= self.required_level
        return has_item and meets_level

    def enter(self, character, inventory):
        slow_print(f"\nEntering {self.name}: {self.description}")
        if self not in character.visited_worlds:    character.visited_worlds.append(self)
        if self.ascii_art:
            slow_print_art(self.ascii_art)
        else:
            slow_print(f"No ASCII art available for {self.name}.")

        # Random event chance
        if random.randint(1, 100) <= 40:
            self.trigger_random_event(character)

        # Combat
        if self.enemies:
            enemy_data = random.choice(self.enemies)
            enemy = Enemy(
                name=enemy_data["name"], 
                level=enemy_data.get("level",1),  # You can adjust enemy level if needed
                health=enemy_data["hp"], 
                attack=enemy_data["attack"]
            )
            slow_print(f"A {enemy.name} blocks your path!")
            combat = Combat(character, inventory)
            combat.start_combat(enemy)
           
            if character.health <= 0:
                slow_print("You failed the combat. Game over.")
                exit()
        # Collect items
        for item in self.items:
            slow_print(f"You found {item}!")
            inventory.add_item(item,'quest_items')

        # XP and level up
        character.gain_xp(self.xp_reward)
        self.completed = True
        slow_print(f"World '{self.name}' completed.\n")
        return True

    def trigger_random_event(self, character):
        events = [
            ("A mysterious traveler offers guidance.", lambda c: c.gain_xp(25)),
            ("You fall into a trap and take damage.", lambda c: c.take_damage(10)),
            ("You discover a hidden shrine and gain insight.", lambda c: c.learn_skill("Ancient Insight")),
        ]
        desc, effect = random.choice(events)
        slow_print(f"Random Event: {desc}")
        effect(character)


class WorldManager:
    def __init__(self):
        self.all_worlds = []
        self.unlocked_worlds = []
        self.completed_worlds = []

    def add_world(self, world):
        self.all_worlds.append(world)
    
    def unlock_worlds(self, character_level):
        for world in self.all_worlds:
            if world.required_level <= character_level and world not in self.unlocked_worlds:
                self.unlocked_worlds.append(world)

    def available_worlds(self, inventory,character):
        accessible = []
        for w in self.unlocked_worlds:
            if not w.completed and w.can_enter(inventory,character):
                accessible.append(w)
        #slow_print(f"Accessible worlds: {[w.name for w in accessible]}")
        return accessible

    def all_completed(self):
        return all(w.completed for w in self.all_worlds)

    def enter_world(self, world_name, character, inventory):
        for world in self.all_worlds:
            if world.name.lower().strip() != world_name.lower().strip():    continue  # Try next world if name doesn't match

            if not world.can_enter(inventory, character):
                slow_print(f"You cannot access '{world.name}' yet. Check requirements.")
                return

            if world.name in self.completed_worlds:
                slow_print(f"\n🌍 You have already completed '{world.name}'. Choose another world.\n")
                return

            # Enter the chosen world
            if world.name == "Fractured Nexus":
                #from final_realm import FracturedNexus
                fractured_nexus = FracturedNexus(character)
                fractured_nexus.enter()
                if getattr(fractured_nexus, "completed", True):
                    self.completed_worlds.append(world.name)
                return

            # Normal world enter
            world.enter(character, inventory)

            if world.completed:
                self.completed_worlds.append(world.name)
            return

        slow_print(f"'{world_name}' not found among the available worlds.")

void_world = World(
    name="The Void",
    description="An empty, eerie place where the journey begins.",
    entry_item=None,
    enemies=[{"name": "Shadowling","level":1, "hp": 15, "attack": 4}],
    items=["Starter Token"],
    xp_reward=50,
    ascii_art='void.txt'
)

# Main Worlds
world_definitions = [
    World(
        name="Emberfall Caverns",
        description="Molten tunnels teeming with fire spirits.",
        entry_item=None,
        enemies=[{"name": "Flame Warden","level":2, "hp": 30, "attack": 8,}],
        items=["Lava Core", "Ash Pendant"],
        xp_reward=120,
        ascii_art='emberfall.txt'
    ),
    World(
        name="Glimmerfen Hollow",
        description="A foggy swamp where illusions roam.",
        entry_item="Ash Pendant",
        enemies=[{"name": "Swamp Wraith","level":4, "hp": 25, "attack": 6}],
        items=["Swamp Herb", "Wind Fragment"],
        xp_reward=130,
        ascii_art='glimmerfen.txt'
    ),
    World(
        name="Obsidian Wastes",
        description="Cracked earth and cursed bones.",
        entry_item="Wind Fragment",
        enemies=[{"name": "Cursed Nomad","level":5, "hp": 35, "attack": 9}],
        items=["Obsidian Shard", "Void Map"],
        xp_reward=150,
        ascii_art='obsidian.txt'
    ),
    World(
        name="Aetherreach Peaks",
        description="Floating islands of air and light.",
        entry_item="Void Map",
        enemies=[{"name": "Sky Watcher","level":6, "hp": 40, "attack": 10}],
        items=["Sky Crystal", "Feather Talisman"],
        xp_reward=160,
        ascii_art='aetherreach.txt'
    ),
    World(
        name="Silversong Tundra",
        description="Frozen plains with spirits of old.",
        entry_item="Sky Crystal",
        enemies=[{"name": "Frost Revenant","level":7, "hp": 45, "attack": 12}],
        items=["Frozen Tear", "Mirror Shard"],
        xp_reward=170,
        ascii_art='silver_song.txt'
    ),
    World(
        name="Sunken Archives",
        description="Drowned ruins holding lost knowledge.",
        entry_item="Mirror Shard",
        enemies=[{"name": "Tide Warden","level":8, "hp": 50, "attack": 14}],
        items=["Memory Scroll", "Nexus Key"],
        xp_reward=180,
        ascii_art='sunken.txt'
    )
]
'''
fractured_nexus = FracturedNexus(
    name="Fractured Nexus",
    description="The crumbling center of reality where all destinies collide.",
    entry_item="Nexus Key",
    enemies=[{"name": "Harbinger of Ends", "level": 10, "hp": 70, "attack": 20}],
    items=["Nexus Shard"],
    xp_reward=250,
    ascii_art='nexus.txt'
)


class FracturedNexus(World):
    def enter(self, character, inventory):
        slow_print("\n🌀 You have entered the Fractured Nexus...")
        slow_print("Time distorts. Realities clash. The realm echoes your entire journey.")

        # Boss encounter
        if self.enemies:
            enemy_data = self.enemies[0]
            final_boss = Enemy(
                name=enemy_data["name"],
                level=enemy_data["level"],
                health=enemy_data["hp"],
                attack=enemy_data["attack"]
            )
            slow_print(f"\n👑 Final Boss: {final_boss.name} appears!")
            combat = Combat(character, inventory)
            combat.start_combat(final_boss)

            if character.health <= 0:
                slow_print("You fell to the Harbinger of Ends. The realms fade into silence...")
                exit()

        # Mark world completed and give rewards
        for item in self.items:
            inventory.add_item(item, 'quest_items')
        character.gain_xp(self.xp_reward)
        self.completed = True

        # Trigger ending
        trigger_final_ending(character)
'''

def setup_worlds():
    world_manager = WorldManager()
    world_manager.add_world(void_world)
    for w in world_definitions: world_manager.add_world(w)
    #world_manager.add_world(fractured_nexus)
    return world_manager


'''
    def enter_world(self, world_name, character, inventory):
        for world in self.all_worlds:
            if world.name.lower().strip() == world_name.lower().strip() and world.can_enter(inventory,character):
                continue
                if world.name in self.completed_worlds:
                    slow_print(f"\n🌍 You have already completed '{world.name}'. Choose another world.\n")
                    return
                if world.can_enter(inventory,character):    world.enter(character, inventory)
                if world.completed and world.name not in self.completed_worlds:
                    self.completed_worlds.append(world.name)
                return
        slow_print(f"You cannot access '{world_name}' yet. Check requirements.")'''