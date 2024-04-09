from pixel_game.menu import settings
import os

def test_load_settings():
    # Проверяем, что функция load_settings() возвращает словарь
    assert isinstance(settings.load_settings(), dict)

def test_get_default_settings():
    # Проверяем, что функция get_default_settings() возвращает словарь с настройками по умолчанию
    default_settings = settings.get_default_settings()
    assert isinstance(default_settings, dict)
    assert default_settings == settings.DEFAULT_SETTINGS

def test_save_settings():
    # Проверяем, что функция save_settings() сохраняет переданные настройки в файл
    test_settings = {"initial_pixel_size": 10, "pixel_split_parts": 3}
    settings.save_settings(test_settings)
    loaded_settings = settings.load_settings()
    assert test_settings == loaded_settings

def test_get_settings():
    # Проверяем, что функция get_settings() возвращает настройки из файла, если он существует, иначе настройки по умолчанию
    test_settings = {"initial_pixel_size": 10, "pixel_split_parts": 3}
    settings.save_settings(test_settings)
    loaded_settings = settings.get_settings()
    assert test_settings == loaded_settings

    # Удаление файла с настройками
    os.remove(settings.SETTINGS_FILE)

    # Проверяем, что функция возвращает настройки по умолчанию, если файл не существует
    default_settings = settings.get_default_settings()
    assert default_settings == settings.get_settings()
