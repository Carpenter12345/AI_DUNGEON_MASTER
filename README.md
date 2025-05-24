# AI Dungeon Master

AI Dungeon Master is a Python-based text adventure game where players choose a character class and embark on a branching narrative adventure across diverse, mysterious worlds. 
Every class—from the stoic Knight to the enigmatic Ashborn—offers a unique gameplay experience with secrets to uncover and quests to complete.

## 🚀 Features

- **6 Unique Character Classes**: Knight, Mage, Rogue, Alchemist, Necromancer, and Ashborn (a hidden evolving class).
- **7 Explorable Worlds**: Traverse through multiple custom-designed worlds including the final realm: **Fractured Nexus**.
- **Combat System**: Turn-based battles against a variety of enemies.
- **Inventory & Items**: Pick up and use items that affect your journey.
- **Choice-Based Narrative**: Decisions shape your story and character evolution.
- **Ashborn Awakening Mechanic**: A hidden transformation mechanic triggered on death after level 5.

## 🧩 Project Structure

```bash
AI-Dungeon-Master/
├── main.py                  # Main game loop and entry point
├── character.py             # Character classes and logic
├── inventory.py             # Inventory system and item management
├── worlds.py                # Contains all the access to the worlds
├── story.py                 # Handles narrative progression
├── final_realm.py           # End-game challenge logic
├── combat.py                # Combat mechanics and enemy logic
├── utils.py                 # Utility functions
│── ascii_art.py             # Function to access the ascii_art assigned to worlds and characters  
|-- UI_elements.py           # Some basic UI  
└── README.md                # Project documentation
