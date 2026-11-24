"""Testes consolidados de jogabilidade: Player, Combate, Projéteis, HUD e Menu."""

import os
import unittest
from unittest.mock import patch

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from pplay.window import Window

from objects.attack_hitbox import AttackHitbox
from objects.dash import Dash
from objects.enemies.coco import Coco
from objects.hud import Hud
from objects.player import Player
from objects.projectile import Projectile
from scenes.menu import Menu
from scenes.phase1.phase import Phase1


class TestGameplay(unittest.TestCase):
    """Testa mecânicas essenciais do jogador, combate, armas e interface."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.window = Window(1280, 700)

    def test_player_health_and_movement(self):
        player = Player(0, 0, max_hp=100, base_speed=180)
        self.assertEqual(player.hp, 100)
        self.assertTrue(player.is_alive)

        # Dano e invulnerabilidade
        self.assertTrue(player.take_damage(30))
        self.assertEqual(player.hp, 70)
        self.assertTrue(player.is_invulnerable)
        self.assertFalse(player.take_damage(20))  # bloqueado por i-frame

        # Cura
        player.heal(15)
        self.assertEqual(player.hp, 85)

        # Morte
        player.update(0, 0, delta_time=2.0)
        player.take_damage(85)
        self.assertEqual(player.hp, 0)
        self.assertFalse(player.is_alive)

    def test_dash_mechanics(self):
        dash = Dash()
        self.assertFalse(dash.is_active)
        self.assertTrue(dash.try_start(1, 0))
        self.assertTrue(dash.is_active)
        self.assertEqual(dash.speed_multiplier, Dash.SPEED_MULTIPLIER)

        # Não inicia se já ativo ou em cooldown
        self.assertFalse(dash.try_start(0, 1))
        dash.update(Dash.DURATION + Dash.COOLDOWN + 0.01)
        self.assertFalse(dash.is_active)
        self.assertFalse(dash.is_on_cooldown)

    def test_combat_and_enemies(self):
        coco = Coco(100, 100)
        self.assertEqual(coco.state, "idle")

        # Perseguição
        coco.update(120, 100, delta_time=0.016)
        self.assertEqual(coco.state, "pursuing")

        # Espada de desentupidor
        atk = AttackHitbox()
        # Posiciona ataque em cima do coco
        self.assertTrue(atk.try_attack(coco.x - 40, coco.y - 10, 60, 60, "right"))
        hits = atk.check_hits([coco])
        self.assertIn(coco, hits)
        self.assertLess(coco.hp, Coco.MAX_HP)

    def test_projectile_and_descarga(self):
        phase = Phase1(self.window, 1280, 700)
        coco = Coco(phase.player.x + 50, phase.player.y)
        phase._add_enemy(coco)

        # Projétil
        proj = Projectile(100, 100, 200, 100, speed=500, damage=10)
        proj.update(0.1)
        self.assertAlmostEqual(proj.x, 150.0)

        # Descarga
        init_hp = coco.hp
        self.assertTrue(phase.trigger_descarga())
        self.assertLess(coco.hp, init_hp)

    def test_hud_and_menu(self):
        player = Player(0, 0)
        hud = Hud(self.window, player, "Fase Teste", "Objetivo Teste")
        hud.update(1.0)
        self.assertEqual(hud.formatted_survival_time, "00:01")

        menu = Menu(self.window)
        menu.process_input()
        self.assertIsNone(menu.consume_transition_request())


if __name__ == "__main__":
    unittest.main()
