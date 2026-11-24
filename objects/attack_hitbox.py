"""Hitbox temporária do ataque da Espada de Desentupidor (BLD-05 / CTL-03)."""

from pathlib import Path

import pygame


# Tamanho da hitbox em pixels (relativo ao sprite 90×105)
_HIT_WIDTH = 60
_HIT_HEIGHT = 60

_EFFECT_ASSET = (
    Path(__file__).resolve().parents[1] / "assets/imgs/effects/ataque.png"
)

# Offset da hitbox a partir do centro do jogador por direção
_DIRECTION_OFFSETS = {
    "right":      ( 75,  10),
    "left":       (-75,  10),
    "up":         (  0, -70),
    "down":       (  0,  75),
    "up_right":   ( 60, -50),
    "up_left":    (-60, -50),
    "down_right": ( 60,  50),
    "down_left":  (-60,  50),
}


class AttackHitbox:
    """Hitbox retangular criada durante o ataque da espada.

    Dura ``DURATION`` segundos e verifica colisões com inimigos.
    A animação do golpe é visual e não altera a hitbox de dano.
    """

    DURATION = 0.15     # segundos de vida ativa
    COOLDOWN = 0.4      # segundos antes de poder atacar novamente
    DAMAGE = 25         # dano infligido por acerto
    EFFECT_DURATION = 0.6
    EFFECT_FRAME_COUNT = 8
    EFFECT_FRAME_DURATION = EFFECT_DURATION / EFFECT_FRAME_COUNT

    _effect_frames = None
    _effect_rotations = {}

    def __init__(self):
        self.__active_timer = 0.0
        self.__cooldown_timer = 0.0
        self.__x = 0
        self.__y = 0
        self.__effect_timer = 0.0
        self.__effect_center = (0, 0)
        self.__effect_angle = 0
        self.__load_effect_frames()

    # ------------------------------------------------------------------
    # Propriedades
    # ------------------------------------------------------------------

    @property
    def is_active(self):
        """Indica se a hitbox está ativa (dentro do DURATION)."""
        return self.__active_timer > 0.0

    @property
    def is_on_cooldown(self):
        """Indica se o ataque ainda está em recarga."""
        return self.__cooldown_timer > 0.0

    @property
    def bounds(self):
        """Tupla (x, y, width, height) da área de acerto atual."""
        return (self.__x, self.__y, _HIT_WIDTH, _HIT_HEIGHT)

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------

    def try_attack(self, player_x, player_y, player_width, player_height,
                   facing_direction):
        """Tenta iniciar um ataque posicionando a hitbox à frente do jogador.

        Retorna True se o ataque começou; False se ainda está em cooldown.
        """
        if self.is_on_cooldown:
            return False

        center_x = player_x + player_width / 2
        center_y = player_y + player_height / 2
        offset = _DIRECTION_OFFSETS.get(facing_direction, (75, 0))

        self.__x = center_x + offset[0] - _HIT_WIDTH / 2
        self.__y = center_y + offset[1] - _HIT_HEIGHT / 2
        self.__effect_center = (
            center_x + offset[0],
            center_y + offset[1],
        )
        self.__effect_angle = {
            "right": 0,
            "up_right": 45,
            "up": 90,
            "up_left": 135,
            "left": 180,
            "down_left": 225,
            "down": 270,
            "down_right": 315,
        }.get(facing_direction, 0)
        self.__active_timer = self.DURATION
        self.__cooldown_timer = self.DURATION + self.COOLDOWN
        self.__effect_timer = self.EFFECT_DURATION
        return True

    def update(self, delta_time):
        """Avança os timers de duração e cooldown."""
        if self.__active_timer > 0.0:
            self.__active_timer = max(0.0, self.__active_timer - delta_time)

        if self.__cooldown_timer > 0.0:
            self.__cooldown_timer = max(0.0, self.__cooldown_timer - delta_time)

        if self.__effect_timer > 0.0:
            self.__effect_timer = max(0.0, self.__effect_timer - delta_time)

    def check_hits(self, enemies):
        """Verifica quais inimigos estão dentro da hitbox e aplica dano.

        Retorna a lista de inimigos atingidos neste quadro.
        """
        if not self.is_active:
            return []

        hx, hy, hw, hh = self.bounds
        hit = []
        for enemy in enemies:
            if not enemy.is_alive:
                continue
            ex, ey, ew, eh = enemy.bounds
            if hx < ex + ew and hx + hw > ex and hy < ey + eh and hy + hh > ey:
                if enemy.take_damage(self.DAMAGE):
                    hit.append(enemy)
        return hit

    def draw(self, screen):
        """Renderiza a animação do golpe enquanto ela estiver em andamento."""
        if self.__effect_timer <= 0.0:
            return
        elapsed = self.EFFECT_DURATION - self.__effect_timer
        frame_index = min(
            self.EFFECT_FRAME_COUNT - 1,
            int(elapsed / self.EFFECT_FRAME_DURATION),
        )
        frame = self._get_rotated_effect_frame(frame_index, self.__effect_angle)
        frame_rect = frame.get_rect(
            center=(round(self.__effect_center[0]), round(self.__effect_center[1]))
        )
        screen.blit(frame, frame_rect)

    @classmethod
    def __load_effect_frames(cls):
        if cls._effect_frames is not None:
            return

        sheet = pygame.image.load(str(_EFFECT_ASSET))
        frames = []
        for index in range(cls.EFFECT_FRAME_COUNT):
            left = index * sheet.get_width() // cls.EFFECT_FRAME_COUNT
            right = (index + 1) * sheet.get_width() // cls.EFFECT_FRAME_COUNT
            frame = sheet.subsurface(
                pygame.Rect(left, 0, right - left, sheet.get_height())
            )
            frames.append(frame.subsurface(frame.get_bounding_rect()).copy())
        cls._effect_frames = tuple(frames)

    @classmethod
    def _get_rotated_effect_frame(cls, frame_index, angle):
        rotation_key = (frame_index, angle)
        if rotation_key not in cls._effect_rotations:
            cls._effect_rotations[rotation_key] = pygame.transform.rotate(
                cls._effect_frames[frame_index], angle
            )
        return cls._effect_rotations[rotation_key]
