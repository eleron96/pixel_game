import sys
import pygame
import pymunk
import math
from ..menu.settings import load_settings
from .walls import add_walls
from .pixel import Pixel


settings = load_settings()
wall_thickness = settings.get("wall_thickness", 5)
elasticity = settings.get("elasticity", 1.0)
friction = settings.get("friction", 0.5)
min_speed_color = settings.get("min_speed_color", [255, 255, 255])
max_speed_color = settings.get("max_speed_color", [173, 232, 244])
attract_force = settings.get("attract_force", 1000)
pixel_size = settings.get("pixel_size", 10)


def run_game():
    pygame.init()
    screen_width, screen_height = 320, 240
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 20)

    add_walls(space, screen_width, screen_height, wall_thickness, elasticity,
              friction)

    settings = load_settings()
    initial_pixel_size = settings.get("initial_pixel_size", 16)
    pixel_split_parts = settings.get("pixel_split_parts", 4)
    font_size = settings.get("font_size", 16)

    pixels = [
        Pixel(space, screen_width // 2, screen_height // 2, initial_pixel_size,
              100, -100, pixel_split_parts)]
    attraction_force = 0
    font = pygame.font.Font(None, font_size)

    return_to_menu = False

    while not return_to_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                attraction_force = 1000
            elif event.type == pygame.MOUSEBUTTONUP:
                attraction_force = 0

        # Новый код для применения силы притяжения
        if attraction_force > 0:
            cursor_pos = pygame.mouse.get_pos()
            for pixel in pixels:
                direction_vector = pymunk.Vec2d(
                    cursor_pos[0] - pixel.body.position.x,
                    cursor_pos[1] - pixel.body.position.y)
                direction_vector = direction_vector.normalized() * attraction_force
                pixel.body.apply_force_at_local_point(direction_vector)

        screen.fill((0, 0, 0))
        space.step(1 / 40.0)  # Step the simulation forward

        cursor_pos = pygame.mouse.get_pos()
        new_pixels = []

        # В основном игровом цикле
        for pixel in pixels[:]:
            if pixel.body.position.x < 0 or pixel.body.position.x > screen_width or pixel.body.position.y < 0 or pixel.body.position.y > screen_height:
                # Удаление происходит здесь, если пиксель вне экрана.
                if pixel.body in space.bodies:
                    space.remove(pixel.body, pixel.shape)
                pixels.remove(pixel)
            else:
                d = math.sqrt((pixel.body.position.x - cursor_pos[0]) ** 2 + (
                        pixel.body.position.y - cursor_pos[1]) ** 2)
                if d <= pixel.size:
                    # Разделяем пиксель и получаем новые пиксели
                    new_pixels = pixel.split()
                    # Если размер пикселя был достаточно большой, чтобы разделиться, удаляем исходный пиксель
                    if pixel.size > 2:
                        if pixel.body in space.bodies:
                            space.remove(pixel.body, pixel.shape)
                        pixels.remove(pixel)
                    # Добавляем новые пиксели в список пикселей
                    pixels.extend(new_pixels)

        pixels.extend(new_pixels)

        pixel_count_text = font.render(f"pixels: {len(pixels)}", True,
                                       (255, 255, 255))
        screen.blit(pixel_count_text, (10, 10))
        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True,
                               (255, 255, 255))
        screen.blit(fps_text, (10, 30))

        for pixel in pixels:
            speed = math.sqrt(
                pixel.body.velocity.x ** 2 + pixel.body.velocity.y ** 2)
            pixel.draw(screen, speed)

        pygame.display.flip()
        clock.tick(120)

    return return_to_menu


if __name__ == "__main__":
    run_game()

