"""Inimigo Alimento Podre Zumbi — dano em área fétido (INI-06 / INI-07)."""

import math
import pygame

from objects.enemies.enemy_base import EnemyBase


_ZUMBI_COLOR = (70, 110, 50)       # verde-oliva lodo
_ZUMBI_EYE_COLOR = (220, 255, 120)  # amarelo-tóxico
_ZUMBI_PUPIL_COLOR = (20, 40, 10)
_ZUMBI_HURT_COLOR = (210, 80, 80)
_ZUMBI_DEAD_COLOR = (40, 60, 30)
_AURA_COLOR = (90, 160, 40, 45)     # verde semitransparente para aura fétida

_WIDTH = 46
_HEIGHT = 46


class AlimentoZumbi(EnemyBase):
    """Inimigo lento que exala uma aura tóxica contínua de dano em área.

    Atributos:
    - Movimento lento (45 px/s).
    - Raio de efeito da aura fétida (75 px), usando distância euclidiana.
    - Causa dano periódico de contaminação se o jogador permanecer no raio.
    """

    MAX_HP = 30
    SPEED = 45                  # px/s — movimento lento e pesado
    CONTACT_DAMAGE = 10
    AURA_RADIUS = 75            # px — raio de dano contínuo
    AURA_TICK_INTERVAL = 0.8    # intervalo em segundos entre pulsos de dano
    AURA_DAMAGE = 5

    def __init__(self, x, y):
        super().__init__(
            x, y,
            max_hp=self.MAX_HP,
            speed=self.SPEED,
            contact_damage=self.CONTACT_DAMAGE,
        )
        self.__aura_timer = 0.0
        self.__hurt_flash_timer = 0.0

    @property
    def _hitbox_width(self):
        return _WIDTH

    @property
    def _hitbox_height(self):
        return _HEIGHT

    @property
    def aura_radius(self):
        """Raio em pixels do efeito contínuo da aura tóxica."""
        return self.AURA_RADIUS

    def update(self, player_x, player_y, delta_time, obstacles=()):
        self._update_invulnerability(delta_time)

        if self.__hurt_flash_timer > 0.0:
            self.__hurt_flash_timer = max(0.0, self.__hurt_flash_timer - delta_time)

        if not self.is_alive:
            self._set_state("dead")
            return

        # Movimento lento e incessante em direção a Privadus
        self._move_toward(player_x, player_y, delta_time, obstacles)

        # Atualiza o timer da aura fétida
        self.__aura_timer += delta_time

    def check_aura_damage(self, player_center_x, player_center_y):
        """Verifica se o jogador está na área e aplica dano se o ciclo completou.

        Retorna True se aplicou dano de aura neste ciclo.
        """
        if not self.is_alive:
            return False

        center_x = self.x + _WIDTH / 2
        center_y = self.y + _HEIGHT / 2
        # Distância euclidiana (INI-07)
        dist = math.hypot(player_center_x - center_x, player_center_y - center_y)

        if dist <= self.AURA_RADIUS and self.__aura_timer >= self.AURA_TICK_INTERVAL:
            self.__aura_timer = 0.0
            return True

        if self.__aura_timer >= self.AURA_TICK_INTERVAL:
            self.__aura_timer = 0.0

        return False

    def take_damage(self, amount):
        damaged = super().take_damage(amount)
        if damaged:
            self.__hurt_flash_timer = 0.15
        return damaged

    def draw(self):
        screen = pygame.display.get_surface()
        if screen is None:
            return

        cx = int(self.x + _WIDTH // 2)
        cy = int(self.y + _HEIGHT // 2)

        # Desenha a aura fétida semitransparente ao redor do zumbi se vivo
        if self.is_alive:
            aura_surface = pygame.Surface(
                (self.AURA_RADIUS * 2, self.AURA_RADIUS * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                aura_surface,
                _AURA_COLOR,
                (self.AURA_RADIUS, self.AURA_RADIUS),
                self.AURA_RADIUS,
            )
            screen.blit(
                aura_surface,
                (cx - self.AURA_RADIUS, cy - self.AURA_RADIUS),
            )

        color = _ZUMBI_DEAD_COLOR if not self.is_alive else (
            _ZUMBI_HURT_COLOR if self.__hurt_flash_timer > 0 else _ZUMBI_COLOR
        )
        pygame.draw.circle(screen, color, (cx, cy), _WIDTH // 2)

        if self.is_alive:
            eye_offset_x = _WIDTH // 4
            eye_offset_y = _HEIGHT // 6
            for ex in (cx - eye_offset_x, cx + eye_offset_x):
                ey = cy - eye_offset_y
                pygame.draw.circle(screen, _ZUMBI_EYE_COLOR, (ex, ey), 4)
                pygame.draw.circle(screen, _ZUMBI_PUPIL_COLOR, (ex, ey), 2)
