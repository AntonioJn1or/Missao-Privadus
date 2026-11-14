"""Mecânica de dash/esquiva de Privadus (CTL-06)."""


class Dash:
    """Gerencia o estado, o cooldown e a duração do dash de Privadus.

    Enquanto o dash estiver ativo, o chamador deve substituir o vetor
    de movimento pelo multiplicador retornado por ``speed_multiplier``.
    Durante o dash, Privadus recebe invulnerabilidade automática.
    """

    DURATION = 0.18          # segundos de duração do dash
    COOLDOWN = 1.0           # segundos de espera após o fim do dash
    SPEED_MULTIPLIER = 4.0   # velocidade relativa durante o dash
    INVULNERABILITY = 0.25   # i-frames concedidos ao jogador (s)

    def __init__(self):
        self.__active_timer = 0.0    # tempo restante de dash ativo
        self.__cooldown_timer = 0.0  # tempo restante de cooldown
        self.__direction = (0.0, 0.0)  # vetor normalizado da última entrada

    # ------------------------------------------------------------------
    # Propriedades públicas
    # ------------------------------------------------------------------

    @property
    def is_active(self):
        """Indica se o dash está em andamento neste instante."""
        return self.__active_timer > 0.0

    @property
    def is_on_cooldown(self):
        """Indica se o dash ainda está em recarga e não pode ser usado."""
        return self.__cooldown_timer > 0.0

    @property
    def direction(self):
        """Vetor (dx, dy) normalizado usado durante o dash atual."""
        return self.__direction

    @property
    def speed_multiplier(self):
        """Multiplicador de velocidade a aplicar enquanto o dash estiver ativo."""
        return self.SPEED_MULTIPLIER if self.is_active else 1.0

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------

    def try_start(self, direction_x, direction_y):
        """Tenta iniciar o dash na direção (dx, dy) dada.

        Retorna True se o dash começou, False se já está ativo ou em
        cooldown, ou se o vetor de direção for nulo.
        """
        if self.is_active or self.is_on_cooldown:
            return False

        length = (direction_x ** 2 + direction_y ** 2) ** 0.5
        if length == 0:
            return False

        self.__direction = (direction_x / length, direction_y / length)
        self.__active_timer = self.DURATION
        self.__cooldown_timer = self.DURATION + self.COOLDOWN
        return True

    def update(self, delta_time):
        """Avança os timers de dash e cooldown pelo tempo do quadro.

        Retorna True se o dash acabou de terminar neste quadro (útil
        para o chamador conceder i-frames ao jogador exatamente na saída).
        """
        just_ended = False
        if self.__active_timer > 0.0:
            self.__active_timer = max(0.0, self.__active_timer - delta_time)
            if self.__active_timer == 0.0:
                just_ended = True

        if self.__cooldown_timer > 0.0:
            self.__cooldown_timer = max(0.0, self.__cooldown_timer - delta_time)

        return just_ended
