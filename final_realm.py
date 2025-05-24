from character import Character
from ascii_art import slow_print_art
from utils import *
class FracturedNexus:
    def __init__(self, player):
        self.player = player
        self.echo = self.generate_echoed_self()
        self.completed=False

    def enter(self):
        slow_print_art('nexus.txt')
        slow_print("\n🌀 You have entered the Fractured Nexus...")
        slow_print("Time distorts. Realities clash. The realm echoes your entire journey.\n")
        self.describe_realm_fragments()
        self.class_trial()
        self.final_battle()
        self.ending_choice()

    def describe_realm_fragments(self):
        slow_print("Fragments of the realms you've visited float in the void:")
        for world in self.player.visited_worlds:
            slow_print(f" - The essence of {world.name} shimmers in the air...")

    def class_trial(self):
        slow_print("\n🌌 A challenge forms, tailored to your very soul...")

        class_name = self.player.char_class
        if class_name == "Knight":
            slow_print("You face innocent villagers surrounded by enemies — but your sword is gone.")
            input("Will you protect them without violence? (Press Enter to decide...)")
        elif class_name == "Mage":
            slow_print("A tome offers you absolute power at the cost of your memories...")
            input("Do you open it? (Press Enter...)")
        elif class_name == "Alchemist":
            slow_print("A loyal creature offers itself to become the key forward. Do you accept?")
            input("Your transmutation will be irreversible. (Press Enter...)")
        elif class_name == "Rogue":
            slow_print("A shadow-self mocks you — a Rogue who never cared. Will you confront or become it?")
            input("Your decision defines your legacy. (Press Enter...)")
        elif class_name == "Necromancer":
            slow_print("Your army of souls turns on you — do you suppress or surrender?")
            input("Their pain mirrors yours. Choose. (Press Enter...)")
        elif class_name == "Ashborn":
            slow_print("You stand before your destined form — divine and monstrous.")
            input("Will you embrace it or forge your own path? (Press Enter...)")

    def generate_echoed_self(self):
        unused_paths = self.player.unchosen_skills or ["Forgotten Power", "Lost Potential"]
        echo = {
            "name": "The Echoed Self",
            "traits": unused_paths,
            "strength": self.player.level + 3,
            "flavor": f"A reflection of what you *could* have become."
        }
        return echo

    def final_battle(self):
        from combat import Combat, Enemy

        slow_print(f"\n⚔️ The {self.echo['name']} manifests...")
        slow_print(f"It wields: {', '.join(self.echo['traits'])}")
        slow_print("It speaks: 'You walked away from power. I *became* it.'")

        input("Prepare to face yourself... (Press Enter to battle!)")

    # Create the Echoed Self as an actual enemy
        echoed_self = Enemy(
            name=self.echo["name"],
            level=self.player.level*2,
            health=120,
            attack=self.player.attack + 5,
            #abilities=self.echo["traits"]
        )

        combat = Combat(self.player, echoed_self)
        outcome = combat.start_combat(echoed_self)

        if outcome == "player": 
            slow_print("\n🔥 You conquer the Echo. The realm quiets...")
        else:   
            slow_print("\n💀 You fall. But perhaps, in falling, you learn...")


    def battle_simulation(self):
        import random
        win_chance = 0.6 if self.player.level > 5 else 0.3
        return "win" if random.random() < win_chance else "lose"

    def ending_choice(self):
        slow_print("\nThe Echo fades. The Nexus responds to your will.")
        slow_print("You may:")
        slow_print("1. Fracture reality and create a new realm (Power Ending)")
        slow_print("2. Heal the realm, restoring balance (Harmony Ending)")
        slow_print("3. Walk away into the unknown (Mystery Ending)")

        choice = input("Choose your fate (1/2/3): ")
        if choice == "1":
            slow_print("🌑 A new world is born in your image. You are legend.")
        elif choice == "2":
            slow_print("🌕 Light returns. The realms realign. You are at peace.")
        else:
            slow_print("🌫️ You vanish beyond the veil. Your journey becomes myth.")
        

        if self.player.char_class == "Knight":
            slow_print("🛡️ As a Knight, your legacy will guard the realm for generations.")
        elif self.player.char_class == "Mage":
            slow_print("📚 As a Mage, your knowledge rewrites the fate of worlds.")
        elif self.player.char_class == "Rogue":
            slow_print("🗡️ As a Rogue, your name becomes legend in whispered tales.")
        elif self.player.char_class == "Alchemist":
            slow_print("⚗️ As an Alchemist, you transform the fractured realm into harmony.")
        elif self.player.char_class == "Necromancer":
            slow_print("💀 As a Necromancer, the realm kneels to your will beyond death.")
        elif self.player.char_class == "Ashborn":
            slow_print("🔥 As Ashborn, you ascend beyond form—becoming the eternal flame of rebirth.")

        slow_print("\n And so, the final chapter closes. The echoes of your deeds shall linger through the ages.\n")



