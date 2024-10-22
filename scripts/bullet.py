import pygame

class Bullet:
    def __init__(self, x, y, direction, speed=10):
        self.rect = pygame.Rect(x, y, 10, 10)  # Bullet size is a small square (10x10)
        self.color = (255, 255, 0)  # Yellow color for the bullet
        self.direction = direction  # Direction the bullet will travel
        self.speed = speed

    def update(self):
        # Move the bullet in the given direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_off_screen(self, screen_width, screen_height):
        # Check if the bullet is outside the screen boundaries
        return not self.rect.colliderect(pygame.Rect(0, 0, screen_width, screen_height))
