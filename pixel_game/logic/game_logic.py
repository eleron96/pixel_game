import sys
import pygame
import pymunk
import math
from ..menu.settings import load_settings
import asyncio
from .walls import add_walls



settings = load_settings()
wall_thickness = settings.get("wall_thickness", 5)
elasticity = settings.get("elasticity", 1.0)
friction = settings.get("friction", 0.5)
min_speed_color = settings.get("min_speed_color", [255, 255, 255])
max_speed_color = settings.get("max_speed_color", [173, 232, 244])
attract_force = settings.get("attract_force", 1000)
font_size = settings.get("font_size", 16)
pixel_size = settings.get("pixel_size", 10)



def generate_angles(split_parts):
    for i in range(split_parts):
        yield 2 * math.pi * i / split_parts


class Pixel:
    def __init__(self, space, x, y, size, speed_x, speed_y, split_parts):
        self.space = space
        self.size = size
        self.split_parts = split_parts
        mass = 1
        moment = pymunk.moment_for_box(mass, (size, size))
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.body.velocity = speed_x, speed_y
        self.shape = pymunk.Poly.create_box(self.body, (size, size))
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.space.add(self.body, self.shape)

    def draw(self, screen, speed):
        x, y = self.body.position
        color = calculate_color(speed)
        pygame.draw.rect(screen, pygame.Color(color[0], color[1], color[2]), (x, y, self.size, self.size))

    def split(self):
        if self.size <= 2:
            self.space.remove(self.body, self.shape)
            return []

        new_size = max(self.size // 2, 1)
        new_pixels = []
        base_speed = math.sqrt(
            self.body.velocity.x ** 2 + self.body.velocity.y ** 2) * 1.4

        for angle in generate_angles(self.split_parts):
            new_speed_x = base_speed * math.cos(angle)
            new_speed_y = base_speed * math.sin(angle)
            new_x, new_y = self.body.position
            new_pixels.append(
                Pixel(self.space, new_x, new_y, new_size, new_speed_x,
                      new_speed_y, self.split_parts))

        return new_pixels

    def apply_force(self, pos):
        direction = pymunk.Vec2d(pos[0], pos[1]) - self.body.position
        self.body.apply_force_at_local_point(direction.normalized() * attract_force, (0, 0))


def calculate_color(speed):
    red = min(max(min_speed_color[0] + (max_speed_color[0] - min_speed_color[0]) * (100 - speed) / 90, 0), 255)
    green = min(max(min_speed_color[1] + (max_speed_color[1] - min_speed_color[1]) * (100 - speed) / 90, 0), 255)
    blue = min(max(min_speed_color[2] + (max_speed_color[2] - min_speed_color[2]) * (100 - speed) / 90, 0), 255)
    return int(red), int(green), int(blue)


async def check_pixel_position(pixel, screen_width, screen_height):
    while True:
        if (pixel.body.position.x < 0 or pixel.body.position.x > screen_width or
                pixel.body.position.y < 0 or pixel.body.position.y > screen_height):
            pixel.space.remove(pixel.body, pixel.shape)
            break
        await asyncio.sleep(1)  # Проверяем пиксели каждую секунду


def run_game():
    pygame.init()
    screen_width, screen_height = 320, 240
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 20)

    # add_walls(space, screen_width, screen_height)
    # Добавляем стены в пространство
    add_walls(space, screen_width, screen_height, wall_thickness, elasticity,
              friction)

    settings = load_settings()
    initial_pixel_size = settings.get("initial_pixel_size", 16)
    pixel_split_parts = settings.get("pixel_split_parts", 4)

    pixels = [
        Pixel(space, screen_width // 2, screen_height // 2, initial_pixel_size,
              100, -100, pixel_split_parts)]

    attraction_force = 0

    font = pygame.font.Font(None, font_size)

    # Создаем асинхронную задачу для проверки положения пикселей
    tasks = [check_pixel_position(pixel, screen_width, screen_height) for pixel in pixels]
    asyncio.ensure_future(asyncio.gather(*tasks))

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

        screen.fill((0, 0, 0))
        space.step(1 / 120.0)  # Установка FPS до 120

        cursor_pos = pygame.mouse.get_pos()
        new_pixels = []

        for pixel in pixels[:]:
            d = math.sqrt((pixel.body.position.x - cursor_pos[0]) ** 2 + (
                        pixel.body.position.y - cursor_pos[1]) ** 2)
            if d <= pixel.size:
                pixels.remove(pixel)
                new_pixels.extend(pixel.split())

            # Применяем силу притяжения к каждому пикселю
            if attraction_force > 0:
                pixel.apply_force(cursor_pos)

        pixels.extend(new_pixels)

        # Отображаем количество пикселей на экране
        pixel_count_text = font.render("pixels: {}".format(len(pixels)), True, (255, 255, 255))
        screen.blit(pixel_count_text, (10, 10))

        # Отображаем FPS
        fps_text = font.render("FPS: {:.2f}".format(clock.get_fps()), True, (255, 255, 255))
        screen.blit(fps_text, (10, 30))

        for pixel in pixels:
            speed = math.sqrt(pixel.body.velocity.x ** 2 + pixel.body.velocity.y ** 2)
            pixel.draw(screen, speed)

        pygame.display.flip()
        clock.tick(120)  # Установка FPS до 120

    return return_to_menu


if __name__ == "__main__":
    run_game()
