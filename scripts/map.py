import pygame

class Map:
    def __init__(self, width, height, tile_size=10):
        self.width = width
        self.height = height
        self.tile_size = tile_size  # Size of each tile
        self.color1 = (0, 80, 0)  # First color (red)
        self.color2 = (0, 100, 0)  # Second color (black)

    def draw(self, screen, camera):
        # Iterate over the map and draw alternating colors to create a checkered pattern
        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                # Alternate between color1 and color2
                if (x // self.tile_size + y // self.tile_size) % 2 == 0:
                    color = self.color1
                else:
                    color = self.color2
                
                # Draw each tile relative to the camera
                rect = pygame.Rect(x - camera.camera.x, y - camera.camera.y, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)
