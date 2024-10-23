import pygame

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 3

    def update(self):
        # Future: Add enemy movement and AI
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
