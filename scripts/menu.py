import pygame
import json
import time
import os
from scripts.game import Game

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
            title = self.font.render("Shoot 'em dead", True, (255, 255, 255))
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
        """Display the load game slots with the ability to delete saves using a trashcan button with a red border, 
        and buttons to return to the main or pause menu."""
        running = True
        slot_height = 60
        delete_mode = False  # Toggle delete mode

        # Load the trashcan image and scale it to an appropriate size
        trashcan_image = pygame.image.load("assets/trashcan.png")
        trashcan_image = pygame.transform.scale(trashcan_image, (40, 40))  # Set the size of the trashcan button

        # Create buttons for returning to main menu and pause menu
        return_main_menu_button = pygame.Rect(300, 500, 200, 50)
        return_pause_menu_button = pygame.Rect(300, 560, 200, 50)

        while running:
            self.screen.fill((0, 0, 0))

            # Draw load game slots with the trashcan button next to each
            for i, save_file in enumerate(self.save_slots):
                slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), slot_rect)

                # Draw the trashcan button with a red border
                trashcan_rect = pygame.Rect(510, 200 + i * slot_height + 5, 40, 40)
                border_rect = pygame.Rect(508, 198 + i * slot_height + 5, 44, 44)  # Slightly larger rect for the border

                # Draw the red border
                pygame.draw.rect(self.screen, (255, 0, 0), border_rect, 2)  # Red border with thickness 2
                self.screen.blit(trashcan_image, trashcan_rect)  # Draw the trashcan image inside the border

                # Check if save file exists and render appropriate text
                if os.path.exists(save_file):
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    save_name = save_data.get('save_name', f'Slot {i+1}')
                    slot_text = self.font.render(save_name, True, (0, 0, 0))
                else:
                    slot_text = self.font.render(f'Slot {i+1} (Empty)', True, (0, 0, 0))

                self.screen.blit(slot_text, (slot_rect.x + 20, slot_rect.y + 10))

            # Draw the buttons for returning to the Main Menu and Pause Menu
            pygame.draw.rect(self.screen, (255, 255, 255), return_main_menu_button)
            pygame.draw.rect(self.screen, (255, 255, 255), return_pause_menu_button)

            # Render button text
            main_menu_text = self.font.render('Return to Main Menu', True, (0, 0, 0))
            pause_menu_text = self.font.render('Return to Pause Menu', True, (0, 0, 0))

            self.screen.blit(main_menu_text, (return_main_menu_button.x + 20, return_main_menu_button.y + 10))
            self.screen.blit(pause_menu_text, (return_pause_menu_button.x + 20, return_pause_menu_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if any trashcan button is clicked
                    for i, save_file in enumerate(self.save_slots):
                        trashcan_rect = pygame.Rect(510, 200 + i * slot_height + 5, 40, 40)
                        if trashcan_rect.collidepoint(mouse_pos) and os.path.exists(save_file):
                            # Delete the save file
                            os.remove(save_file)
                            print(f'Save Slot {i+1} deleted.')

                    # Check if any save slot is clicked (for loading)
                    for i, save_file in enumerate(self.save_slots):
                        slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                        if slot_rect.collidepoint(mouse_pos) and os.path.exists(save_file):
                            # Load the game if the slot is clicked
                            self.load_game(save_file)

                    # Check if the "Return to Main Menu" button is clicked
                    if return_main_menu_button.collidepoint(mouse_pos):
                        from main import main
                        main()  # Call the main menu function

                    # Check if the "Return to Pause Menu" button is clicked
                    if return_pause_menu_button.collidepoint(mouse_pos):
                        running = False  # Close the load game window and return to pause menu

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
                    
                    # Resume game logic
                    if 300 <= mouse_pos[0] <= 500 and 200 <= mouse_pos[1] <= 230:
                        # Resume the game
                        running = False  # Exit the pause menu loop
                        self.game.is_paused = False
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
        """Prompt the player to select a slot and enter a name for the save, with overwrite confirmation."""
        running = True
        slot_height = 60
        save_name = ''  # Store the save name
        selected_slot = None
        overwrite_confirm = False  # Track if we are confirming overwrite

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

            # Input prompt for save name and overwrite confirmation
            if selected_slot is not None:
                # Show the "Enter save name" prompt regardless of whether it's an old save or empty
                prompt_text = self.font.render('Enter save name: ' + save_name, True, (255, 255, 255))
                self.screen.blit(prompt_text, (300, 150))

                if os.path.exists(self.save_slots[selected_slot]):
                    # Overwrite confirmation if the slot already contains a save
                    overwrite_text = self.font.render(f"Overwrite save in Slot {selected_slot+1}?", True, (255, 255, 255))
                    self.screen.blit(overwrite_text, (300, 100))

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
                        if not os.path.exists(self.save_slots[selected_slot]):
                            # Save directly if the slot is empty
                            self.save_game(selected_slot, save_name)
                            running = False
                        elif overwrite_confirm:
                            # Save after confirming overwrite
                            self.save_game(selected_slot, save_name)
                            running = False

                    # Check if any slot is clicked
                    for i, save_file in enumerate(self.save_slots):
                        slot_rect = pygame.Rect(300, 200 + i * slot_height, 200, 50)
                        if slot_rect.collidepoint(mouse_pos):
                            selected_slot = i  # Select the slot
                            overwrite_confirm = os.path.exists(self.save_slots[selected_slot])  # Set overwrite confirmation

                # Handle keyboard input for typing save name or confirming overwrite
                if selected_slot is not None:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            save_name = save_name[:-1]  # Remove the last character
                        elif event.key == pygame.K_RETURN:
                            if overwrite_confirm:
                                # Confirm overwrite if slot exists
                                self.save_game(selected_slot, save_name)
                                running = False
                            elif save_name:
                                # Save normally if no overwrite
                                self.save_game(selected_slot, save_name)
                                running = False
                        elif event.key == pygame.K_y and overwrite_confirm:
                            # Yes to overwrite
                            self.save_game(selected_slot, save_name)
                            running = False
                        elif event.key == pygame.K_n and overwrite_confirm:
                            # No to overwrite, go back to selection
                            overwrite_confirm = False
                        else:
                            # Add typed character for save name
                            save_name += event.unicode

            if not running:
                return



    def save_game(self, slot_index, save_name):
        """Save the game to the selected slot."""
        save_file = self.save_slots[slot_index]

        # Prepare enemy square data to save
        enemy_data = [{
            'x': enemy.rect.x,
            'y': enemy.rect.y,
            'health': enemy.health
        } for enemy in self.game.enemy_squares]  # Collect enemy square data

        # Check if enemy_data has been properly collected
        print(f"Enemy data collected for saving: {enemy_data}")

        # Prepare the game data to save, including enemies
        self.game_data = {
            'save_name': save_name,
            'player_x': self.game.player.rect.x,
            'player_y': self.game.player.rect.y,
            'level': self.game.game_data['level'],
            'player_health': self.game.player.health,
            'enemy_squares': enemy_data  # Save enemy square data
        }
        
        # Write the game data to the save file
        with open(save_file, 'w') as f:
            json.dump(self.game_data, f)
        
        num_enemies = len(self.game.enemy_squares)
        print(f"Game saved in Slot {slot_index + 1} as '{save_name}' with {num_enemies} enemies.")


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