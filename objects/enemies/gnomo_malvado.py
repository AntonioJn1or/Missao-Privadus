"""Chefe final da campanha com escudo, bullet hell e minions."""

import math
from pathlib import Path

import pygame

from objects.enemies.coco import Coco
from objects.enemies.enemy_base import EnemyBase
from objects.magic_projectile import MagicProjectile


class GnomoMalvado(EnemyBase):
    MAX_HP = 160
    SPEED = 25
    CONTACT_DAMAGE = 18
    ENRAGE_RATIO = 0.5
    FRAME_COUNT = 8
    SPRITE_SIZE = (148, 156)
    ATTACK_ANIMATION_DURATION = 0.88
    SHIELDED_ATTACK_INTERVAL = 1.7
    ATTACK_INTERVAL = 1.7
    ENRAGED_ATTACK_INTERVAL = 1.6

    def __init__(self, x, y, window_width):
        super().__init__(
            x,
            y,
            max_hp=self.MAX_HP,
            speed=self.SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__window_width = window_width
        self.__shielded = True
        self.__attack_timer = 0.8
        self.__stun_cycle_timer = 0.0
        self.__stun_timer = 0.0
        self.__minion_timer = 0.0
        self.__pending_projectiles = []
        self.__pending_minions = []
        self.__hurt_timer = 0.0
        self.__spiral_angle = 0.0
        self.__active = False
        self.__animation_timer = 0.0
        self.__animation_active = False
        self.__frames = self.__load_frames()

    @property
    def _hitbox_width(self):
        return 88

    @property
    def _hitbox_height(self):
        return 100

    @classmethod
    def __load_frames(cls):
        sprite_path = Path(__file__).resolve().parents[2] / "assets/imgs/enemies/gnomo.png"
        sheet = pygame.image.load(str(sprite_path)).convert_alpha()
        frames = []
        for index in range(cls.FRAME_COUNT):
            left = index * sheet.get_width() // cls.FRAME_COUNT
            right = (index + 1) * sheet.get_width() // cls.FRAME_COUNT
            frame = sheet.subsurface((left, 0, right - left, sheet.get_height()))
            frames.append(pygame.transform.smoothscale(frame, cls.SPRITE_SIZE))
        return frames

    def activate(self):
        """Inicia o duelo quando Privadus alcança o círculo ritualístico."""
        self.__active = True

    @property
    def is_shielded(self):
        return self.__shielded

    @property
    def is_enraged(self):
        return self.hp / self.max_hp <= self.ENRAGE_RATIO

    @property
    def is_stunned(self):
        return self.__stun_timer > 0.0

    def remove_shield(self):
        self.__shielded = False
        self.__stun_cycle_timer = 0.0

    def pop_pending_projectiles(self):
        pending = self.__pending_projectiles
        self.__pending_projectiles = []
        return pending

    def pop_pending_minions(self):
        pending = self.__pending_minions
        self.__pending_minions = []
        return pending

    def update(self, player_x, player_y, delta_time, obstacles=()):
        self._update_invulnerability(delta_time)
        self.__hurt_timer = max(0.0, self.__hurt_timer - delta_time)
        if not self.is_alive:
            self._set_state("dead")
            return
        if not self.__active:
            self._set_state("waiting")
            return

        if self.__animation_active:
            self.__animation_timer += delta_time
            if self.__animation_timer >= self.ATTACK_ANIMATION_DURATION:
                self.__animation_timer = 0.0
                self.__animation_active = False

        if self.__shielded:
            self._set_state("shielded")
            self.__attack_timer += delta_time
            if self.__attack_timer >= self.SHIELDED_ATTACK_INTERVAL:
                self.__attack_timer = 0.0
                self.__fire_spiral()
            return

        self.__stun_timer = max(0.0, self.__stun_timer - delta_time)
        self.__stun_cycle_timer += delta_time
        if self.__stun_cycle_timer >= 4.0 and self.__stun_timer <= 0.0:
            self.__stun_timer = 0.9
            self.__stun_cycle_timer = 0.0

        self.__attack_timer += delta_time
        interval = self.ENRAGED_ATTACK_INTERVAL if self.is_enraged else self.ATTACK_INTERVAL
        if self.__attack_timer >= interval:
            self.__attack_timer = 0.0
            if self.is_enraged:
                self.__fire_cross_burst(player_x, player_y)
            else:
                self.__fire_spiral()

        if self.is_enraged:
            self.__minion_timer += delta_time
            if self.__minion_timer >= 4.5:
                self.__minion_timer = 0.0
                self.__pending_minions.extend(
                    [Coco(self.x - 45, self.y + 20), Coco(self.x + 60, self.y + 20)]
                )

        if self.is_stunned:
            self._set_state("stunned")
        else:
            self._set_state("attacking")

    def __fire_spiral(self):
        self.__start_attack_animation()
        center_x = self.x + self._hitbox_width / 2
        center_y = self.y + self._hitbox_height / 2
        for index in range(8):
            angle = self.__spiral_angle + index * math.tau / 8
            self.__pending_projectiles.append(
                MagicProjectile(
                    center_x,
                    center_y,
                    math.cos(angle),
                    math.sin(angle),
                    speed=170,
                )
            )
        self.__spiral_angle = (self.__spiral_angle + math.pi / 8) % math.tau

    def __fire_cross_burst(self, player_x, player_y):
        self.__start_attack_animation()
        center_x = self.x + self._hitbox_width / 2
        center_y = self.y + self._hitbox_height / 2
        dx = player_x - center_x
        dy = player_y - center_y
        base_angle = math.atan2(dy, dx)
        for spread in (-0.35, 0.0, 0.35):
            angle = base_angle + spread
            self.__pending_projectiles.append(
                MagicProjectile(
                    center_x,
                    center_y,
                    math.cos(angle),
                    math.sin(angle),
                    speed=210,
                    damage=11,
                )
            )
        for index in range(4):
            angle = self.__spiral_angle + index * math.pi / 2
            self.__pending_projectiles.append(
                MagicProjectile(
                    center_x,
                    center_y,
                    math.cos(angle),
                    math.sin(angle),
                    speed=190,
                )
            )
        self.__spiral_angle = (self.__spiral_angle + math.pi / 6) % math.tau

    def __start_attack_animation(self):
        self.__animation_timer = 0.0
        self.__animation_active = True

    def take_damage(self, amount):
        if self.__shielded:
            return False
        if self.hp / self.max_hp <= self.ENRAGE_RATIO and not self.is_stunned:
            return False
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_timer = 0.18
        return damaged

    def draw(self):
        screen = pygame.display.get_surface()
        if screen is None:
            return

        center_x = round(self.x + self._hitbox_width / 2)
        center_y = round(self.y + self._hitbox_height / 2)
        if self.__shielded:
            pygame.draw.circle(screen, (100, 55, 183), (center_x, center_y), 83, 4)
        elif self.is_stunned:
            pygame.draw.circle(screen, (255, 220, 86), (center_x, center_y), 80, 3)

        frame_index = 0
        if self.__animation_active and not self.is_stunned:
            progress = min(0.999, self.__animation_timer / self.ATTACK_ANIMATION_DURATION)
            frame_index = min(self.FRAME_COUNT - 1, int(progress * self.FRAME_COUNT))
        sprite = self.__frames[frame_index]
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

        bar_w, bar_h = 108, 9
        bar_x = center_x - bar_w // 2
        bar_y = round(self.y + (self._hitbox_height - self.SPRITE_SIZE[1]) / 2 - 17)
        pygame.draw.rect(screen, (24, 18, 32), (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
        hp_color = (216, 53, 85) if self.is_enraged else (177, 87, 230)
        pygame.draw.rect(
            screen,
            hp_color,
            (bar_x, bar_y, max(0, round(bar_w * self.hp / self.max_hp)), bar_h),
        )
