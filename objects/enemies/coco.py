"""Inimigo Coco — perseguidor em linha reta (INI-02)."""

import pygame

from objects.enemies.enemy_base import EnemyBase


_COCO_COLOR = (139, 90, 43)       # marrom-coco
_COCO_EYE_COLOR = (255, 255, 255)
_COCO_PUPIL_COLOR = (0, 0, 0)
_COCO_HURT_COLOR = (200, 60, 60)
_COCO_DEAD_COLOR = (80, 50, 20)

_WIDTH = 44
_HEIGHT = 44


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

    def __init__(self, x, y):
        super().__init__(
            x, y,
            max_hp=self.MAX_HP,
            speed=self.SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__hurt_flash_timer = 0.0

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
        """Atualiza o estado e a posição do Coco a cada quadro."""
        self._update_invulnerability(delta_time)

        if self.__hurt_flash_timer > 0.0:
            self.__hurt_flash_timer = max(
                0.0, self.__hurt_flash_timer - delta_time
            )

        if not self.is_alive:
            self._set_state("dead")
            return

        # Centro do jogador (aproximação) para medir distância
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
    # Override de take_damage para ativar flash visual
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_flash_timer = self.HURT_FLASH_DURATION
        return damaged

    # ------------------------------------------------------------------
    # Renderização (placeholder geométrico pixel-art)
    # ------------------------------------------------------------------

    def draw(self):
        """Desenha o Coco como um círculo escuro com olhos simples."""
        if not self.is_alive:
            color = _COCO_DEAD_COLOR
        elif self.__hurt_flash_timer > 0.0:
            color = _COCO_HURT_COLOR
        else:
            color = _COCO_COLOR

        screen = pygame.display.get_surface()
        if screen is None:
            return

        cx = int(self.x + _WIDTH // 2)
        cy = int(self.y + _HEIGHT // 2)
        radius = _WIDTH // 2

        pygame.draw.circle(screen, color, (cx, cy), radius)

        # Olhos simples
        if self.is_alive:
            eye_offset_x = radius // 3
            eye_offset_y = radius // 4
            eye_radius = max(2, radius // 5)
            pupil_radius = max(1, eye_radius // 2)

            for ex in (cx - eye_offset_x, cx + eye_offset_x):
                ey = cy - eye_offset_y
                pygame.draw.circle(screen, _COCO_EYE_COLOR, (ex, ey), eye_radius)
                pygame.draw.circle(screen, _COCO_PUPIL_COLOR, (ex, ey), pupil_radius)
