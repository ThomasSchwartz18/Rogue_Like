# scripts/camera.py
import pygame

class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target):
        # Only follow the target horizontally, keep the target vertically centered
        self.offset_x = target.rect.centerx - self.screen_width // 2

        # Keep the camera within the map boundaries horizontally
        self.offset_x = max(0, min(self.offset_x, self.map_width - self.screen_width))

    def apply(self, entity):
        # Apply the horizontal offset, leaving vertical positioning untouched
        return entity.rect.move(-self.offset_x, 0)
