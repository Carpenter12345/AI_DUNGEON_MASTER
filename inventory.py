from utils import *
class Inventory:
    def __init__(self, character_name, level=1):
        self.character_name = character_name
        self.level = level
        self.max_slots = self.calculate_max_slots()
        self.items = {
            "weapons": [],
            "armor": [],
            "potions": [],
            "quest_items": [],
            "misc": []
        }
        self.storage = {
            "weapons": [],
            "armor": [],
            "potions": [],
            "quest_items": [],
            "misc": []
        }
        # Track order of acquisition to know which items are oldest
        self.item_acquisition_order = []

    def calculate_max_slots(self):
        # Unlocks +2 slots every 3 levels, starting from 10
        return 10 + (self.level // 3) * 2

    def update_level(self, new_level):
        self.level = new_level
        self.max_slots = self.calculate_max_slots()

    def total_items(self):
        return sum(len(lst) for lst in self.items.values())

    def has_space(self):
        return self.total_items() < self.max_slots

    def add_item(self, item_name, category):
        if category not in self.items:
            slow_print(f"Invalid category: {category}")
            return False

        # Try to free space if needed
        if not self.has_space():
            slow_print("Inventory full! Trying to free space by moving items to storage...")
            self.auto_move_first_three_to_storage()

            # Try to retrieve some items back if space is available
            if not self.has_space():
                self.auto_retrieve_to_inventory()

            if not self.has_space():
                slow_print("Still no space after moving items. Consider removing items manually.")
                return False

        self.items[category].append(item_name)
        self.item_acquisition_order.append((item_name, category))
        slow_print(f"Added {item_name} to {category}.")
        return True

    def remove_item(self, item_name):
        for category in self.items:
            if item_name in self.items[category]:
                self.items[category].remove(item_name)
                self.item_acquisition_order = [x for x in self.item_acquisition_order if x[0] != item_name]
                slow_print(f"Removed {item_name} from inventory.")
                # Try to retrieve items from storage now that space freed
                self.auto_retrieve_to_inventory()
                return True
        slow_print(f"{item_name} not found in inventory.")
        return False

    def use_item(self, item_name):
        for category in self.items:
            if item_name in self.items[category]:
                self.items[category].remove(item_name)
                self.item_acquisition_order = [x for x in self.item_acquisition_order if x[0] != item_name]
                slow_print(f"You used {item_name}.")
                # Try to retrieve items from storage now that space freed
                self.auto_retrieve_to_inventory()
                return item_name
        slow_print(f"{item_name} not available to use.")
        return None

    def equip_item(self, item_name):
        if item_name in self.items["weapons"] or item_name in self.items["armor"]:
            slow_print(f"{self.character_name} has equipped {item_name}.")
            return item_name
        slow_print(f"{item_name} cannot be equipped.")
        return None

    def list_items(self):
        slow_print(f"Inventory for {self.character_name} (Level {self.level}) — {self.total_items()}/{self.max_slots} slots used:")
        for category, items in self.items.items():
            if items:
                slow_print(f"  {category.title()}: {', '.join(items)}")
        self.list_storage()

    def has_item(self, item_name):
        for category in self.items:
            if item_name in self.items[category]:
                return True
        return False

    def get_items_by_category(self, category):
        return self.items.get(category, [])

    def clear_inventory(self):
        for category in self.items:
            self.items[category] = []
        self.item_acquisition_order = []
        slow_print("Inventory cleared.")

    # --- Storage methods ---

    def move_to_storage(self, item_name):
        for category in self.items:
            if item_name in self.items[category]:
                self.items[category].remove(item_name)
                self.storage[category].append(item_name)
                self.item_acquisition_order = [x for x in self.item_acquisition_order if x[0] != item_name]
                slow_print(f"Moved {item_name} to storage.")
                return True
        return False

    def retrieve_from_storage(self, item_name):
        for category in self.storage:
            if item_name in self.storage[category]:
                if self.has_space():
                    self.storage[category].remove(item_name)
                    self.items[category].append(item_name)
                    self.item_acquisition_order.append((item_name, category))
                    slow_print(f"Moved {item_name} from storage to inventory.")
                    return True
                else:
                    slow_print("No space to retrieve items from storage.")
                    return False
        return False

    def list_storage(self):
        slow_print(f"Storage for {self.character_name}:")
        total_storage = sum(len(lst) for lst in self.storage.values())
        slow_print(f"  {total_storage} items stored.")
        for category, items in self.storage.items():
            if items:
                slow_print(f"    {category.title()}: {', '.join(items)}")

    def auto_move_first_three_to_storage(self):
        moved_count = 0
        for item_name, category in list(self.item_acquisition_order):
            if moved_count >= 3:
                break
            # Skip keys or important quest items containing 'key'
            if category == "quest_items" and "key" in item_name.lower():
                continue
            if item_name in self.items[category]:  
                if self.move_to_storage(item_name):
                    moved_count += 1
        #slow_print(f"Auto-moved {moved_count} items to storage.")

    def auto_retrieve_to_inventory(self):
        retrieved_count = 0
        # Try to bring items back from storage if inventory has space
        for category in list(self.storage.keys()):
            for item_name in list(self.storage[category]):
                if self.has_space():
                    if self.retrieve_from_storage(item_name):
                        retrieved_count += 1
                else:
                    slow_print(f"Inventory full while retrieving items.")
                    slow_print(f"Auto-retrieved {retrieved_count} items from storage to inventory.")
                    return
        slow_print(f"Auto-retrieved {retrieved_count} items from storage to inventory.")

    def complete_world(self):
        slow_print(f"World complete! Managing inventory and storage...")
        self.auto_move_first_three_to_storage()
        self.list_items()
