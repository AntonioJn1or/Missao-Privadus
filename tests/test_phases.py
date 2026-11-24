"""Testes consolidados de progressão e fases: Phase 1 e Phase 2."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from pplay.window import Window

from scenes.phase1.phase import Phase1
from scenes.phase2.phase import Phase2


class TestPhases(unittest.TestCase):
    """Testa a progressão canônica da Fase 1 e a estrutura da Fase 2."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.window = Window(1280, 700)

    def test_phase1_canonical_steps(self):
        phase1 = Phase1(self.window, 1280, 700)
        self.assertEqual(phase1.step, 1)

        # Durante o Passo 1, dispenser e outros objetos NÃO são interagíveis
        phase1.player.teleport_to(900, 220)
        phase1.update(0.016)
        self.assertIsNone(phase1._find_nearest_interactable())

        # Passo 1: Coleta do desentupidor
        phase1.player.teleport_to(180, 380)
        phase1.update(0.016)
        interactable = phase1._find_nearest_interactable()
        self.assertIsNotNone(interactable)
        self.assertEqual(interactable.tag, "plunger")
        phase1.on_interact(interactable)
        self.assertTrue(phase1.player.has_plunger)
        self.assertEqual(phase1.step, 2)

        # Passo 2: Dispenser de papel higiênico
        phase1.player.teleport_to(900, 220)
        phase1.update(0.016)
        phase1.on_interact(phase1._find_nearest_interactable())
        self.assertGreater(phase1.ammo, 0)
        self.assertEqual(phase1.step, 3)
        self.assertEqual(len(phase1.enemies), 3)

        # Passo 3 -> 4: Eliminar cocos
        for e in list(phase1.enemies):
            e.take_damage(e.max_hp)
        phase1.update(0.016)
        self.assertEqual(phase1.step, 4)

        # Passo 4 -> 5: Válvula
        phase1.player.teleport_to(980, 340)
        phase1.update(0.016)
        phase1.on_interact(phase1._find_nearest_interactable())
        self.assertEqual(phase1.step, 5)

        # Passo 5: Vaso no canto superior direito encaminha automaticamente para a fase 2
        target_x = round(650 * phase1._Phase1__scale_x)
        target_y = round(520 * phase1._Phase1__scale_y)
        phase1.player.teleport_to(target_x, target_y)
        phase1.update(0.016)
        self.assertEqual(phase1.consume_transition_request(), "phase2")

    def test_phase2_mechanics_and_objectives(self):
        phase2 = Phase2(self.window, 1280, 700)
        self.assertEqual(phase2.step, 1)

        # Sem porta de retorno para a Fase 1
        tags = [i.tag for i in phase2._Phase__interactables]
        self.assertNotIn("back_door", tags)

        # Passo 1 -> Passo 2: Elimina a patrulha inicial
        for e in list(phase2.enemies):
            e.take_damage(e.max_hp)
        phase2.update(0.016)
        self.assertEqual(phase2.step, 2)
        self.assertIn("painel de energia", phase2.hud.objective)

        # Passo 2 -> Passo 3: Religa painel elétrico
        panel = [i for i in phase2._Phase__interactables if i.tag == "electrical_panel"][0]
        phase2.on_interact(panel)
        self.assertEqual(phase2.step, 3)
        self.assertIn("bomba hidráulica", phase2.hud.objective)

        # Passo 3 -> Passo 4: Drenagem e surgimento do Rei Coco
        pump = [i for i in phase2._Phase__interactables if i.tag == "hydraulic_pump"][0]
        phase2.on_interact(pump)
        self.assertEqual(phase2.step, 4)
        self.assertIn("Rei Coco", phase2.hud.objective)

        boss = phase2._Phase2__boss
        self.assertIsNotNone(boss)
        self.assertEqual(boss.boss_phase, 1)

        # Passo 4: Causa dano no Rei Coco para disparar transição de fase e minions (CHE-01/02)
        boss.take_damage(35)
        phase2.update(0.016)
        self.assertEqual(boss.boss_phase, 2)
        # Minions foram invocados
        self.assertGreater(len(phase2.enemies), 1)

        # Derrota o Rei Coco (aguarda o fim dos i-frames)
        phase2.update(0.5)
        boss.take_damage(boss.hp)
        phase2.update(0.016)
        self.assertEqual(phase2.step, 5)
        self.assertIn("comporta", phase2.hud.objective)

        # Passo 5: Comporta do esgoto
        gate = [i for i in phase2._Phase__interactables if i.tag == "sewer_gate"][0]
        phase2.on_interact(gate)
        self.assertTrue(phase2._Phase2__gate_opened)

    def test_carry_items_across_phases(self):
        from game import Game
        game = Game()
        phase1 = Phase1(self.window, 1280, 700)
        phase1.player.equip_plunger()
        phase1.add_ammo(15)

        # Transição carregando o jogador com itens para a Fase 2 via Game
        game._Game__current_scene = phase1
        phase1._request_transition("phase2")
        game._Game__update(0.016)

        phase2 = game._Game__current_scene
        self.assertIsInstance(phase2, Phase2)
        self.assertTrue(phase2.player.has_plunger)
        self.assertTrue(phase2.player.has_item("plunger"))
        self.assertEqual(phase2.ammo, 15)
        self.assertEqual(phase2.hud.ammo, 15)


if __name__ == "__main__":
    unittest.main()
