import pygame
import sys
from pixel_game.menu.main_menu import Menu
from pixel_game.logic.game_logic import run_game
from pixel_game.menu.settings import settings_menu


def main():
    pygame.init()

    screen_width, screen_height = 320, 240  # Задаем размеры окна
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pixel Game")

    menu_items = ["Начать игру", "Настройки", "Выход"]
    menu = Menu(screen, menu_items, screen_width,
                screen_height)  # Передаем размеры окна в конструктор меню

    while True:
        selected_option = menu.run()

        if selected_option == 0:
            while True:  # Бесконечный цикл, чтобы мы могли продолжать открывать игру из главного меню
                if run_game():  # Если игра возвращает True, это означает, что нужно открыть главное меню снова
                    break
        elif selected_option == 1:
            settings_menu()  # Вызываем функцию настроек
        elif selected_option == 2:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
