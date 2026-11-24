"""Chefe da Fase 2: Rei Coco — invocador de minions e fases de ataque (CHE-01 / CHE-02)."""

from pathlib import Path

import pygame

from objects.enemies.coco import Coco
from objects.enemies.enemy_base import EnemyBase


_SPRITE_ASSET = Path(__file__).resolve().parents[2] / "assets/imgs/enemies/rei_coco.png"
_FRAME_COUNT = 8
_SPRITE_SIZE = (150, 160)
_FRAME_DURATION = 0.12
_WIDTH = 104
_HEIGHT = 110


class ReiCoco(EnemyBase):
    """Primeiro tenente do Gnomo: Chefe das Galerias de Manutenção.

    Características:
    - HP alto (90).
    - Fases de combate acionadas em limiares de HP (70% e 35%) — CHE-01.
    - Em cada limiar, invoca minions Coco via spawn_minions() — CHE-02.
    - Na última fase (HP < 35%), torna-se enfurecido aumentando a velocidade.
    """

    MAX_HP = 90
    BASE_SPEED = 75
    ENRAGED_SPEED = 110
    CONTACT_DAMAGE = 15

    THRESHOLD_PHASE_2 = 0.70  # 70% HP
    THRESHOLD_PHASE_3 = 0.35  # 35% HP

    def __init__(self, x, y):
        super().__init__(
            x, y,
            max_hp=self.MAX_HP,
            speed=self.BASE_SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__current_phase = 1
        self.__spawned_phase_2 = False
        self.__spawned_phase_3 = False
        self.__pending_minions = []
        self.__hurt_flash_timer = 0.0
        self.__animation_timer = 0.0
        self.__animation_frame = 0
        self.__frames = self.__load_frames()
        self.__facing_left = False

    @classmethod
    def __load_frames(cls):
        sheet = pygame.image.load(str(_SPRITE_ASSET)).convert_alpha()
        frames = []
        for index in range(_FRAME_COUNT):
            left = index * sheet.get_width() // _FRAME_COUNT
            right = (index + 1) * sheet.get_width() // _FRAME_COUNT
            frame = sheet.subsurface((left, 0, right - left, sheet.get_height()))
            frames.append(pygame.transform.smoothscale(frame, _SPRITE_SIZE))
        return tuple(frames)

    @property
    def _hitbox_width(self):
        return _WIDTH

    @property
    def _hitbox_height(self):
        return _HEIGHT

    @property
    def boss_phase(self):
        """Fase atual do combate (1, 2 ou 3)."""
        return self.__current_phase

    def spawn_minions(self):
        """Cria e retorna uma lista de instâncias de Coco (CHE-02).

        Retorna a lista de novos minions invocados que devem ser adicionados
        à fase.
        """
        minions = [
            Coco(self.x - 30, self.y + 10),
            Coco(self.x + _WIDTH + 10, self.y + 10),
        ]
        return minions

    def pop_pending_minions(self):
        """Consome minions gerados na transição de limiar para a Fase registrar."""
        minions = self.__pending_minions
        self.__pending_minions = []
        return minions

    def update(self, player_x, player_y, delta_time, obstacles=()):
        self._update_invulnerability(delta_time)

        if self.__hurt_flash_timer > 0.0:
            self.__hurt_flash_timer = max(0.0, self.__hurt_flash_timer - delta_time)

        if not self.is_alive:
            self._set_state("dead")
            return

        hp_ratio = self.hp / self.max_hp

        # Transições de fase por limiar de HP (CHE-01)
        if hp_ratio <= self.THRESHOLD_PHASE_3 and not self.__spawned_phase_3:
            self.__current_phase = 3
            self.__spawned_phase_3 = True
            # Invocação de minions e modo enfurecido
            self.__pending_minions.extend(self.spawn_minions())
        elif hp_ratio <= self.THRESHOLD_PHASE_2 and not self.__spawned_phase_2:
            self.__current_phase = 2
            self.__spawned_phase_2 = True
            self.__pending_minions.extend(self.spawn_minions())

        speed = self.ENRAGED_SPEED if self.__current_phase == 3 else self.BASE_SPEED
        # Aplica velocidade correspondente à fase
        self._set_position(self.x, self.y)
        dx = player_x - self.x
        dy = player_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dx != 0:
            self.__facing_left = dx < 0
        if dist > 0:
            step_x = (dx / dist) * speed * delta_time
            step_y = (dy / dist) * speed * delta_time
            self._set_position(self.x + step_x, self.y + step_y)
            self.__animation_timer += delta_time
            while self.__animation_timer >= _FRAME_DURATION:
                self.__animation_timer -= _FRAME_DURATION
                self.__animation_frame = (self.__animation_frame + 1) % _FRAME_COUNT
        else:
            self.__animation_frame = 0
            self.__animation_timer = 0.0

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_flash_timer = 0.15
        return damaged

    def draw(self):
        screen = pygame.display.get_surface()
        if screen is None:
            return

        sprite = self.__frames[self.__animation_frame]
        if self.__facing_left:
            sprite = pygame.transform.flip(sprite, True, False)
        sprite_x = round(self.x + (_WIDTH - sprite.get_width()) / 2)
        sprite_y = round(self.y + _HEIGHT - sprite.get_height())
        if self.__hurt_flash_timer > 0:
            sprite = sprite.copy()
            sprite.fill((255, 100, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(sprite, (sprite_x, sprite_y))

        # Barra de vida do Chefe no topo quando vivo
        if self.is_alive:
            bar_w = 112
            bar_h = 9
            bar_x = round(self.x + (_WIDTH - bar_w) / 2)
            bar_y = sprite_y - 15
            pygame.draw.rect(screen, (30, 30, 30), (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
            hp_w = max(0, int(bar_w * (self.hp / self.max_hp)))
            bar_col = (220, 50, 50) if self.__current_phase == 3 else (220, 180, 40)
            pygame.draw.rect(screen, bar_col, (bar_x, bar_y, hp_w, bar_h))
