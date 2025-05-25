import pygame
import sys
from UI_elements import Button
from ascii_art import slow_print_art
from utils import *

# Import your existing modules
from character import Character
from inventory import Inventory
from worlds import setup_worlds
from story import Story
from final_realm import FracturedNexus

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Dungeon Master")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

def draw_text(text, font, color, surface, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)

def run_game():
    # This function runs your existing game logic (console-based for now)
    slow_print("""
    ==================================
        🐉 AI Dungeon Master 🧙‍♂️
    ==================================
    """)
    
    player = Character.create_character()
    player.visited_worlds = []            # Track explored realms
    player.unchosen_skills = []           # For Echoed Self simulation
  
    slow_print(f"Welcome, {player.name} the {player.char_class}!")
    slow_print(format_stats(player))
    inventory = Inventory(player.name)

    world_manager = setup_worlds()
    world_manager.unlock_worlds(player.level)
    available = world_manager.available_worlds(inventory, player)

    game_story = Story(player, inventory, world_manager)
    game_story.start()

    if all(world.completed for world in world_manager.all_worlds):
        slow_print("\n🏁 Next Step: Final Challenge")
        slow_print("“You have explored all available worlds. The final challenge awaits...”")
        enter = input("Do you wish to enter the Fractured Nexus? (yes/no): ").strip().lower()
        if enter in ["yes", "y"]:
            nexus = FracturedNexus(player,inventory)
            nexus.enter()
        else:
            slow_print("You turn away, for now...")

def main_menu():
    button_start = Button(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50, 'Start New Game', font, WHITE, BLACK, GRAY)
    button_load = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, 'Load Game', font, WHITE, BLACK, GRAY)
    button_quit = Button(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50, 'Quit', font, WHITE, BLACK, GRAY)

    buttons = [button_start, button_load, button_quit]

    while True:
        screen.fill(BLACK)
        draw_text('AI Dungeon Master', font, WHITE, screen, WIDTH//2, HEIGHT//4)

        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            button.update(mouse_pos)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                if button.is_clicked(event):
                    if button.text == 'Start New Game':
                        # Run your existing game logic here
                        run_game()
                        # After game ends, return to menu
                    elif button.text == 'Load Game':
                        slow_print("Load Game clicked - feature not implemented yet")
                    elif button.text == 'Quit':
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()

'''
from character import Character
from inventory import Inventory
from worlds import setup_worlds
from story import Story
from final_realm import FracturedNexus
from ascii_art import slow_print_art
from utils import *
def main():
    slow_print("""
    ==================================
        🐉 AI Dungeon Master 🧙‍♂️
    ==================================
    """)

    # Create player character
    player = Character.create_character()
    player.visited_worlds = []            # Track explored realms
    player.unchosen_skills = []           # For Echoed Self simulation
  

    #Character.register_characters(player)
    
    slow_print(f"Welcome, {player.name} the {player.char_class}!")
    slow_print(format_stats(player))

    # Set up inventory and worlds
    inventory = Inventory(player.name)
    world_manager = setup_worlds()

    # Unlock worlds based on level
    world_manager.unlock_worlds(player.level)

    # Fetch available worlds for first display (optional)
    available = world_manager.available_worlds(inventory, player)

    # Start story
    game_story = Story(player, inventory, world_manager)
    game_story.start()

    # Trigger Nexus if all worlds are completed
    if all(world.completed for world in world_manager.all_worlds):
        slow_print("\n🏁 Next Step: Final Challenge")
        slow_print("“You have explored all available worlds. The final challenge awaits...”")
        enter = input("Do you wish to enter the Fractured Nexus? (yes/no): ").strip().lower()
        if enter in ["yes", "y"]:
            nexus = FracturedNexus(player)
            nexus.enter()
        else:
            slow_print("You turn away, for now...")

if __name__ == "__main__":
    main()'''
