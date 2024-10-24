import pygame
import os
import random
import math
from player import Player  # Import the Player class from player.py

class Background:
    def __init__(self, screen_width, screen_height):
        # Load background images
        self.background_images = [
            pygame.image.load('../assets/images/backgrounds/background1.png'),
            pygame.image.load('../assets/images/backgrounds/background2.png'),
            pygame.image.load('../assets/images/backgrounds/background3.png')
        ]

        # Resize the background images to fit the screen size
        self.background_images = [pygame.transform.scale(img, (screen_width, screen_height)) for img in self.background_images]

        # Load cloud images
        self.cloud_images = [
            pygame.image.load(f'../assets/images/backgrounds/cloud{i}.png') for i in range(1, 9)
        ]

        # Set random initial positions for the clouds in the top half of the screen
        self.cloud_positions = []
        for cloud in self.cloud_images:
            x = random.randint(0, screen_width - cloud.get_width())
            y = random.randint(0, screen_height // 2 - cloud.get_height())
            self.cloud_positions.append([x, y, random.uniform(0.5, 1.5)])  # Include a speed factor for each cloud

        # To handle swaying clouds, we will track time for oscillation
        self.time_counter = 0

        # Ground setup (at the bottom of the window)
        self.ground = pygame.Rect(0, screen_height - 50, screen_width, 50)  # Ground at the bottom

    def update(self):
        # Increase the time counter for cloud sway
        self.time_counter += 0.02  # Adjust the sway speed by changing this value

        # Update the cloud positions to make them sway gently
        for i, pos in enumerate(self.cloud_positions):
            sway_magnitude = 0.25  # Much smaller sway magnitude for gentle cloud movement
            pos[1] += math.sin(self.time_counter * pos[2]) * sway_magnitude  # Apply slight vertical oscillation

    def draw(self, screen):
        # Draw background layers (background1 at the back, followed by background2 and background3)
        for bg_image in self.background_images:
            screen.blit(bg_image, (0, 0))

        # Draw clouds
        for i, cloud in enumerate(self.cloud_images):
            screen.blit(cloud, (self.cloud_positions[i][0], self.cloud_positions[i][1]))

        # Draw ground
        pygame.draw.rect(screen, (0, 128, 0), self.ground)  # Ground is green

# Initialize Pygame and set up the screen
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Initialize the background and the player using the Player class from player.py
background = Background(screen_width, screen_height)
player = Player(100, screen_height - 100)  # Start player just above the ground

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the background and cloud positions
    background.update()

    # Update the player with ground collision
    player.update(background.ground, screen)

    # Draw everything
    screen.fill((255, 255, 255))  # Fill the screen with white (optional)
    background.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
