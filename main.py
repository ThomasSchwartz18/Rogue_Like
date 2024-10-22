import pygame
from scripts.menu import MainMenu
from scripts.game import Game
import json

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Simple Platformer')

    main_menu = MainMenu(screen)
    choice = main_menu.display()

    if choice == 'new_game':
        game = Game(screen)
        game.play()
    elif choice == 'load_game':
        try:
            with open('savegame.json', 'r') as f:
                game_data = json.load(f)
                game = Game(screen)
                game.game_data = game_data
                game.play()
        except FileNotFoundError:
            print("No saved game found.")
            main()

if __name__ == "__main__":
    main()
