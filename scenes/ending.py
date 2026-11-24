"""Tela de encerramento da campanha."""

import pygame

from scenes.scene import Scene


class Ending(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.__title_font = pygame.font.SysFont(None, 56)
        self.__body_font = pygame.font.SysFont(None, 30)

    def process_input(self):
        keyboard = self.window.keyboard
        if keyboard.key_pressed("M"):
            self._request_transition("menu")
        elif keyboard.key_pressed("ESC"):
            self._request_transition("quit")

    def draw(self):
        super().draw()
        screen = self.window.screen
        screen.fill((20, 39, 38))
        title = self.__title_font.render("VITÓRIA!", True, (239, 214, 133))
        message = self.__body_font.render(
            "Privadus baniu o Gnomo e salvou o campus.",
            True,
            (226, 235, 221),
        )
        hint = self.__body_font.render(
            "Pressione M para voltar ao menu ou Esc para sair",
            True,
            (158, 181, 169),
        )
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 260)))
        screen.blit(message, message.get_rect(center=(screen.get_width() // 2, 340)))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, 410)))
