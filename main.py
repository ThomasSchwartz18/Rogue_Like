# main.py
import pygame
from scripts.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Window size
    pygame.display.set_caption("2D Platformer")

    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
