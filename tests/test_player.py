"""Testes unitários para o estado, vida e invulnerabilidade de Player."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from objects.player import Player


class TestPlayer(unittest.TestCase):
    """Testa os requisitos JOG-02 e JOG-03 na classe Player."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_initial_state(self):
        player = Player(100, 200, max_hp=100, base_speed=180)
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.max_hp, 100)
        self.assertEqual(player.base_speed, 180)
        self.assertFalse(player.is_invulnerable)
        self.assertTrue(player.is_alive)
        self.assertEqual(player.invulnerability_timer, 0.0)
        self.assertEqual(player.state, "idle")

    def test_take_damage_reduces_hp_and_triggers_invulnerability(self):
        player = Player(0, 0, max_hp=100, invulnerability_duration=1.0)
        damaged = player.take_damage(30)

        self.assertTrue(damaged)
        self.assertEqual(player.hp, 70)
        self.assertTrue(player.is_invulnerable)
        self.assertEqual(player.invulnerability_timer, 1.0)
        self.assertEqual(player.state, "hurt")

    def test_invulnerability_blocks_further_damage(self):
        player = Player(0, 0, max_hp=100, invulnerability_duration=1.0)
        first_hit = player.take_damage(20)
        second_hit = player.take_damage(20)

        self.assertTrue(first_hit)
        self.assertFalse(second_hit)
        self.assertEqual(player.hp, 80)

    def test_invulnerability_timer_decreases_with_delta_time(self):
        player = Player(0, 0, max_hp=100, invulnerability_duration=1.0)
        player.take_damage(10)
        self.assertTrue(player.is_invulnerable)

        player.update(0, 0, delta_time=0.4)
        self.assertAlmostEqual(player.invulnerability_timer, 0.6)
        self.assertTrue(player.is_invulnerable)

        player.update(0, 0, delta_time=0.6)
        self.assertEqual(player.invulnerability_timer, 0.0)
        self.assertFalse(player.is_invulnerable)

    def test_heal_restores_hp_up_to_max(self):
        player = Player(0, 0, max_hp=100)
        player.take_damage(50)
        self.assertEqual(player.hp, 50)

        healed_amount = player.heal(30)
        self.assertEqual(healed_amount, 30)
        self.assertEqual(player.hp, 80)

        overflow_heal = player.heal(50)
        self.assertEqual(overflow_heal, 20)
        self.assertEqual(player.hp, 100)

    def test_death_when_hp_reaches_zero(self):
        player = Player(0, 0, max_hp=50)
        player.take_damage(50)

        self.assertEqual(player.hp, 0)
        self.assertFalse(player.is_alive)
        self.assertEqual(player.state, "dead")

        # Não deve receber cura nem mover quando morto
        self.assertEqual(player.heal(20), 0)
        initial_x, initial_y = player.x, player.y
        player.update(1, 0, delta_time=0.5)
        self.assertEqual(player.x, initial_x)
        self.assertEqual(player.y, initial_y)

    def test_set_base_speed(self):
        player = Player(0, 0, base_speed=180)
        player.set_base_speed(250)
        self.assertEqual(player.base_speed, 250)

        with self.assertRaises(ValueError):
            player.set_base_speed(-10)

    def test_movement_scales_with_base_speed(self):
        player = Player(0, 0, base_speed=200)
        player.update(1, 0, delta_time=0.5)
        self.assertEqual(player.x, 100)


if __name__ == "__main__":
    unittest.main()
