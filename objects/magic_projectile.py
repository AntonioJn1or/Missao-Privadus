"""Projétil mágico simples usado pelos chefes da campanha."""

import math

import pygame


class MagicProjectile:
    RADIUS = 9
    SPEED = 230
    DAMAGE = 8
    MAX_LIFETIME = 5.0

    def __init__(self, x, y, direction_x, direction_y, speed=SPEED, damage=DAMAGE):
        self.x = float(x)
        self.y = float(y)
        length = max(1.0, math.hypot(direction_x, direction_y))
        self.__vx = direction_x / length * speed
        self.__vy = direction_y / length * speed
        self.damage = int(damage)
        self.__lifetime = self.MAX_LIFETIME
        self.is_active = True

    @property
    def bounds(self):
        diameter = self.RADIUS * 2
        return (self.x - self.RADIUS, self.y - self.RADIUS, diameter, diameter)

    def update(self, delta_time, window_width, window_height):
        if not self.is_active:
            return
        self.x += self.__vx * delta_time
        self.y += self.__vy * delta_time
        self.__lifetime -= delta_time
        if (
            self.__lifetime <= 0
            or self.x < -self.RADIUS
            or self.x > window_width + self.RADIUS
            or self.y < -self.RADIUS
            or self.y > window_height + self.RADIUS
        ):
            self.is_active = False

    def draw(self, screen):
        if not self.is_active:
            return
        center = (round(self.x), round(self.y))
        pygame.draw.circle(screen, (80, 31, 130), center, self.RADIUS + 4)
        pygame.draw.circle(screen, (190, 119, 255), center, self.RADIUS)
        pygame.draw.circle(screen, (248, 229, 255), center, 3)
