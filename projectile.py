import pygame

class Projectile:
    def __init__(self, x, y, direction, speed=35):  # Add speed as a parameter with a default value
        self.image = pygame.image.load('../assets/images/PNG/projectiles_and_effects/arrow/arrow_.png')
        # Flip the image if the direction is left
        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)  # Flip horizontally
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed  # Use the speed value passed in
        self.direction = direction  # Direction the projectile is flying (1 for right, -1 for left)

    def update(self):
        # Move the arrow in the direction it's facing
        self.rect.x += self.speed * self.direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
