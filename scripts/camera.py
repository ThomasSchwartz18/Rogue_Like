import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)  # The camera's visible area
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height
        self.camera_margin = 100  # Allow the camera to pan slightly beyond the map

    def apply(self, entity):
        # Offset the entity's position by the camera's current topleft corner
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        # Center the camera on the target (the player)
        self.camera.x = target.rect.centerx - self.width // 2
        self.camera.y = target.rect.centery - self.height // 2

        # Allow the camera to pan slightly beyond the edges of the map
        self.camera.x = max(-self.camera_margin, min(self.camera.x, self.map_width - self.width + self.camera_margin))
        self.camera.y = max(-self.camera_margin, min(self.camera.y, self.map_height - self.height + self.camera_margin))
