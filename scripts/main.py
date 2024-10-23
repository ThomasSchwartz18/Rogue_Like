import pygame
from scripts.player import Player
from scripts.enemy import Enemy

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Create player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Create an enemy instance for future use
enemy = Enemy(100, 100)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player
    player.update()

    # Update enemy (future functionality)
    # enemy.update()

    # Draw everything
    screen.fill((0, 0, 0))  # Black background
    player.draw(screen)
    # enemy.draw(screen)  # Future: draw enemies

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
