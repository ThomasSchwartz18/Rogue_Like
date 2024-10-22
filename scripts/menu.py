import pygame
import json
import time
import os
from scripts.game import Game  # Import the Game class

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.new_game_button = pygame.Rect(300, 250, 200, 50)  # (x, y, width, height)
        self.load_game_button = pygame.Rect(300, 350, 200, 50)
        self.save_slots = [f'save_slot_{i}.json' for i in range(1, 5)]  # Four save slots

    def display(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            # Render button text
            title = self.font.render('Simple Platformer', True, (255, 255, 255))
            new_game_text = self.font.render('New Game', True, (0, 0, 0))
            load_game_text = self.font.render('Load Game', True, (0, 0, 0))

            # Draw buttons as rectangles
            pygame.draw.rect(self.screen, (255, 255, 255), self.new_game_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.load_game_button)

            # Blit text onto buttons and title
            self.screen.blit(title, (300, 150))
            self.screen.blit(new_game_text, (self.new_game_button.x + 40, self.new_game_button.y + 10))
            self.screen.blit(load_game_text, (self.load_game_button.x + 40, self.load_game_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_game_button.collidepoint(event.pos):
                        return 'new_game'
                    if self.load_game_button.collidepoint(event.pos):
                        self.display_load_slots()

        pygame.quit()

    def display_load_slots(self):
        """Display the load game slots with the ability to delete saves."""
        running = True
        slot_height = 60
        delete_mode = False  # Toggle delete mode

        while running:
            self.screen.fill((0, 0, 0))

            # Render a delete button
            delete_button_rect = pygame.Rect(550, 50, 100, 50)
            delete_button_text = self.font.render('Delete', True, (255, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), delete_button_rect)
            self.screen.blit(delete_button_text, (delete_button_rect.x + 20, delete_button_rect.y + 10))

            # Draw load game slots
            for i, save_file in enumerate(self.save_slots):
                slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), slot_rect)

                # Check if save file exists and render appropriate text
                if os.path.exists(save_file):
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    save_name = save_data.get('save_name', f'Slot {i+1}')
                    slot_text = self.font.render(save_name, True, (0, 0, 0))
                else:
                    slot_text = self.font.render(f'Slot {i+1} (Empty)', True, (0, 0, 0))

                self.screen.blit(slot_text, (slot_rect.x + 20, slot_rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the delete button is clicked
                    if delete_button_rect.collidepoint(mouse_pos):
                        delete_mode = not delete_mode  # Toggle delete mode

                    # Check if any save slot is clicked
                    for i, save_file in enumerate(self.save_slots):
                        slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                        if slot_rect.collidepoint(mouse_pos):
                            if delete_mode and os.path.exists(save_file):
                                # Delete the save file
                                os.remove(save_file)
                                print(f'Save Slot {i+1} deleted.')
                            elif not delete_mode and os.path.exists(save_file):
                                # Load the game if not in delete mode
                                self.load_game(save_file)

    def load_game(self, save_file):
        """Load the selected save game and return the saved data."""
        with open(save_file, 'r') as f:
            save_data = json.load(f)
        
        # Create a new Game instance and load the save data into it
        game = Game(self.screen)
        game.load_save_data(save_data)  # Custom method to load saved data into the game
        game.play()  # Resume the game


class PauseMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.pause_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.pause_surface.fill((50, 50, 50, 150))  # Semi-transparent background
        self.save_slots = [f'save_slot_{i}.json' for i in range(1, 5)]  # Four save slots

    def display(self):
        running = True
        while running:
            self.screen.blit(self.pause_surface, (0, 0))

            resume_game_button = self.font.render('Resume Game', True, (255, 255, 255))
            save_game_button = self.font.render('Save Game', True, (255, 255, 255))
            quit_game_button = self.font.render('Quit to Main Menu', True, (255, 255, 255))

            self.screen.blit(resume_game_button, (300, 200))
            self.screen.blit(save_game_button, (300, 250))
            self.screen.blit(quit_game_button, (300, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if 300 <= mouse_pos[0] <= 500 and 250 <= mouse_pos[1] <= 280:
                        self.save_game_prompt()
                    if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 380:
                        from main import main
                        main()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
                self.game.is_paused = False
                self.game.play()

    def save_game_prompt(self):
        """Prompt the player to select a slot and enter a name for the save."""
        running = True
        slot_height = 60
        save_name = ''  # Store the save name
        selected_slot = None

        while running:
            self.screen.fill((0, 0, 0))

            # Draw load game slots
            for i, save_file in enumerate(self.save_slots):
                slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), slot_rect)

                # Check if save file exists and render appropriate text
                if os.path.exists(save_file):
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    save_name_display = save_data.get('save_name', f'Slot {i+1}')
                    slot_text = self.font.render(save_name_display, True, (0, 0, 0))
                else:
                    slot_text = self.font.render(f'Slot {i+1} (Empty)', True, (0, 0, 0))

                self.screen.blit(slot_text, (slot_rect.x + 20, slot_rect.y + 10))

                # Highlight the selected slot
                if selected_slot == i:
                    pygame.draw.rect(self.screen, (0, 255, 0), slot_rect, 3)

            # Input prompt for save name
            if selected_slot is not None and not os.path.exists(self.save_slots[selected_slot]):
                prompt_text = self.font.render('Enter save name: ' + save_name, True, (255, 255, 255))
                self.screen.blit(prompt_text, (300, 150))

            # Save button
            save_button_rect = pygame.Rect(350, 450, 100, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), save_button_rect)
            save_button_text = self.font.render('Save', True, (0, 0, 0))
            self.screen.blit(save_button_text, (save_button_rect.x + 20, save_button_rect.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the save button is clicked
                    if save_button_rect.collidepoint(mouse_pos) and selected_slot is not None and save_name:
                        self.save_game(selected_slot, save_name)
                        running = False

                    # Check if any slot is clicked
                    for i, save_file in enumerate(self.save_slots):
                        slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                        if slot_rect.collidepoint(mouse_pos) and not os.path.exists(save_file):
                            selected_slot = i  # Select the slot

                # Handle keyboard input for typing save name
                if selected_slot is not None:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            save_name = save_name[:-1]  # Remove the last character
                        elif event.key == pygame.K_RETURN:
                            # Press Enter to confirm the save
                            self.save_game(selected_slot, save_name)
                            running = False
                        else:
                            save_name += event.unicode  # Add typed character

        if not running:
            return

    def save_game(self, slot_index, save_name):
        """Save the game to the selected slot."""
        save_file = self.save_slots[slot_index]
        self.game_data = {
            'save_name': save_name,
            'player_x': self.game.player.rect.x,
            'player_y': self.game.player.rect.y,
            'level': self.game.game_data['level'],
            'player_health': self.game.player.health
        }
        with open(save_file, 'w') as f:
            json.dump(self.game_data, f)
        print(f"Game saved in Slot {slot_index + 1} as '{save_name}'")

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 72)  # Large font for the "Game Over" message
        self.timer_font = pygame.font.Font(None, 36)  # Smaller font for the timer
        self.game_over_duration = 5  # Game over screen duration (5 seconds)
        self.start_time = time.time()  # Record the start time of the game over screen

    def display(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Fill the screen with black

            # Render the "Game Over" message
            game_over_text = self.font.render('Game Over', True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, self.screen.get_height() // 2 - 100))

            # Calculate remaining time and display it
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.game_over_duration - elapsed_time)
            timer_text = self.timer_font.render(f'Returning to main menu in {int(remaining_time)}...', True, (255, 255, 255))
            self.screen.blit(timer_text, (self.screen.get_width() // 2 - timer_text.get_width() // 2, self.screen.get_height() // 2 + 50))

            pygame.display.flip()

            # Exit the loop after the timer reaches 0
            if remaining_time <= 0:
                running = False
                return 'main_menu'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()