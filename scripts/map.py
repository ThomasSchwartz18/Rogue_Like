import pygame

class Map:
    def __init__(self, width, height, tile_size=25, level=1):
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Load different background images based on the level
        if level == 1:
            self.background_image = pygame.image.load('assets/Level1.png')
        elif level == 2:
            self.background_image = pygame.image.load('assets/Level2.png')
        elif level == 'shop':
            self.background_image = pygame.image.load('assets/Shop.png')  # You can add an image for the shop

        # Scale the background image to fit the map size
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    def draw(self, screen, camera):
        # Draw the background image with the camera's offset
        screen.blit(self.background_image, (-camera.camera.x, -camera.camera.y))
