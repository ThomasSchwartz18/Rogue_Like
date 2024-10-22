import pygame
import json

from scripts.character import Character
from scripts.camera import Camera
from scripts.map import Map
from scripts.enemy_square import EnemySquare



import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.window_width, self.window_height = screen.get_size()
        self.is_paused = False

        # Initialize the game map (larger than the window)
        self.map = Map(2000, 2000, tile_size=25)  # Map size and tile size (e.g., 50 for each checkered tile)

        # Initialize the camera with the size of the window and the size of the map
        self.camera = Camera(self.window_width, self.window_height, self.map.width, self.map.height)

        # Calculate the center of the map for the player's spawn position
        map_center_x = self.map.width // 2
        map_center_y = self.map.height // 2

        # Load the pause button image and resize it to 50x50 pixels
        self.pause_button_image = pygame.image.load("assets/PauseButton.png")
        self.pause_button_image = pygame.transform.scale(self.pause_button_image, (50, 50))
        self.pause_button_rect = self.pause_button_image.get_rect(bottomright=(self.window_width - 10, self.window_height - 10))

        # Initialize the player at the center of the map
        self.game_data = {
            'player_x': map_center_x,
            'player_y': map_center_y,
            'level': 1,
            'player_health': 100
        }
        self.player = Character(self.game_data['player_x'], self.game_data['player_y'], self.map.width, self.map.height)

        # List to hold enemy squares
        self.enemy_squares = []
        
        # Spawn timer (to spawn enemies every few seconds)
        self.spawn_timer = 0
        self.spawn_interval = 180  # Spawn an enemy every 180 frames (3 seconds at 60 FPS)

    def spawn_enemy_square(self):
        # Randomly spawn the enemy at the edges of the map
        spawn_x = random.choice([0, self.map.width - 40])
        spawn_y = random.choice([0, self.map.height - 40])
        
        # Create an enemy square targeting the player
        enemy_square = EnemySquare(spawn_x, spawn_y, self.player.rect)
        self.enemy_squares.append(enemy_square)
        
    def load_save_data(self, save_data):
        """Load the save data into the current game."""
        # Load player data
        self.game_data['player_x'] = save_data['player_x']
        self.game_data['player_y'] = save_data['player_y']
        self.game_data['level'] = save_data['level']
        self.player.rect.x = save_data['player_x']
        self.player.rect.y = save_data['player_y']
        self.player.health = save_data.get('player_health', 100)
        
        # Load enemy squares from the save data
        self.enemy_squares = []  # Clear any existing enemies

        enemy_squares_data = save_data.get('enemy_squares', [])
        print(f"Loading {len(enemy_squares_data)} enemies")  # Debugging print
        
        for enemy_info in enemy_squares_data:
            enemy_square = EnemySquare(enemy_info['x'], enemy_info['y'], self.player.rect)
            enemy_square.health = enemy_info['health']
            self.enemy_squares.append(enemy_square)

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for clicking on the pause button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        self.is_paused = True
                        self.pause_game()

            # Only update the game if it's not paused
            if not self.is_paused:
                self.update_game()

            # Render the pause button in the bottom right
            self.screen.blit(self.pause_button_image, self.pause_button_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def update_game(self):
        self.screen.fill((0, 0, 0))  # Background for the window (black)

        # Update player movement
        self.player.update()

        # Check if the player is still alive
        if self.player.health <= 0:
            self.game_over()

        # Update the camera to keep the player centered
        self.camera.update(self.player)

        # Draw the map (relative to the camera)
        self.map.draw(self.screen, self.camera)

        # Apply the camera offset to the player before drawing
        player_position = self.camera.apply(self.player)
        self.player.draw(self.screen, player_position, self.camera, self.enemy_squares)  # Pass enemy_squares

        # Spawn enemy squares based on the spawn timer
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy_square()
            self.spawn_timer = 0  # Reset the timer

        # Update and draw all enemy squares
        for enemy in self.enemy_squares[:]:
            enemy.update()
            enemy.draw(self.screen, self.camera)

            # Check if the enemy square is colliding with the player
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10)  # Deal 10 damage if the enemy touches the player

        # Always draw the health and stamina bars last, so they appear on top of everything
        self.player.draw_health_bar(self.screen)
        self.player.draw_stamina_bar(self.screen)

    def pause_game(self):
        from scripts.menu import PauseMenu  # Dynamic import to avoid circular import issues
        pause_menu = PauseMenu(self.screen, self)
        pause_menu.display()

    def save_game(self, slot_index, save_name):
        """Save the game to the selected slot."""
        save_file = self.save_slots[slot_index]
        
        # Prepare enemy square data to save
        enemy_data = [{
            'x': enemy.rect.x,
            'y': enemy.rect.y,
            'health': enemy.health
        } for enemy in self.enemy_squares]
        
        print(f"Saving {len(self.enemy_squares)} enemies")  # Debugging print

        # Prepare the game data to save
        self.game_data = {
            'save_name': save_name,
            'player_x': self.player.rect.x,
            'player_y': self.player.rect.y,
            'player_health': self.player.health,
            'level': self.game_data['level'],
            'enemy_squares': enemy_data
        }
        
        with open(save_file, 'w') as f:
            json.dump(self.game_data, f)
        print(f"Game saved in Slot {slot_index + 1} as '{save_name}'")

            
    def game_over(self):
        from scripts.menu import GameOverScreen  # Dynamic import for GameOverScreen
        game_over_screen = GameOverScreen(self.screen)
        result = game_over_screen.display()

        # Return to main menu if the timer runs out
        if result == 'main_menu':
            from main import main
            main()
