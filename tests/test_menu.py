"""Testes unitários para a cena do Menu e botões clicáveis."""

import os
import unittest
from unittest.mock import patch

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from pplay.window import Window

from game import Game
from scenes.menu import Menu


class TestMenu(unittest.TestCase):
    """Testa o carregamento e os botões interativos do Menu."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.window = Window(1280, 700)

    def setUp(self):
        self.menu = Menu(self.window)

    def test_button_rectangles_exist_and_scale(self):
        start_rect = self.menu.start_button_rect
        exit_rect = self.menu.exit_button_rect

        self.assertGreater(start_rect.width, 0)
        self.assertGreater(start_rect.height, 0)
        self.assertGreater(exit_rect.width, 0)
        self.assertGreater(exit_rect.height, 0)

        # O botão de início fica acima do botão de saída
        self.assertLess(start_rect.bottom, exit_rect.top)
        # Não colidem
        self.assertFalse(start_rect.colliderect(exit_rect))

    def test_start_button_click_transitions_to_phase1(self):
        start_rect = self.menu.start_button_rect
        click_x = start_rect.centerx
        click_y = start_rect.centery

        with patch.object(self.window.mouse, "get_position", return_value=(click_x, click_y)), \
             patch.object(self.window.mouse, "is_button_pressed", return_value=True):
            self.menu.process_input()

        self.assertEqual(self.menu.consume_transition_request(), "phase1")

    def test_exit_button_click_transitions_to_quit(self):
        exit_rect = self.menu.exit_button_rect
        click_x = exit_rect.centerx
        click_y = exit_rect.centery

        with patch.object(self.window.mouse, "get_position", return_value=(click_x, click_y)), \
             patch.object(self.window.mouse, "is_button_pressed", return_value=True):
            self.menu.process_input()

        self.assertEqual(self.menu.consume_transition_request(), "quit")

    def test_click_outside_buttons_does_not_transition(self):
        # Clicando no canto superior esquerdo (fora de qualquer botão)
        with patch.object(self.window.mouse, "get_position", return_value=(10, 10)), \
             patch.object(self.window.mouse, "is_button_pressed", return_value=True):
            self.menu.process_input()

        self.assertIsNone(self.menu.consume_transition_request())

    def test_space_key_does_not_trigger_transition(self):
        with patch.object(self.window.keyboard, "key_pressed", return_value=True), \
             patch.object(self.window.mouse, "is_button_pressed", return_value=False):
            self.menu.process_input()

        self.assertIsNone(self.menu.consume_transition_request())

    def test_draw_executes_without_error(self):
        self.menu.draw()

    def test_game_handles_quit_transition(self):
        game = Game()
        self.assertTrue(game._Game__is_running)

        # Simula a cena atual requisitando "quit"
        game._Game__current_scene._request_transition("quit")
        game._Game__update(0.016)

        self.assertFalse(game._Game__is_running)


if __name__ == "__main__":
    unittest.main()
