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
        
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load and play background music on loop
        pygame.mixer.music.load('assets/sound/Soundtrack.mp3')
        pygame.mixer.music.set_volume(0.5)  # Adjust volume to 50%
        pygame.mixer.music.play(-1)  # Play the soundtrack on repeat

        self.map_level = 1  # Start at level 1
        
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

        # Initialize the font for the kill counter
        self.font = pygame.font.Font(None, 36)  # Adjust font size as needed
        
        # List to hold enemy squares
        self.enemy_squares = []
        self.killed_enemies = 0  # Track the number of enemies killed
        
        # Spawn timer (to spawn enemies every few seconds)
        self.spawn_timer = 0
        self.spawn_interval = 180  # Spawn an enemy every 180 frames (3 seconds at 60 FPS)
        
        # Doorway variables
        # Initialize the doorway at the top center of the map
        self.doorway_open = False
        self.doorway_width = 100
        self.doorway_height = 50
        # Create a rect for the doorway at the top center of the map
        self.doorway_rect = pygame.Rect(self.map.width // 2 - self.doorway_width // 2, 0, self.doorway_width, self.doorway_height)

    def spawn_enemy_square(self):
        # Randomly spawn the enemy at the edges of the map
        spawn_x = random.choice([0, self.map.width - 40])
        spawn_y = random.choice([0, self.map.height - 40])
        
        # Create an enemy square targeting the player
        enemy_square = EnemySquare(spawn_x, spawn_y, self.player.rect)
        self.enemy_squares.append(enemy_square)

        # Print debugging information to check if enemies are being spawned and added
        print(f"Enemy spawned at ({spawn_x}, {spawn_y}). Total enemies: {len(self.enemy_squares)}")

    def check_doorway(self):
        """Check if the player enters the doorway."""
        if self.doorway_open and self.player.rect.colliderect(self.doorway_rect):
            if self.map_level == 'shop':
                print("Entering Level 2...")
                self.transition_to_next_map()  # Transition to the second level
            else:
                print("Entering the shop room...")
                self.transition_to_shop()  # Transition to the shop room after defeating 10 enemies

    def display_enter_prompt(self):
        """Display a prompt to press 'E' when near the doorway."""
        prompt_text = self.font.render('Press E to open', True, (255, 255, 255))  # White text
        prompt_rect = prompt_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))  # Center the prompt
        self.screen.blit(prompt_text, prompt_rect)  # Render the prompt on the screen


    def transition_to_shop(self):
        """Transition to the shop room after defeating 10 enemies."""
        self.map_level = 'shop'  # Set this as the shop level
        self.map = Map(1000, 1000, tile_size=25, level=self.map_level)  # Shop room is smaller

        # Set the player’s position at the center of the shop
        self.player.rect.x = self.map.width // 2 - self.player.rect.width // 2
        self.player.rect.y = self.map.height - self.player.rect.height

        # Reposition the shop doorway that leads to Level 2
        self.doorway_rect = pygame.Rect(self.map.width // 2 - self.doorway_width // 2, 0, self.doorway_width, self.doorway_height)

        print("Entered the shop room.")
    
    def transition_to_next_map(self):
        """Transition to the next map (Level 2)."""
        self.map_level = 2  # Set to Level 2
        self.map = Map(2000, 2000, tile_size=25, level=self.map_level)

        # Set the player's position at the bottom center of Level 2
        self.player.rect.x = self.map.width // 2 - self.player.rect.width // 2
        self.player.rect.y = self.map.height - self.player.rect.height

        # Update the doorway rect for Level 2
        self.doorway_rect = pygame.Rect(self.map.width // 2 - self.doorway_width // 2, 0, self.doorway_width, self.doorway_height)

        print("Transitioned to Level 2.")

                
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
            # Recreate each enemy square with saved position and health
            enemy_square = EnemySquare(enemy_info['x'], enemy_info['y'], self.player.rect)
            enemy_square.health = enemy_info['health']
            self.enemy_squares.append(enemy_square)
        
        print(f"Loaded {len(self.enemy_squares)} enemies from save.")

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

        # Draw the doorway if open and apply the camera to its position
        if self.doorway_open:
            doorway_position = self.doorway_rect.move(-self.camera.camera.x, -self.camera.camera.y)
            pygame.draw.rect(self.screen, (255, 255, 0), doorway_position)  # Draw a yellow doorway

        # Spawn enemy squares based on the spawn timer
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy_square()
            self.spawn_timer = 0  # Reset the timer

        # List to track dead enemies
        dead_enemies = []  # List to track dead enemies

        for enemy in self.enemy_squares[:]:
            enemy.update()
            enemy.draw(self.screen, self.camera)

            # Check if the enemy square is colliding with the player
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10)  # Deal 10 damage if the enemy touches the player

            # Check if the enemy is dead after being damaged by the laser
            if enemy.health <= 0:  # Check if the enemy is dead
                dead_enemies.append(enemy)  # Track dead enemies

        # Remove dead enemies and update kill count
        for dead_enemy in dead_enemies:
            self.enemy_squares.remove(dead_enemy)  # Remove the dead enemy
            self.killed_enemies += 1  # Increment kill count
            print(f"Enemies killed: {self.killed_enemies}")
            if self.killed_enemies >= 10:
                self.doorway_open = True  # Open the doorway if all enemies are killed
                print("All enemies are defeated! Opening doorway...")

        # Check if the player enters the doorway
        self.check_doorway()

        # Always draw the health and stamina bars last, so they appear on top of everything
        self.player.draw_health_bar(self.screen)
        self.player.draw_stamina_bar(self.screen)
        
        # Draw the kill counter at the top right
        self.draw_kill_counter()

        pygame.display.flip()  # Make sure the screen updates every frame


    def draw_kill_counter(self):
        # Render the kill counter text
        kill_counter_text = self.font.render(f'Kills: {self.killed_enemies}', True, (255, 255, 255))  # White color
        kill_counter_rect = kill_counter_text.get_rect(topright=(self.window_width - 20, 20))  # Position it top right
        self.screen.blit(kill_counter_text, kill_counter_rect)


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

        # Check if enemy_data has been properly collected
        print(f"Enemy data collected for saving: {enemy_data}")

        # Prepare the game data to save
        self.game_data = {
            'save_name': save_name,
            'player_x': self.player.rect.x,
            'player_y': self.player.rect.y,
            'player_health': self.player.health,
            'level': self.game_data['level'],
            'enemy_squares': enemy_data  # Include enemy square data
        }
        
        # Write the game data to the save file
        with open(save_file, 'w') as f:
            json.dump(self.game_data, f)
        
        num_enemies = len(self.enemy_squares)
        print(f"Game saved in Slot {slot_index + 1} as '{save_name}' with {num_enemies} enemies.")




            
    def game_over(self):
        from scripts.menu import GameOverScreen  # Dynamic import for GameOverScreen
        game_over_screen = GameOverScreen(self.screen)
        result = game_over_screen.display()

        # Return to main menu if the timer runs out
        if result == 'main_menu':
            from main import main
            main()
