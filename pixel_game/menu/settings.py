# settings.py

import json
import pygame
import sys
from .main_menu import Menu

from pathlib import Path

# Получаем путь к директории текущего файла
current_dir = Path(__file__).parent

# Формируем абсолютный путь к файлу settings.json
settings_file_path = current_dir / '..' / 'data' / 'settings.json'

# Путь к файлу с настройками как строка
SETTINGS_FILE = str(settings_file_path.resolve())


# Загрузка настроек из файла
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        # Если файл не найден, возвращаем пустой словарь
        settings = {}
    return settings


# Сохранение настроек в файл
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


# Получение настроек, если они есть, или настроек по умолчанию
def get_settings():
    settings = load_settings()
    if not settings:
        settings = get_default_settings()
    return settings


# Значения настроек по умолчанию
DEFAULT_SETTINGS = {
    "initial_pixel_size": 16,
    "pixel_split_parts": 4,
}


# Загрузка настроек по умолчанию, если файл не найден
def get_default_settings():
    return DEFAULT_SETTINGS.copy()


# Функция меню настроек
def settings_menu():
    pygame.init()

    screen_width, screen_height = 320, 240
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Настройки")

    settings = get_settings()
    menu_items = ["Размер пикселя", "Количество частей", "Сохранить", "Назад"]
    menu = Menu(screen, menu_items, screen_width, screen_height)

    selected_option = None
    while selected_option != 3:
        selected_option = menu.run()

        if selected_option == 0:
            # Изменение размера пикселя
            settings['initial_pixel_size'] = edit_setting(screen,
                                                          "Размер пикселя",
                                                          settings[
                                                              'initial_pixel_size'])
        elif selected_option == 1:
            # Изменение количества частей при разделении пикселя
            settings['pixel_split_parts'] = edit_setting(screen,
                                                         "Количество частей",
                                                         settings[
                                                             'pixel_split_parts'])
        elif selected_option == 2:
            # Сохранение настроек
            save_settings(settings)
            return  # Возвращаемся в главное меню


def edit_setting(screen, title, default_value):
    font = pygame.font.Font(None, 32)
    value = default_value
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_UP:
                    value += 1
                elif event.key == pygame.K_DOWN:
                    value -= 1
                elif event.key == pygame.K_LEFT:
                    value -= 1
                elif event.key == pygame.K_RIGHT:
                    value += 1

        screen.fill((30, 30, 30))
        text_surface = font.render(f"{title}: {value}", True, (255, 255, 255))
        screen.blit(text_surface, (50, 50))
        pygame.display.flip()

    return value
