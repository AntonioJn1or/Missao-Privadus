"""Hitbox temporária do ataque da Espada de Desentupidor (BLD-05 / CTL-03)."""

import pygame


_DEBUG_COLOR = (255, 165, 0, 120)   # laranja semitransparente (apenas debug)
_SLASH_COLOR = (220, 220, 255, 160)  # branco-azulado semitransparente

# Tamanho da hitbox em pixels (relativo ao sprite 90×105)
_HIT_WIDTH = 60
_HIT_HEIGHT = 60

# Offset da hitbox a partir do centro do jogador por direção
_DIRECTION_OFFSETS = {
    "right":      ( 60,  10),
    "left":       (-60,  10),
    "up":         (  0, -55),
    "down":       (  0,  60),
    "up_right":   ( 50, -40),
    "up_left":    (-50, -40),
    "down_right": ( 50,  40),
    "down_left":  (-50,  40),
}


class AttackHitbox:
    """Hitbox retangular criada durante o ataque da espada.

    Dura ``DURATION`` segundos e verifica colisões com inimigos.
    Visualmente exibida como um flash semitransparente.
    """

    DURATION = 0.15     # segundos de vida ativa
    COOLDOWN = 0.4      # segundos antes de poder atacar novamente
    DAMAGE = 25         # dano infligido por acerto

    def __init__(self):
        self.__active_timer = 0.0
        self.__cooldown_timer = 0.0
        self.__x = 0
        self.__y = 0
        self.__surface = pygame.Surface(
            (_HIT_WIDTH, _HIT_HEIGHT), pygame.SRCALPHA
        )
        self.__surface.fill(_SLASH_COLOR)

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
        offset = _DIRECTION_OFFSETS.get(facing_direction, (60, 0))

        self.__x = center_x + offset[0] - _HIT_WIDTH / 2
        self.__y = center_y + offset[1] - _HIT_HEIGHT / 2
        self.__active_timer = self.DURATION
        self.__cooldown_timer = self.DURATION + self.COOLDOWN
        return True

    def update(self, delta_time):
        """Avança os timers de duração e cooldown."""
        if self.__active_timer > 0.0:
            self.__active_timer = max(0.0, self.__active_timer - delta_time)

        if self.__cooldown_timer > 0.0:
            self.__cooldown_timer = max(0.0, self.__cooldown_timer - delta_time)

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
        """Renderiza o flash visual da hitbox enquanto ativa."""
        if not self.is_active:
            return
        screen.blit(self.__surface, (int(self.__x), int(self.__y)))
