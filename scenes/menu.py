"""Menu inicial de Missão Privada."""

import pygame

from scenes.scene import Scene


class Menu(Scene):
    """Exibe a instrução inicial e inicia a primeira fase com Espaço."""

    INSTRUCTION = "Clique espaço para dar descarga"
    INSTRUCTION_FONT_SIZE = 32

    def process_input(self):
        if self.window.keyboard.key_pressed("SPACE"):
            self._request_transition("phase1")

    def draw(self):
        super().draw()

        font = pygame.font.SysFont(
            "Arial",
            self.INSTRUCTION_FONT_SIZE,
            bold=True,
        )
        text_width, text_height = font.size(self.INSTRUCTION)
        x = (self.window.width - text_width) // 2
        y = (self.window.height - text_height) // 2
        self.window.draw_text(
            self.INSTRUCTION,
            x,
            y,
            size=self.INSTRUCTION_FONT_SIZE,
            color=(255, 255, 255),
            font_name="Arial",
            bold=True,
        )
