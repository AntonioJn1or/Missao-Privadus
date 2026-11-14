"""Classe-base abstrata para todos os inimigos de Missão Privada (INI-01)."""

import math


class EnemyBase:
    """Encapsula estado, HP, timers e movimento base de um inimigo.

    Subclasses devem implementar ``update(player_x, player_y, delta_time,
    obstacles)`` definindo a lógica da máquina de estados própria, e
    ``draw()`` para renderizar o sprite correspondente.
    """

    def __init__(self, x, y, max_hp, speed, contact_damage,
                 invulnerability_duration=0.4):
        self.__x = float(x)
        self.__y = float(y)
        self.__max_hp = max(1, int(max_hp))
        self.__hp = self.__max_hp
        self.__speed = max(0.0, float(speed))
        self.__contact_damage = max(0, int(contact_damage))
        self.__invulnerability_duration = max(0.0, float(invulnerability_duration))
        self.__invulnerability_timer = 0.0
        self.__state = "idle"

    # ------------------------------------------------------------------
    # Propriedades públicas
    # ------------------------------------------------------------------

    @property
    def x(self):
        """Coordenada X do canto superior esquerdo da sprite do inimigo."""
        return self.__x

    @property
    def y(self):
        """Coordenada Y do canto superior esquerdo da sprite do inimigo."""
        return self.__y

    @property
    def hp(self):
        """Pontos de vida atuais."""
        return self.__hp

    @property
    def max_hp(self):
        """Pontos de vida máximos."""
        return self.__max_hp

    @property
    def is_alive(self):
        """Indica se o inimigo ainda tem HP positivo."""
        return self.__hp > 0

    @property
    def is_invulnerable(self):
        """Indica se o inimigo está nos i-frames após receber dano."""
        return self.__invulnerability_timer > 0.0

    @property
    def contact_damage(self):
        """Dano causado ao jogador por contato físico a cada acerto."""
        return self.__contact_damage

    @property
    def speed(self):
        """Velocidade de movimento base em pixels por segundo."""
        return self.__speed

    @property
    def state(self):
        """Estado atual da máquina de estados."""
        return self.__state

    # ------------------------------------------------------------------
    # Operações internas acessíveis às subclasses
    # ------------------------------------------------------------------

    def _set_state(self, state):
        """Altera o estado interno (uso exclusivo de subclasses)."""
        self.__state = state

    def _set_position(self, x, y):
        """Reposiciona o inimigo (uso exclusivo de subclasses)."""
        self.__x = float(x)
        self.__y = float(y)

    def _move_toward(self, target_x, target_y, delta_time, obstacles=()):
        """Desloca o inimigo em direção ao alvo, respeitando obstáculos.

        Resolve colisões separando os eixos X e Y (wall-sliding).
        """
        dx = target_x - self.__x
        dy = target_y - self.__y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        nx = dx / dist
        ny = dy / dist
        step_x = nx * self.__speed * delta_time
        step_y = ny * self.__speed * delta_time

        self.__x = self.__try_move_axis(self.__x, step_x, "x", obstacles)
        self.__y = self.__try_move_axis(self.__y, step_y, "y", obstacles)

    def __try_move_axis(self, current, step, axis, obstacles):
        if step == 0:
            return current

        candidate = current + step
        if axis == "x":
            hitbox_rect = (candidate, self.__y,
                           self._hitbox_width, self._hitbox_height)
        else:
            hitbox_rect = (self.__x, candidate,
                           self._hitbox_width, self._hitbox_height)

        for obs in obstacles:
            if _rects_overlap(hitbox_rect, (obs.x, obs.y, obs.width, obs.height)):
                return current
        return candidate

    # ------------------------------------------------------------------
    # Dano e morte
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        """Aplica dano ao inimigo se ele não estiver invulnerável.

        Retorna True se o dano foi aplicado; False caso contrário.
        """
        if amount <= 0 or not self.is_alive or self.is_invulnerable:
            return False

        self.__hp = max(0, self.__hp - int(amount))
        self.__invulnerability_timer = self.__invulnerability_duration
        if self.__hp == 0:
            self.__state = "dead"
        return True

    def _update_invulnerability(self, delta_time):
        """Decrementa o timer de invulnerabilidade (chamar em update())."""
        if self.__invulnerability_timer > 0.0:
            self.__invulnerability_timer = max(
                0.0, self.__invulnerability_timer - delta_time
            )

    # ------------------------------------------------------------------
    # Hitbox — pode ser sobrescrita por subclasses
    # ------------------------------------------------------------------

    @property
    def _hitbox_width(self):
        """Largura da hitbox de colisão (padrão: 40 px)."""
        return 40

    @property
    def _hitbox_height(self):
        """Altura da hitbox de colisão (padrão: 40 px)."""
        return 40

    @property
    def bounds(self):
        """Tupla (x, y, width, height) da hitbox de colisão."""
        return (self.__x, self.__y, self._hitbox_width, self._hitbox_height)

    # ------------------------------------------------------------------
    # Interface pública — subclasses devem implementar
    # ------------------------------------------------------------------

    def update(self, player_x, player_y, delta_time, obstacles=()):
        """Atualiza a máquina de estados do inimigo. Deve ser sobrescrita."""
        raise NotImplementedError

    def draw(self):
        """Renderiza o inimigo na tela. Deve ser sobrescrito."""
        raise NotImplementedError


def _rects_overlap(a, b):
    """Retorna True se dois retângulos (x, y, w, h) se sobrepõem."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by
