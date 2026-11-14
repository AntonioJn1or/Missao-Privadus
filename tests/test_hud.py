"""Testes unitários para a classe Hud e requisitos de UI."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from pplay.window import Window

from objects.hud import Hud
from objects.player import Player
from scenes.phase1.phase import Phase1


class TestHud(unittest.TestCase):
    """Testa os requisitos UI-01, UI-02 e UI-03 na classe Hud."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.window = Window(1280, 700)

    def setUp(self):
        self.player = Player(100, 100, max_hp=100)
        self.hud = Hud(
            self.window,
            self.player,
            stage_name="1 - Banheiro da UFF",
            objective="Encontrar o gnomo",
        )

    def test_initial_values(self):
        self.assertEqual(self.hud.stage_name, "1 - Banheiro da UFF")
        self.assertEqual(self.hud.objective, "Encontrar o gnomo")
        self.assertEqual(self.hud.survival_time, 0.0)
        self.assertEqual(self.hud.formatted_survival_time, "00:00")

    def test_timer_updates_and_formats(self):
        self.hud.update(15.0)
        self.assertEqual(self.hud.formatted_survival_time, "00:15")

        self.hud.update(50.0)  # Total: 65s
        self.assertEqual(self.hud.formatted_survival_time, "01:05")

        self.hud.update(535.0)  # Total: 600s = 10m
        self.assertEqual(self.hud.formatted_survival_time, "10:00")

    def test_reset_timer(self):
        self.hud.update(30.0)
        self.assertEqual(self.hud.survival_time, 30.0)

        self.hud.reset_timer()
        self.assertEqual(self.hud.survival_time, 0.0)
        self.assertEqual(self.hud.formatted_survival_time, "00:00")

    def test_set_stage_name_and_objective(self):
        self.hud.set_stage_name("2 - Sistema de Esgoto")
        self.assertEqual(self.hud.stage_name, "2 - Sistema de Esgoto")

        self.hud.set_objective("Derrotar a Ratazana")
        self.assertEqual(self.hud.objective, "Derrotar a Ratazana")

    def test_draw_with_various_health_levels(self):
        # 1. Vida cheia
        self.hud.draw()

        # 2. Vida moderada (50%)
        self.player.take_damage(50)
        self.hud.draw()

        # 3. Vida baixa (< 25%)
        # Força expirar invulnerabilidade para poder levar mais dano
        self.player.update(0, 0, delta_time=2.0)
        self.player.take_damage(35)  # 15 HP restante
        self.assertEqual(self.player.hp, 15)
        self.hud.draw()

        # 4. Morte (0 HP)
        self.player.update(0, 0, delta_time=2.0)
        self.player.take_damage(15)  # 0 HP
        self.assertEqual(self.player.hp, 0)
        self.hud.draw()

    def test_phase1_hud_integration(self):
        phase = Phase1(self.window, 1280, 700)
        self.assertIsNotNone(phase.hud)
        self.assertEqual(phase.hud.stage_name, Phase1.STAGE_NAME)
        self.assertEqual(phase.hud.objective, Phase1.OBJECTIVE)

        # Atualização e desenho da fase executam o HUD sem erro
        phase.update(0.1)
        self.assertAlmostEqual(phase.hud.survival_time, 0.1)
        phase.draw()


if __name__ == "__main__":
    unittest.main()
