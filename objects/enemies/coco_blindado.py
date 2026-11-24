"""Variação resistente do Coco, protegida por uma camada de lodo."""

import pygame

from objects.enemies.coco import Coco


class CocoBlindado(Coco):
    MAX_HP = 45
    SPEED = 70
    CONTACT_DAMAGE = 15

    def draw(self):
        super().draw()
        screen = pygame.display.get_surface()
        if screen is not None and self.is_alive:
            x, y, width, height = self.bounds
            shield_rect = pygame.Rect(
                round(x - 5), round(y - 5), round(width + 10), round(height + 10)
            )
            pygame.draw.ellipse(screen, (91, 174, 142), shield_rect, 3)
