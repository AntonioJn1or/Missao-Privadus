"""Interface de Usuário (HUD) para exibição de vida e dados da run."""

import pygame


class Hud:
    """Gerencia e renderiza o HUD sobreposto aos elementos da fase."""

    DEFAULT_STAGE_NAME = "1 - Estrutura da UFF"
    DEFAULT_OBJECTIVE = "Encontrar o gnomo"

    FONT_NAME = "Arial"
    LABEL_FONT_SIZE = 14
    VALUE_FONT_SIZE = 16

    BAR_X = 20
    BAR_Y = 38
    BAR_WIDTH = 220
    BAR_HEIGHT = 20

    COLOR_PANEL_BG = (10, 10, 10, 160)
    COLOR_BORDER = (40, 40, 40)
    COLOR_EMPTY_BAR = (50, 15, 15)
    COLOR_HIGH_HP = (46, 204, 113)
    COLOR_MED_HP = (241, 196, 15)
    COLOR_LOW_HP = (231, 76, 60)
    COLOR_TEXT = (255, 255, 255)
    COLOR_LABEL = (200, 200, 200)

    TOP_RIGHT_MARGIN = 20
    TOP_RIGHT_Y = 16
    LINE_SPACING = 24

    def __init__(
        self,
        window,
        player,
        stage_name=DEFAULT_STAGE_NAME,
        objective=DEFAULT_OBJECTIVE,
    ):
        self.__window = window
        self.__player = player
        self.__stage_name = stage_name
        self.__objective = objective
        self.__survival_time = 0.0
        self.__ammo = 0

    @property
    def ammo(self):
        """Quantidade de munição de papel higiênico."""
        return self.__ammo

    def set_ammo(self, ammo):
        """Atualiza o contador de munição de papel higiênico."""
        self.__ammo = max(0, int(ammo))

    @property
    def survival_time(self):
        """Tempo decorrido de sobrevivência na run em segundos."""
        return self.__survival_time

    @property
    def formatted_survival_time(self):
        """Retorna o tempo formatado em MM:SS."""
        minutes = int(self.__survival_time // 60)
        seconds = int(self.__survival_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def stage_name(self):
        """Nome do estágio atual exibido no HUD."""
        return self.__stage_name

    @property
    def objective(self):
        """Objetivo atual exibido no HUD."""
        return self.__objective

    def set_stage_name(self, stage_name):
        """Atualiza o nome do estágio atual."""
        self.__stage_name = str(stage_name)

    def set_objective(self, objective):
        """Atualiza o objetivo exibido no HUD."""
        self.__objective = str(objective)

    def reset_timer(self):
        """Reinicia o cronômetro de sobrevivência da run."""
        self.__survival_time = 0.0

    def update(self, delta_time):
        """Atualiza o cronômetro de sobrevivência com base em delta_time."""
        self.__survival_time += delta_time

    def draw(self):
        """Desenha a interface sobreposta: vida na esquerda e info da run na direita."""
        self.__draw_health_bar()
        self.__draw_run_info()

    def __draw_health_bar(self):
        panel_width = self.BAR_WIDTH + 110
        panel_height = 76 if self.__ammo > 0 else 54
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill(self.COLOR_PANEL_BG)
        self.__window.screen.blit(panel, (self.BAR_X - 8, self.BAR_Y - 26))

        self.__window.draw_text(
            "VIDA",
            self.BAR_X,
            self.BAR_Y - 22,
            size=self.LABEL_FONT_SIZE,
            color=self.COLOR_LABEL,
            font_name=self.FONT_NAME,
            bold=True,
        )

        border_rect = pygame.Rect(
            self.BAR_X - 2,
            self.BAR_Y - 2,
            self.BAR_WIDTH + 4,
            self.BAR_HEIGHT + 4,
        )
        pygame.draw.rect(
            self.__window.screen,
            self.COLOR_BORDER,
            border_rect,
            border_radius=3,
        )

        empty_rect = pygame.Rect(
            self.BAR_X,
            self.BAR_Y,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
        )
        pygame.draw.rect(
            self.__window.screen,
            self.COLOR_EMPTY_BAR,
            empty_rect,
            border_radius=2,
        )

        ratio = max(0.0, min(1.0, self.__player.hp / max(1, self.__player.max_hp)))
        fill_width = int(self.BAR_WIDTH * ratio)

        if ratio > 0.5:
            bar_color = self.COLOR_HIGH_HP
        elif ratio > 0.25:
            bar_color = self.COLOR_MED_HP
        else:
            bar_color = self.COLOR_LOW_HP

        if fill_width > 0:
            fill_rect = pygame.Rect(
                self.BAR_X,
                self.BAR_Y,
                fill_width,
                self.BAR_HEIGHT,
            )
            pygame.draw.rect(
                self.__window.screen,
                bar_color,
                fill_rect,
                border_radius=2,
            )

        hp_text = f"{self.__player.hp} / {self.__player.max_hp}"
        self.__window.draw_text(
            hp_text,
            self.BAR_X + self.BAR_WIDTH + 10,
            self.BAR_Y + 1,
            size=self.VALUE_FONT_SIZE,
            color=self.COLOR_TEXT,
            font_name=self.FONT_NAME,
            bold=True,
        )

        if self.__ammo > 0:
            ammo_text = f"Papel: {self.__ammo} (Botão Direito do Mouse)"
            self.__window.draw_text(
                ammo_text,
                self.BAR_X,
                self.BAR_Y + self.BAR_HEIGHT + 6,
                size=self.LABEL_FONT_SIZE,
                color=(240, 240, 180),
                font_name=self.FONT_NAME,
                bold=True,
            )

    def __draw_run_info(self):
        font = pygame.font.SysFont(self.FONT_NAME, self.VALUE_FONT_SIZE, bold=True)
        lines = [
            f"Tempo: {self.formatted_survival_time}",
            f"Estágio: {self.__stage_name}",
            f"Objetivo: {self.__objective}",
        ]

        max_text_width = max(font.size(line)[0] for line in lines)
        panel_padding_x = 12
        panel_padding_y = 10
        panel_width = max_text_width + panel_padding_x * 2
        panel_height = len(lines) * self.LINE_SPACING + panel_padding_y

        panel_x = self.__window.width - panel_width - self.TOP_RIGHT_MARGIN
        panel_y = self.TOP_RIGHT_Y - 4

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill(self.COLOR_PANEL_BG)
        self.__window.screen.blit(panel, (panel_x, panel_y))

        for index, line in enumerate(lines):
            line_y = self.TOP_RIGHT_Y + index * self.LINE_SPACING
            self.__window.draw_text(
                line,
                panel_x + panel_padding_x,
                line_y,
                size=self.VALUE_FONT_SIZE,
                color=self.COLOR_TEXT,
                font_name=self.FONT_NAME,
                bold=True,
            )
