import pymunk
import math
import pygame
from ..menu.settings import load_settings

settings = load_settings()


def calculate_color(speed):
    settings = load_settings()
    min_speed_color = settings.get("min_speed_color", [255, 255, 255])
    max_speed_color = settings.get("max_speed_color", [173, 232, 244])
    red = min(max(
        min_speed_color[0] + (max_speed_color[0] - min_speed_color[0]) * (
                    100 - speed) / 90, 0), 255)
    green = min(max(
        min_speed_color[1] + (max_speed_color[1] - min_speed_color[1]) * (
                    100 - speed) / 90, 0), 255)
    blue = min(max(
        min_speed_color[2] + (max_speed_color[2] - min_speed_color[2]) * (
                    100 - speed) / 90, 0), 255)
    return int(red), int(green), int(blue)


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
        self.shape.elasticity = settings.get("elasticity", 1.0)
        self.shape.friction = settings.get("friction", 0.5)
        self.space.add(self.body, self.shape)

    def draw(self, screen, speed):
        x, y = self.body.position
        color = calculate_color(speed)
        pygame.draw.rect(screen, pygame.Color(color[0], color[1], color[2]),
                         (x, y, self.size, self.size))

    def split(self):
        if self.size <= 2:
            # self.space.remove(self.body, self.shape)
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
        self.body.apply_force_at_local_point(
            direction.normalized() * settings.get("attract_force", 1000),
            (0, 0))
