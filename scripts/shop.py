class Shop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.upgrade_options = [
            {"name": "Upgrade Speed", "cost": 50, "upgrade_function": self.player.upgrade_speed, "upgrade_amount": 1},
            {"name": "Upgrade Damage", "cost": 100, "upgrade_function": self.player.upgrade_damage, "upgrade_amount": 5},
            {"name": "Upgrade Dash Distance", "cost": 75, "upgrade_function": self.player.upgrade_dash_distance, "upgrade_amount": 20},
        ]
        self.coins = 200  # Set initial coins for testing

    def display(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            # Display shop options and player coins
            title = self.font.render("Shop - Buy Upgrades", True, (255, 255, 255))
            coins_text = self.font.render(f"Coins: {self.coins}", True, (255, 255, 0))
            self.screen.blit(title, (100, 50))
            self.screen.blit(coins_text, (100, 100))

            for i, option in enumerate(self.upgrade_options):
                option_text = self.font.render(f"{option['name']} - {option['cost']} Coins", True, (255, 255, 255))
                self.screen.blit(option_text, (100, 150 + i * 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.upgrade_options):
                        if 100 <= mouse_pos[0] <= 400 and 150 + i * 50 <= mouse_pos[1] <= 200 + i * 50:
                            self.purchase_upgrade(option)

    def purchase_upgrade(self, option):
        """Purchase the upgrade if the player has enough coins."""
        if self.coins >= option["cost"]:
            self.coins -= option["cost"]
            option["upgrade_function"](option["upgrade_amount"])  # Call the upgrade function
            print(f"Purchased {option['name']}. Remaining coins: {self.coins}")
        else:
            print("Not enough coins!")
