# scripts/ground.py
import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))

        # Load the tile image
        tile_image = pygame.image.load("assets/images/tile.png").convert()

        # Get the dimensions of the tile
        tile_width = tile_image.get_width()
        tile_height = tile_image.get_height()

        # Tile the surface across the width and height of the ground
        for i in range(0, width, tile_width):
            for j in range(0, height, tile_height):
                self.image.blit(tile_image, (i, j))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
