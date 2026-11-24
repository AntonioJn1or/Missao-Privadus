"""Inimigo Coco — perseguidor em linha reta (INI-02)."""

from pathlib import Path
import random

import pygame

from objects.enemies.enemy_base import EnemyBase


_WIDTH = 44
_HEIGHT = 44
_SPRITE_SCALE = 0.68
_SPRITE_FRAME_COUNT = 12
_SPRITE_ANIMATION_DURATION = 0.6
_SPRITE_ASSETS = (
    Path(__file__).resolve().parents[2] / "assets/imgs/enemies/coco1.png",
    Path(__file__).resolve().parents[2] / "assets/imgs/enemies/coco2.png",
)


class Coco(EnemyBase):
    """Inimigo Coco: persegue Privadus em linha reta e causa dano por contato.

    Máquina de estados:
    - ``idle``      : aguarda o jogador entrar no raio de perseguição.
    - ``pursuing``  : move-se diretamente em direção ao jogador.
    """

    DETECTION_RADIUS = 400  # px — raio para ativar a perseguição
    MAX_HP = 20
    SPEED = 90              # px/s
    CONTACT_DAMAGE = 10
    HURT_FLASH_DURATION = 0.15   # segundos piscando após levar dano

    _sprite_frames_by_asset = {}

    def __init__(self, x, y):
        super().__init__(
            x, y,
            max_hp=self.MAX_HP,
            speed=self.SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__hurt_flash_timer = 0.0
        sprite_asset = random.choice(_SPRITE_ASSETS)
        self.__frames = self.__load_sprite_frames(sprite_asset)
        self.__animation_frame = 0
        self.__animation_timer = 0.0
        self.__facing_left = False

    # ------------------------------------------------------------------
    # Hitbox
    # ------------------------------------------------------------------

    @property
    def _hitbox_width(self):
        return _WIDTH

    @property
    def _hitbox_height(self):
        return _HEIGHT

    # ------------------------------------------------------------------
    # Lógica de update (máquina de estados FSM)
    # ------------------------------------------------------------------

    def update(self, player_x, player_y, delta_time, obstacles=()):
        """Atualiza o estado, a animação e a posição do Coco."""
        self._update_invulnerability(delta_time)

        if self.__hurt_flash_timer > 0.0:
            self.__hurt_flash_timer = max(
                0.0, self.__hurt_flash_timer - delta_time
            )

        horizontal_delta = player_x - (self.x + _WIDTH / 2)
        if horizontal_delta != 0:
            self.__facing_left = horizontal_delta < 0

        self.__animation_timer += delta_time
        frame_duration = _SPRITE_ANIMATION_DURATION / _SPRITE_FRAME_COUNT
        while self.__animation_timer >= frame_duration:
            self.__animation_timer -= frame_duration
            self.__animation_frame = (
                self.__animation_frame + 1
            ) % _SPRITE_FRAME_COUNT

        if not self.is_alive:
            self._set_state("dead")
            return

        # Centro do jogador para medir a distância de perseguição.
        distance = (
            (player_x - self.x) ** 2 + (player_y - self.y) ** 2
        ) ** 0.5

        if self.state == "idle":
            if distance <= self.DETECTION_RADIUS:
                self._set_state("pursuing")
        elif self.state == "pursuing":
            if distance > self.DETECTION_RADIUS * 1.2:
                self._set_state("idle")
            else:
                self._move_toward(player_x, player_y, delta_time, obstacles)

    # ------------------------------------------------------------------
    # Dano e renderização
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_flash_timer = self.HURT_FLASH_DURATION
        return damaged

    def draw(self):
        """Desenha o frame atual da versão escolhida ao gerar o Coco."""
        screen = pygame.display.get_surface()
        if screen is None:
            return

        frame, flipped_frame = self.__frames[self.__animation_frame]
        image = flipped_frame if self.__facing_left else frame
        if self.__hurt_flash_timer > 0.0:
            image = image.copy()
            image.fill((255, 100, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # Mantém os pés alinhados com a hitbox usada para movimento e dano.
        screen_x = self.x + (_WIDTH - image.get_width()) / 2
        screen_y = self.y + _HEIGHT - image.get_height()
        screen.blit(image, (round(screen_x), round(screen_y)))

    @classmethod
    def __load_sprite_frames(cls, asset_path):
        cached_frames = cls._sprite_frames_by_asset.get(asset_path)
        if cached_frames is not None:
            return cached_frames

        sheet = pygame.image.load(str(asset_path))
        display_width = round(
            sheet.get_width() / _SPRITE_FRAME_COUNT * _SPRITE_SCALE
        )
        display_height = round(sheet.get_height() * _SPRITE_SCALE)
        frames = []
        for index in range(_SPRITE_FRAME_COUNT):
            left = index * sheet.get_width() // _SPRITE_FRAME_COUNT
            right = (index + 1) * sheet.get_width() // _SPRITE_FRAME_COUNT
            source_frame = sheet.subsurface(
                pygame.Rect(left, 0, right - left, sheet.get_height())
            )
            frame = pygame.transform.scale(
                source_frame,
                (display_width, display_height),
            )
            frames.append((frame, pygame.transform.flip(frame, True, False)))

        cached_frames = tuple(frames)
        cls._sprite_frames_by_asset[asset_path] = cached_frames
        return cached_frames
