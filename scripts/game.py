# scripts/game.py
import pygame
from scripts.character import Character
from scripts.ground import Ground
from scripts.camera import Camera
from scripts.background import Background

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map_width = 2000  # Width of the map
        self.map_height = 600  # Height of the map

        # Initialize background to stretch over the entire map
        self.background = Background(self.map_width, self.map_height)

        # Initialize character, ground, and camera
        self.character = Character(screen.get_width(), screen.get_height())
        self.ground = Ground(0, 500, self.map_width, 100)
        self.camera = Camera(screen.get_width(), screen.get_height(), self.map_width, self.map_height)

    def update(self):
        self.character.update()
        self.camera.update(self.character)  # Pass the character to center the camera
        self.check_collisions()

    def draw(self):
        time = pygame.time.get_ticks() / 1000  # Get time in seconds for sway effect

        # Fill the screen with white color
        self.screen.fill((255, 255, 255))  # RGB for white

        # Draw the background and move it based on the camera's x-offset
        self.background.draw(self.screen, self.camera.offset_x, time)

        # Draw the ground and character with the camera offset applied
        self.screen.blit(self.ground.image, self.camera.apply(self.ground))
        self.screen.blit(self.character.image, self.camera.apply(self.character))

    def check_collisions(self):
        if pygame.sprite.collide_rect(self.character, self.ground):
            self.character.land_on_ground(self.ground.rect.top)
