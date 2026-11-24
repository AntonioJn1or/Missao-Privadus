"""Tela exibida quando Privadus perde toda a vida."""

import pygame

from scenes.scene import Scene


class GameOver(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.__title_font = pygame.font.SysFont(None, 82)
        self.__body_font = pygame.font.SysFont(None, 32)

    def process_input(self):
        keyboard = self.window.keyboard
        if keyboard.key_pressed("R"):
            self._request_transition("phase1")
        elif keyboard.key_pressed("M"):
            self._request_transition("menu")
        elif keyboard.key_pressed("ESC"):
            self._request_transition("quit")

    def draw(self):
        super().draw()
        screen = self.window.screen
        screen.fill((35, 15, 22))
        title = self.__title_font.render("GAME OVER", True, (235, 79, 83))
        message = self.__body_font.render(
            "Privadus foi derrotado. O esgoto continua tomado.",
            True,
            (235, 220, 211),
        )
        controls = self.__body_font.render(
            "R: tentar novamente     M: menu     Esc: sair",
            True,
            (190, 175, 170),
        )
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 245)))
        screen.blit(message, message.get_rect(center=(screen.get_width() // 2, 335)))
        screen.blit(controls, controls.get_rect(center=(screen.get_width() // 2, 420)))
