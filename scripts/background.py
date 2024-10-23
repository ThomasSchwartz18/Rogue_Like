# scripts/background.py
import pygame
import os
import math

class Background:
    def __init__(self, map_width, map_height):
        # Assign map dimensions to instance variables
        self.map_width = map_width
        self.map_height = map_height

        self.images = self.load_background_images()

        # Sway settings for smoother motion
        self.sway_amplitude = 5  # Reduce amplitude for a more subtle sway
        self.sway_speed = 0.2  # Slow down the sway for smoother motion
        self.sway_offsets = [i * 100 for i in range(len(self.images))]  # Offset each image sway

    def load_background_images(self):
        # Load all images from the 'assets/background1' folder
        background_images = []
        background_folder = "assets/background1"
        for filename in os.listdir(background_folder):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(background_folder, filename)).convert_alpha()
                # Now stretch the images to fit the whole map
                img = pygame.transform.scale(img, (self.map_width, self.map_height))
                background_images.append(img)
        return background_images

    def draw(self, screen, camera_offset_x, time):
        for i, img in enumerate(self.images):
            # Calculate vertical sway offset for each image with smoother motion
            sway_offset_y = self.sway_amplitude * math.sin(self.sway_speed * time + self.sway_offsets[i])

            # Offset the background position based on the camera's x-offset
            background_x = -camera_offset_x * (0.5 + (i * 0.05))  # Each layer moves at a different speed for parallax
            screen.blit(img, (background_x, sway_offset_y))  # Apply vertical sway and movement
