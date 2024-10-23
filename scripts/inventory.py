class Inventory:
    def __init__(self):
        self.items = []  # Empty list for now

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def display_inventory(self):
        # Future: Add logic to display items on the screen
        pass
