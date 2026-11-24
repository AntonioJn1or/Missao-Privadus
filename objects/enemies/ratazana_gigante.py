"""Chefe do Reservatório: imóvel, lança poças e anima o arremesso."""

import math
from pathlib import Path

import pygame

from objects.enemies.enemy_base import EnemyBase


class RatazanaGigante(EnemyBase):
    MAX_HP = 180
    CONTACT_DAMAGE = 0
    POISON_RADIUS = 54
    POISON_DURATION = 8.0
    AURA_DAMAGE = 6
    AURA_TICK_INTERVAL = 0.75
    POOL_INTERVAL = 2.4
    FRAME_COUNT = 8
    THROW_ANIMATION_DURATION = 0.8
    SPRITE_SIZE = (144, 150)

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            max_hp=self.MAX_HP,
            speed=0,
            contact_damage=self.CONTACT_DAMAGE,
            invulnerability_duration=0.25,
        )
        self.__pool_timer = 0.0
        self.__aura_timer = 0.0
        self.__poison_pools = []
        self.__hurt_timer = 0.0
        self.__animation_timer = 0.0
        self.__animation_active = False
        self.__frames = self.__load_frames()

    @property
    def _hitbox_width(self):
        return 100

    @property
    def _hitbox_height(self):
        return 100

    @classmethod
    def __load_frames(cls):
        sprite_path = Path(__file__).resolve().parents[2] / "assets/imgs/enemies/rei_rato.png"
        sheet = pygame.image.load(str(sprite_path)).convert_alpha()
        frames = []
        for index in range(cls.FRAME_COUNT):
            left = index * sheet.get_width() // cls.FRAME_COUNT
            right = (index + 1) * sheet.get_width() // cls.FRAME_COUNT
            frame = sheet.subsurface((left, 0, right - left, sheet.get_height()))
            frames.append(pygame.transform.smoothscale(frame, cls.SPRITE_SIZE))
        return frames

    def update(self, player_x, player_y, delta_time, obstacles=()):
        self._update_invulnerability(delta_time)
        self.__hurt_timer = max(0.0, self.__hurt_timer - delta_time)
        self.__aura_timer += delta_time

        if not self.is_alive:
            self._set_state("dead")
            return

        self._set_state("throwing" if self.__animation_active else "idle")
        if self.__animation_active:
            self.__animation_timer += delta_time
            if self.__animation_timer >= self.THROW_ANIMATION_DURATION:
                self.__animation_timer = 0.0
                self.__animation_active = False

        self.__pool_timer += delta_time
        if self.__pool_timer >= self.POOL_INTERVAL:
            self.__pool_timer -= self.POOL_INTERVAL
            self.__poison_pools.append(
                [player_x, player_y, self.POISON_DURATION]
            )
            self.__animation_timer = 0.0
            self.__animation_active = True

        active_pools = []
        for pool in self.__poison_pools:
            pool[2] -= delta_time
            if pool[2] > 0:
                active_pools.append(pool)
        self.__poison_pools = active_pools

    def check_aura_damage(self, player_center_x, player_center_y):
        if self.__aura_timer < self.AURA_TICK_INTERVAL:
            return False
        self.__aura_timer = 0.0
        for pool_x, pool_y, _ in self.__poison_pools:
            if math.hypot(player_center_x - pool_x, player_center_y - pool_y) <= self.POISON_RADIUS:
                return True
        return False

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_timer = 0.16
        return damaged

    def draw(self):
        screen = pygame.display.get_surface()
        if screen is None:
            return

        for pool_x, pool_y, remaining in self.__poison_pools:
            alpha = round(80 * min(1.0, remaining / 1.5))
            puddle = pygame.Surface(
                (self.POISON_RADIUS * 2, self.POISON_RADIUS * 2), pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                puddle,
                (95, 210, 48, alpha),
                (2, 10, self.POISON_RADIUS * 2 - 4, self.POISON_RADIUS * 2 - 18),
            )
            screen.blit(
                puddle,
                (round(pool_x - self.POISON_RADIUS), round(pool_y - self.POISON_RADIUS)),
            )

        frame_index = 0
        if self.__animation_active:
            progress = min(0.999, self.__animation_timer / self.THROW_ANIMATION_DURATION)
            frame_index = min(self.FRAME_COUNT - 1, int(progress * self.FRAME_COUNT))

        sprite = self.__frames[frame_index]
        if self.__hurt_timer:
            sprite = sprite.copy()
            sprite.fill((90, 25, 25, 0), special_flags=pygame.BLEND_RGBA_ADD)
        sprite_x = round(self.x + (self._hitbox_width - sprite.get_width()) / 2)
        sprite_y = round(self.y + (self._hitbox_height - sprite.get_height()) / 2)
        screen.blit(sprite, (sprite_x, sprite_y))

        bar_w, bar_h = 112, 8
        bar_x = round(self.x + (self._hitbox_width - bar_w) / 2)
        bar_y = round(self.y - 35)
        pygame.draw.rect(screen, (24, 20, 19), (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
        pygame.draw.rect(
            screen,
            (210, 58, 47),
            (bar_x, bar_y, max(0, round(bar_w * self.hp / self.max_hp)), bar_h),
        )
