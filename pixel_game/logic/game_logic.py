import sys
import pygame
import pymunk
import math

from ..menu.settings import load_settings

def add_walls(space, screen_width, screen_height):
    thickness = 10
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (screen_width, 0), thickness),
        pymunk.Segment(space.static_body, (0, 0), (0, screen_height), thickness),
        pymunk.Segment(space.static_body, (screen_width, 0), (screen_width, screen_height), thickness),
        pymunk.Segment(space.static_body, (0, screen_height), (screen_width, screen_height), thickness)
    ]
    for wall in walls:
        wall.elasticity = 1.0
        wall.friction = 0.5
    space.add(*walls)

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
        self.shape.elasticity = 1.0
        self.shape.friction = 0.5
        self.space.add(self.body, self.shape)

    def draw(self, screen):
        x, y = self.body.position
        pygame.draw.rect(screen, (255, 255, 255), (x, y, self.size, self.size))

    def split(self):
        if self.size <= 2:
            self.space.remove(self.body, self.shape)
            return []

        new_size = max(self.size // 2, 1)
        new_pixels = []
        base_speed = math.sqrt(self.body.velocity.x**2 + self.body.velocity.y**2) * 1.4

        for i in range(self.split_parts):
            angle = 2 * math.pi * i / self.split_parts
            new_speed_x = base_speed * math.cos(angle)
            new_speed_y = base_speed * math.sin(angle)
            new_x, new_y = self.body.position
            new_pixels.append(Pixel(self.space, new_x, new_y, new_size, new_speed_x, new_speed_y, self.split_parts))

        self.space.remove(self.body, self.shape)
        return new_pixels

def run_game():
    pygame.init()
    screen_width, screen_height = 320, 240
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 20)

    add_walls(space, screen_width, screen_height)

    settings = load_settings()
    initial_pixel_size = settings.get("initial_pixel_size", 16)
    pixel_split_parts = settings.get("pixel_split_parts", 4)  # Получаем значение pixel_split_parts из настроек

    pixels = [Pixel(space, screen_width // 2, screen_height // 2, initial_pixel_size, 100, -100, pixel_split_parts)]  # Используем полученное значение

    return_to_menu = False

    while not return_to_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True

        screen.fill((0, 0, 0))
        space.step(1/60.0)

        cursor_pos = pygame.mouse.get_pos()
        new_pixels = []

        for pixel in pixels[:]:
            d = math.sqrt((pixel.body.position.x - cursor_pos[0])**2 + (pixel.body.position.y - cursor_pos[1])**2)
            if d <= pixel.size:
                pixels.remove(pixel)
                new_pixels.extend(pixel.split())

        pixels.extend(new_pixels)

        for pixel in pixels:
            pixel.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return return_to_menu


if __name__ == "__main__":
    run_game()
