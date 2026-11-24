"""Ratazana de esgoto com padrão de ataque hit-and-run (INI-04)."""

import math
from pathlib import Path

import pygame

from objects.enemies.enemy_base import EnemyBase


class Ratazana(EnemyBase):
    """Ronda o esgoto, prepara um bote e recua antes de atacar novamente."""

    MAX_HP = 24
    SPEED = 95
    CONTACT_DAMAGE = 12
    DETECTION_RADIUS = 430
    CHARGE_TIME = 1.0
    DASH_TIME = 0.38
    RECOVERY_TIME = 0.8
    DASH_DISTANCE = 250
    FRAME_COUNT = 5
    SPRITE_SIZE = (58, 44)

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            max_hp=self.MAX_HP,
            speed=self.SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__state_timer = 0.0
        self.__dash_target = (self.x, self.y)
        self.__facing_left = False
        self.__hurt_timer = 0.0
        self.__frames = self.__load_frames()

    @classmethod
    def __load_frames(cls):
        sprite_path = Path(__file__).resolve().parents[2] / "assets/imgs/enemies/ratazana.png"
        sheet = pygame.image.load(str(sprite_path)).convert_alpha()
        frames = []
        for index in range(cls.FRAME_COUNT):
            left = index * sheet.get_width() // cls.FRAME_COUNT
            right = (index + 1) * sheet.get_width() // cls.FRAME_COUNT
            frame = sheet.subsurface((left, 0, right - left, sheet.get_height()))
            frames.append(pygame.transform.smoothscale(frame, cls.SPRITE_SIZE))
        return frames

    @property
    def _hitbox_width(self):
        return 42

    @property
    def _hitbox_height(self):
        return 30

    def update(self, player_x, player_y, delta_time, obstacles=()):
        self._update_invulnerability(delta_time)
        self.__state_timer += delta_time
        self.__hurt_timer = max(0.0, self.__hurt_timer - delta_time)
        self.__facing_left = player_x < self.x + self._hitbox_width / 2

        if not self.is_alive:
            self._set_state("dead")
            return

        distance = math.hypot(player_x - self.x, player_y - self.y)
        if self.state in ("idle", "patrolling"):
            self._set_state("patrolling")
            if distance <= self.DETECTION_RADIUS:
                self.__state_timer = 0.0
                self._set_state("charging")
        elif self.state == "charging":
            if self.__state_timer >= self.CHARGE_TIME:
                dx = player_x - (self.x + self._hitbox_width / 2)
                dy = player_y - (self.y + self._hitbox_height / 2)
                length = max(1.0, math.hypot(dx, dy))
                self.__dash_target = (
                    self.x + dx / length * self.DASH_DISTANCE,
                    self.y + dy / length * self.DASH_DISTANCE,
                )
                self.__state_timer = 0.0
                self._set_state("dashing")
        elif self.state == "dashing":
            self._move_toward(
                self.__dash_target[0],
                self.__dash_target[1],
                delta_time * 3,
                obstacles,
            )
            arrived = math.hypot(
                self.__dash_target[0] - self.x,
                self.__dash_target[1] - self.y,
            ) <= 12
            if arrived or self.__state_timer >= self.DASH_TIME:
                self.__state_timer = 0.0
                self._set_state("recovering")
        elif self.state == "recovering" and self.__state_timer >= self.RECOVERY_TIME:
            self.__state_timer = 0.0
            self._set_state("patrolling")

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_timer = 0.15
        return damaged

    def draw(self):
        screen = pygame.display.get_surface()
        if screen is None:
            return

        if self.state == "charging":
            pygame.draw.circle(
                screen,
                (210, 154, 53),
                (round(self.x + 21), round(self.y + 15)),
                26,
                2,
            )

        frame_index = 0
        if self.state == "dashing":
            dash_progress = min(0.999, self.__state_timer / self.DASH_TIME)
            frame_index = 1 + min(3, int(dash_progress * 4))
        sprite = self.__frames[frame_index]
        if self.__facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        if self.__hurt_timer:
            sprite = sprite.copy()
            sprite.fill((90, 25, 25, 0), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(
            sprite,
            (
                round(self.x + (self._hitbox_width - sprite.get_width()) / 2),
                round(self.y + (self._hitbox_height - sprite.get_height()) / 2),
            ),
        )
