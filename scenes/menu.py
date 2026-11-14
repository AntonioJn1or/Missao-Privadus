"""Menu inicial de Missão Privada com botões clicáveis."""

from pathlib import Path

import pygame
from pplay.gameimage import GameImage

from scenes.scene import Scene


class Menu(Scene):
    """Exibe o menu com a imagem de fundo e botões 'Dar Descarga' e 'Sair'."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/menu.png"

    # Coordenadas brutas dos botões na imagem original (787x582): (x1, y1, x2, y2)
    START_BUTTON_RAW = (580, 490, 1100, 620)
    EXIT_BUTTON_RAW = (740, 650, 940, 790)

    def __init__(self, window):
        super().__init__(window)

        project_root = Path(__file__).resolve().parents[1]
        background_path = project_root / self.BACKGROUND_ASSET

        self.__background = GameImage(str(background_path))
        self.__source_width = self.__background.width
        self.__source_height = self.__background.height

        self.__background.image = pygame.transform.scale(
            self.__background.image,
            (self.window.width, self.window.height),
        )
        self.__background.width = self.window.width
        self.__background.height = self.window.height

        self.__was_left_down = False

    @property
    def start_button_rect(self):
        """Retângulo escalado da área do botão 'Dar Descarga'."""
        scale_x = self.window.width / self.__source_width
        scale_y = self.window.height / self.__source_height
        x1, y1, x2, y2 = self.START_BUTTON_RAW
        return pygame.Rect(
            round(x1 * scale_x),
            round(y1 * scale_y),
            round((x2 - x1) * scale_x),
            round((y2 - y1) * scale_y),
        )

    @property
    def exit_button_rect(self):
        """Retângulo escalado da área do botão 'Sair'."""
        scale_x = self.window.width / self.__source_width
        scale_y = self.window.height / self.__source_height
        x1, y1, x2, y2 = self.EXIT_BUTTON_RAW
        return pygame.Rect(
            round(x1 * scale_x),
            round(y1 * scale_y),
            round((x2 - x1) * scale_x),
            round((y2 - y1) * scale_y),
        )

    def process_input(self):
        """Detecta o clique do mouse nos botões 'Dar Descarga' e 'Sair'."""
        mouse = self.window.mouse
        mouse_x, mouse_y = mouse.get_position()
        is_left_down = mouse.is_button_pressed(1)

        # Detecta a borda de subida do clique (quando o botão é pressionado)
        click_occurred = is_left_down and not self.__was_left_down
        self.__was_left_down = is_left_down

        if click_occurred:
            if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                self._request_transition("phase1")
            elif self.exit_button_rect.collidepoint(mouse_x, mouse_y):
                self._request_transition("quit")

    def draw(self):
        """Desenha a imagem de fundo do menu e o destaque nos botões sob o cursor."""
        super().draw()
        self.__background.draw()

        mouse = self.window.mouse
        mouse_x, mouse_y = mouse.get_position()
        is_hovering_start = self.start_button_rect.collidepoint(mouse_x, mouse_y)
        is_hovering_exit = self.exit_button_rect.collidepoint(mouse_x, mouse_y)

        # Atualiza o cursor do mouse se houver suporte no sistema
        try:
            if is_hovering_start or is_hovering_exit:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass

        # Efeito de contorno iluminado ao passar o mouse
        if is_hovering_start:
            self.__draw_hover_highlight(self.start_button_rect, (255, 255, 255, 50))
        elif is_hovering_exit:
            self.__draw_hover_highlight(self.exit_button_rect, (255, 255, 255, 60))

    def __draw_hover_highlight(self, rect, color):
        highlight_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            highlight_surface,
            color,
            highlight_surface.get_rect(),
            width=3,
            border_radius=8,
        )
        self.window.screen.blit(highlight_surface, rect.topleft)
