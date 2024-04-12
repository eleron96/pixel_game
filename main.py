import pygame
import sys
from pixel_game.menu.main_menu import Menu
from pixel_game.logic.game_logic import run_game
from pixel_game.menu.settings import settings_menu


def main():
    pygame.init()

    screen_width, screen_height = 320, 240  # Set the window dimensions
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pixel Game")

    menu_items = ["Start Game", "Settings", "Exit"]
    menu = Menu(screen, menu_items, screen_width,
                screen_height)  # Pass the window dimensions to the menu constructor

    while True:
        selected_option = menu.run()

        if selected_option == 0:
            while True:  # Infinite loop to keep opening the game from the main menu
                if run_game():  # If the game returns True, it means the main menu needs to be opened again
                    break
        elif selected_option == 1:
            settings_menu()  # Call the settings function
        elif selected_option == 2:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
