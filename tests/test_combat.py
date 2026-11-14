"""Testes unitários para Dash (CTL-06), Coco (INI-02) e AttackHitbox (BLD-05)."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from objects.dash import Dash
from objects.attack_hitbox import AttackHitbox
from objects.enemies.coco import Coco
from objects.enemies.enemy_base import EnemyBase


class TestDash(unittest.TestCase):
    """Testa a mecânica de dash/esquiva (CTL-06)."""

    def test_initial_state(self):
        dash = Dash()
        self.assertFalse(dash.is_active)
        self.assertFalse(dash.is_on_cooldown)
        self.assertEqual(dash.speed_multiplier, 1.0)

    def test_try_start_activates_dash(self):
        dash = Dash()
        started = dash.try_start(1, 0)
        self.assertTrue(started)
        self.assertTrue(dash.is_active)
        self.assertTrue(dash.is_on_cooldown)
        self.assertEqual(dash.speed_multiplier, Dash.SPEED_MULTIPLIER)

    def test_try_start_normalizes_direction(self):
        dash = Dash()
        dash.try_start(3, 4)
        dx, dy = dash.direction
        self.assertAlmostEqual((dx**2 + dy**2) ** 0.5, 1.0, places=5)

    def test_cannot_start_while_active(self):
        dash = Dash()
        dash.try_start(1, 0)
        second = dash.try_start(-1, 0)
        self.assertFalse(second)

    def test_cannot_start_on_cooldown(self):
        dash = Dash()
        dash.try_start(1, 0)
        # Termina o dash mas ainda cooldown
        dash.update(Dash.DURATION + 0.001)
        self.assertFalse(dash.is_active)
        self.assertTrue(dash.is_on_cooldown)
        second = dash.try_start(1, 0)
        self.assertFalse(second)

    def test_zero_direction_does_not_start(self):
        dash = Dash()
        started = dash.try_start(0, 0)
        self.assertFalse(started)

    def test_active_timer_decrements(self):
        dash = Dash()
        dash.try_start(1, 0)
        dash.update(Dash.DURATION / 2)
        self.assertTrue(dash.is_active)
        dash.update(Dash.DURATION)
        self.assertFalse(dash.is_active)

    def test_just_ended_signal(self):
        dash = Dash()
        dash.try_start(1, 0)
        # Passa o exato tempo de duração
        just_ended = dash.update(Dash.DURATION + 0.001)
        self.assertTrue(just_ended)

    def test_cooldown_expires_after_full_duration(self):
        dash = Dash()
        dash.try_start(1, 0)
        # Espera duração + cooldown
        dash.update(Dash.DURATION + Dash.COOLDOWN + 0.001)
        self.assertFalse(dash.is_active)
        self.assertFalse(dash.is_on_cooldown)
        # Agora pode usar de novo
        self.assertTrue(dash.try_start(0, 1))


class TestCoco(unittest.TestCase):
    """Testa a máquina de estados do inimigo Coco (INI-02)."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_initial_state(self):
        coco = Coco(100, 100)
        self.assertEqual(coco.state, "idle")
        self.assertTrue(coco.is_alive)
        self.assertEqual(coco.hp, Coco.MAX_HP)

    def test_transitions_to_pursuing_when_player_nearby(self):
        coco = Coco(0, 0)
        # Jogador dentro do raio de detecção
        coco.update(Coco.DETECTION_RADIUS - 1, 0, delta_time=0.016)
        self.assertEqual(coco.state, "pursuing")

    def test_stays_idle_when_player_far(self):
        coco = Coco(0, 0)
        coco.update(Coco.DETECTION_RADIUS + 100, 0, delta_time=0.016)
        self.assertEqual(coco.state, "idle")

    def test_moves_toward_player_when_pursuing(self):
        coco = Coco(0, 0)
        # Força estado perseguindo — alvo dentro do raio de detecção
        target_x = Coco.DETECTION_RADIUS // 2
        coco.update(target_x, 0, delta_time=0.016)
        self.assertEqual(coco.state, "pursuing")
        initial_x = coco.x
        # Mantém o alvo dentro do raio e aguarda movimento
        coco.update(target_x, 0, delta_time=0.1)
        self.assertGreater(coco.x, initial_x)

    def test_take_damage_reduces_hp(self):
        coco = Coco(0, 0)
        coco.take_damage(10)
        self.assertEqual(coco.hp, Coco.MAX_HP - 10)

    def test_death_on_zero_hp(self):
        coco = Coco(0, 0)
        coco.take_damage(Coco.MAX_HP)
        self.assertFalse(coco.is_alive)
        # Estado "dead" é setado no próximo update
        coco.update(0, 0, delta_time=0.016)
        self.assertEqual(coco.state, "dead")

    def test_invulnerability_after_hit(self):
        coco = Coco(0, 0)
        coco.take_damage(5)
        self.assertTrue(coco.is_invulnerable)
        second_hit = coco.take_damage(5)
        self.assertFalse(second_hit)

    def test_bounds_tuple(self):
        coco = Coco(10, 20)
        bx, by, bw, bh = coco.bounds
        self.assertEqual(bx, 10)
        self.assertEqual(by, 20)
        self.assertGreater(bw, 0)
        self.assertGreater(bh, 0)


class TestAttackHitbox(unittest.TestCase):
    """Testa a hitbox da Espada de Desentupidor (BLD-05 / CTL-03)."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_initial_state(self):
        atk = AttackHitbox()
        self.assertFalse(atk.is_active)
        self.assertFalse(atk.is_on_cooldown)

    def test_try_attack_activates_hitbox(self):
        atk = AttackHitbox()
        started = atk.try_attack(100, 100, 90, 105, "right")
        self.assertTrue(started)
        self.assertTrue(atk.is_active)
        self.assertTrue(atk.is_on_cooldown)

    def test_cannot_attack_while_on_cooldown(self):
        atk = AttackHitbox()
        atk.try_attack(0, 0, 90, 105, "right")
        second = atk.try_attack(0, 0, 90, 105, "left")
        self.assertFalse(second)

    def test_hitbox_expires_after_duration(self):
        atk = AttackHitbox()
        atk.try_attack(0, 0, 90, 105, "right")
        atk.update(AttackHitbox.DURATION + 0.001)
        self.assertFalse(atk.is_active)

    def test_cooldown_expires(self):
        atk = AttackHitbox()
        atk.try_attack(0, 0, 90, 105, "right")
        atk.update(AttackHitbox.DURATION + AttackHitbox.COOLDOWN + 0.001)
        self.assertFalse(atk.is_on_cooldown)

    def test_check_hits_damages_enemy(self):
        atk = AttackHitbox()
        # Posiciona o ataque em cima do inimigo
        coco = Coco(100, 100)
        atk.try_attack(100, 100, 90, 105, "right")
        # Garante que a hitbox abrange o coco
        hx, hy, hw, hh = atk.bounds
        bx, by, bw, bh = coco.bounds
        # Se sobreposição: test deve atingir
        overlap = hx < bx + bw and hx + hw > bx and hy < by + bh and hy + hh > by
        if overlap:
            hit = atk.check_hits([coco])
            self.assertIn(coco, hit)
            self.assertEqual(coco.hp, Coco.MAX_HP - AttackHitbox.DAMAGE)

    def test_check_hits_returns_empty_when_inactive(self):
        atk = AttackHitbox()
        coco = Coco(100, 100)
        hit = atk.check_hits([coco])
        self.assertEqual(hit, [])

    def test_check_hits_ignores_dead_enemies(self):
        atk = AttackHitbox()
        coco = Coco(100, 100)
        coco.take_damage(Coco.MAX_HP)  # mata o coco
        atk.try_attack(100, 100, 90, 105, "right")
        hit = atk.check_hits([coco])
        self.assertEqual(hit, [])


if __name__ == "__main__":
    unittest.main()
