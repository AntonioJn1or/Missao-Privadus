"""Projétil de Papel Higiênico disparado por Privadus (BLD-06)."""

import math
from pathlib import Path
import pygame


class Projectile:
    """Representa um rolo de papel higiênico disparado em direção ao clique do mouse."""

    DEFAULT_SPEED = 450.0  # px/s
    DEFAULT_DAMAGE = 10
    DEFAULT_MAX_RANGE = 700.0  # px
    SPRITE_SIZE = 32  # px
    HITBOX_SIZE = 24  # px

    def __init__(
        self,
        start_x,
        start_y,
        target_x,
        target_y,
        speed=DEFAULT_SPEED,
        damage=DEFAULT_DAMAGE,
        max_range=DEFAULT_MAX_RANGE,
    ):
        self.__x = float(start_x)
        self.__y = float(start_y)
        self.__speed = float(speed)
        self.__damage = int(damage)
        self.__max_range = float(max_range)
        self.__distance_traveled = 0.0
        self.__is_active = True

        dx = float(target_x - start_x)
        dy = float(target_y - start_y)
        length = math.hypot(dx, dy)
        if length > 0:
            self.__dx = dx / length
            self.__dy = dy / length
        else:
            self.__dx = 1.0
            self.__dy = 0.0

        # Carrega sprite visual
        self.__sprite_image = None
        project_root = Path(__file__).resolve().parents[1]
        sprite_path = project_root / "assets/imgs/items/papel_projetil.png"
        if sprite_path.exists():
            try:
                source_image = pygame.image.load(str(sprite_path)).convert_alpha()
                self.__sprite_image = pygame.transform.scale(
                    source_image,
                    (self.SPRITE_SIZE, self.SPRITE_SIZE),
                )
            except Exception:
                self.__sprite_image = None

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def is_active(self):
        return self.__is_active

    @property
    def damage(self):
        return self.__damage

    @property
    def bounds(self):
        """Retângulo de colisão do projétil: (x, y, width, height)."""
        half = self.HITBOX_SIZE / 2
        return (
            self.__x - half,
            self.__y - half,
            self.HITBOX_SIZE,
            self.HITBOX_SIZE,
        )

    def deactivate(self):
        """Desativa o projétil manualmente."""
        self.__is_active = False

    def update(self, delta_time, obstacles=()):
        """Move o projétil e desativa caso atinja obstáculos ou o alcance máximo."""
        if not self.__is_active:
            return

        step_dist = self.__speed * delta_time
        self.__x += self.__dx * step_dist
        self.__y += self.__dy * step_dist
        self.__distance_traveled += step_dist

        if self.__distance_traveled >= self.__max_range:
            self.__is_active = False
            return

        # Checa colisão com obstáculos do cenário
        px, py, pw, ph = self.bounds
        for obs in obstacles:
            if px < obs.x + obs.width and px + pw > obs.x and py < obs.y + obs.height and py + ph > obs.y:
                self.__is_active = False
                return

    def check_hit(self, enemies):
        """Verifica se o projétil colidiu com algum inimigo ativo. Aplica dano e desativa."""
        if not self.__is_active:
            return None

        px, py, pw, ph = self.bounds
        for enemy in enemies:
            if enemy.is_alive and not enemy.is_invulnerable:
                ex, ey, ew, eh = enemy.bounds
                if px < ex + ew and px + pw > ex and py < ey + eh and py + ph > ey:
                    enemy.take_damage(self.__damage)
                    self.__is_active = False
                    return enemy
        return None

    def draw(self, screen):
        """Renderiza o projétil na tela."""
        if not self.__is_active:
            return

        if self.__sprite_image is not None:
            screen.blit(
                self.__sprite_image,
                (
                    self.__x - self.SPRITE_SIZE / 2,
                    self.__y - self.SPRITE_SIZE / 2,
                ),
            )
        else:
            # Fallback visual: pequeno círculo branco de papel
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(self.__x), int(self.__y)),
                int(self.HITBOX_SIZE / 2),
            )
            pygame.draw.circle(
                screen,
                (180, 180, 180),
                (int(self.__x), int(self.__y)),
                int(self.HITBOX_SIZE / 2),
                1,
            )
