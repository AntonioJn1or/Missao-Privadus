"""Testes para o botão da porta na fase 1 e transição para o próximo cômodo (Fase 2)."""

import os
import unittest
from unittest.mock import patch

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from pplay.window import Window

from objects.yellow_arrow import YellowArrow
from scenes.phase1.phase import Phase1
from scenes.phase2.phase import Phase2


class TestDoorAndPhase2(unittest.TestCase):
    """Valida a detecção da porta, o popup de interação e a transição de cômodos."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.window = Window(1280, 700)

    def test_door_popup_appears_near_door_phase1(self):
        phase1 = Phase1(self.window, 1280, 700)

        # Afastado da porta no início
        self.assertFalse(phase1._Phase__interaction_popup.is_visible)

        # Teleporta para perto da porta à direita (x=1030, y=560)
        phase1.player.teleport_to(1030, 560)
        phase1.update(0.016)

        # O popup interativo deve ficar visível acima da porta
        self.assertTrue(phase1._Phase__interaction_popup.is_visible)
        interactable = phase1._find_nearest_interactable()
        self.assertIsNotNone(interactable)
        self.assertEqual(interactable.tag, "door")

    def test_press_e_near_door_transitions_to_phase2(self):
        phase1 = Phase1(self.window, 1280, 700)
        phase1.player.teleport_to(1030, 560)
        phase1.update(0.016)

        # Simula pressionar a tecla E
        with patch.object(self.window.keyboard, "key_pressed", side_effect=lambda k: k == "E"):
            phase1.process_input()

        phase1.update(0.016)
        self.assertEqual(phase1.consume_transition_request(), "phase2")

    def test_mouse_click_on_popup_transitions_to_phase2(self):
        phase1 = Phase1(self.window, 1280, 700)
        phase1.player.teleport_to(1030, 560)
        phase1.update(0.016)
        self.assertTrue(phase1._Phase__interaction_popup.is_visible)

        popup_sprite = phase1._Phase__interaction_popup._InteractionPopup__sprite
        click_pos = (popup_sprite.x + 10, popup_sprite.y + 10)

        with patch.object(self.window.mouse, "get_position", return_value=click_pos), \
             patch.object(self.window.mouse, "is_button_pressed", return_value=True):
            phase1.process_input()

        phase1.update(0.016)
        self.assertEqual(phase1.consume_transition_request(), "phase2")

    def test_phase2_room_structure(self):
        phase2 = Phase2(self.window, 1280, 700)

        # Jogador surge no lado esquerdo vindo da porta
        self.assertEqual(phase2.player.x, 140)
        self.assertEqual(phase2.player.y, 380)

        # Informações da run no HUD
        self.assertEqual(phase2.hud.stage_name, Phase2.STAGE_NAME)
        self.assertEqual(phase2.hud.objective, Phase2.OBJECTIVE)

        # Seta amarela ativa apontando para o painel de energia
        self.assertTrue(phase2.yellow_arrow.is_visible)
        self.assertIsNotNone(phase2.yellow_arrow.target)

        # Interação com o painel elétrico atualiza o objetivo
        phase2.player.teleport_to(610, 240)
        phase2.update(0.016)

        with patch.object(self.window.keyboard, "key_pressed", side_effect=lambda k: k == "E"):
            phase2.process_input()
        phase2.update(0.016)

        self.assertIn("Geradores religados", phase2.hud.objective)

    def test_yellow_arrow_mechanics(self):
        arrow = YellowArrow()
        self.assertFalse(arrow.is_visible)

        arrow.set_target(500, 300)
        arrow.update(player_center_x=100, player_center_y=300, delta_time=0.016)
        self.assertTrue(arrow.is_visible)
        self.assertEqual(arrow.target, (500.0, 300.0))

        # Quando muito perto do alvo, oculta suavemente
        arrow.update(player_center_x=495, player_center_y=300, delta_time=0.016)
        self.assertFalse(arrow.is_visible)


if __name__ == "__main__":
    unittest.main()
