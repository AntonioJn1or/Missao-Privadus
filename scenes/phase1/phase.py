"""Primeira fase de Missão Privada."""

from pathlib import Path
import pygame
from pplay.gameimage import GameImage
from objects.enemies.coco import Coco
from scenes.phase import Phase


class Phase1(Phase):
    """Fase inicial, ambientada no banheiro da estrutura da UFF."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase1.png"
    OVERLAY_ASSET = "assets/imgs/backgrounds/fase1-overlay.png"
    OBSTACLES_ASSET = "scenes/phase1_obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase1/interactable.txt"
    STAGE_NAME = "1 - Banheiro da UFF"
    OBJECTIVE = "Coletar o Desentupidor Reforçado na cabine"

    def __init__(self, window, window_width, window_height, spawn_pos=None, player=None):
        super().__init__(
            window,
            window_width,
            window_height,
            self.BACKGROUND_ASSET,
            self.OVERLAY_ASSET,
            self.OBSTACLES_ASSET,
            self.INTERACTABLES_ASSET,
            self.STAGE_NAME,
            self.OBJECTIVE,
            player=player,
        )
        self.__scale_x = window_width / 1697
        self.__scale_y = window_height / 927

        if spawn_pos is not None:
            self.player.teleport_to(spawn_pos[0], spawn_pos[1])
        elif player is None:
            # Privadus desperta no piso central do banheiro se for nova partida
            self.player.teleport_to(
                round(650 * self.__scale_x),
                round(540 * self.__scale_y),
            )

        self.__step = 1
        self.__plunger_collected = self.player.has_plunger

        # Carrega sprite visual do desentupidor no cenário (cabine 3, parede esquerda)
        project_root = Path(__file__).resolve().parents[2]
        self.__plunger_img = None
        plunger_path = project_root / "assets/imgs/items/desentupidor.png"
        if plunger_path.exists():
            self.__plunger_img = GameImage(str(plunger_path))
            self.__plunger_img.x = round(235 * self.__scale_x)
            self.__plunger_img.y = round(300 * self.__scale_y)

        if self.player.has_plunger:
            self.__step = 2
            self.hud.set_objective(
                "Coletar Papel Higiênico Projetil no dispenser da parede norte"
            )
            self.__point_arrow(1250, 310)
        else:
            # Passo 1: aponta para o Desentupidor Reforçado na cabine 3 (canto superior esquerdo)
            self.__point_arrow(251, 332)

    @property
    def step(self):
        return self.__step

    @property
    def tp_ammo(self):
        return self.ammo

    def __point_arrow(self, base_x, base_y):
        self.yellow_arrow.set_target(
            round(base_x * self.__scale_x),
            round(base_y * self.__scale_y),
        )

    def __spawn_initial_cocos(self):
        # Espalha a patrulha pelo piso livre, longe das pias no canto superior direito.
        positions = [(500, 700), (850, 750), (1130, 620)]
        for bx, by in positions:
            self._add_enemy(
                Coco(round(bx * self.__scale_x), round(by * self.__scale_y))
            )

    def _can_interact_with(self, interactable):
        """Permite interação com objetos estritamente quando for a etapa correspondente."""
        tag = interactable.tag
        if self.__step == 1:
            return tag in ("plunger", "cabin")
        elif self.__step == 2:
            return tag == "dispenser"
        elif self.__step == 3:
            # Etapa de combate: nenhum objeto do cenário é interagível
            return False
        elif self.__step == 4:
            return tag == "valve"
        elif self.__step == 5:
            return tag in ("toilet", "magic_toilet")
        elif self.__step == 6:
            return tag in ("toilet", "magic_toilet")
        return False

    def update(self, delta_time):
        super().update(delta_time)

        # Durante o Passo 3, aponta dinamicamente para o Coco mais próximo
        if self.__step == 3:
            if len(self.enemies) > 0:
                nearest = min(
                    self.enemies,
                    key=lambda e: (e.x - self.player.x) ** 2 + (e.y - self.player.y) ** 2,
                )
                self.yellow_arrow.set_target(
                    round(nearest.x + nearest.bounds[2] / 2),
                    round(nearest.y + nearest.bounds[3] / 2),
                )
            else:
                # Passo 3 -> Passo 4: todos os Cocos eliminados
                self.__step = 4
                self.hud.set_objective("Aliviar a pressão na válvula da parede direita")
                self.__point_arrow(1400, 500)

        # Passo 5: alcançar o vaso mágico; passo 6 pede a interação para descer.
        elif self.__step == 5:
            toilet_x = round(650 * self.__scale_x)
            toilet_y = round(520 * self.__scale_y)
            dist = (
                (self.player.x - toilet_x) ** 2 + (self.player.y - toilet_y) ** 2
            ) ** 0.5
            if dist <= 80:
                self.__step = 6
                self.hud.set_objective("Pressionar E no vaso principal para descer pelo cano")

    def on_interact(self, interactable):
        """Executa a progressão sequencial dos mini-objetivos da Fase 1."""
        if interactable.tag in ("plunger", "cabin") and self.__step == 1:
            self.__plunger_collected = True
            self.player.equip_plunger()
            self.__step = 2
            self.hud.set_objective(
                "Coletar Papel Higiênico Projetil no dispenser da parede norte"
            )
            self.__point_arrow(1250, 310)

        elif interactable.tag == "dispenser" and self.__step == 2:
            self.add_ammo(15)
            self.__step = 3
            self.__spawn_initial_cocos()
            self.hud.set_objective("Eliminar a patrulha de Cocos menores perto das pias")

        elif interactable.tag == "valve" and self.__step == 4:
            self.__step = 5
            self.hud.set_objective("Ir ao vaso principal no canto inferior esquerdo")
            self.__point_arrow(650, 520)

        elif interactable.tag in ("toilet", "magic_toilet") and self.__step == 5:
            self.__step = 6
            self.hud.set_objective("Pressionar E no vaso principal para descer pelo cano")

        elif interactable.tag in ("toilet", "magic_toilet") and self.__step == 6:
            self._request_transition("phase2")

    def draw(self):
        super().draw()
        # Desenha o desentupidor no cenário se ainda não foi coletado
        if not self.__plunger_collected and not self.player.has_plunger:
            if self.__plunger_img:
                self.__plunger_img.draw()
            else:
                # Fallback visual caso a imagem não esteja na pasta assets ainda
                pygame.draw.rect(
                    self.window.screen,
                    (180, 50, 50),
                    (round(235 * self.__scale_x), round(300 * self.__scale_y), 15, 35),
                )
