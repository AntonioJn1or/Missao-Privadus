"""Fase 3: Labirinto de Galerias Fétidas."""

import math
from pathlib import Path

import pygame

from objects.enemies.ratazana import Ratazana
from objects.obstacle import Obstacle
from scenes.phase import Phase


class Phase3(Phase):
    STAGE_NAME = "3 - Labirinto de Galerias Fétidas"
    OBJECTIVE = "Cruzar a passarela do canal sul"
    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase3-1.png"
    OBSTACLES_ASSET = "scenes/phase3/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase3/interactable.txt"
    RESERVOIR_OBSTACLES_ASSET = "scenes/phase3/obstacles_reservoir.txt"
    RESERVOIR_INTERACTABLES_ASSET = "scenes/phase3/interactable_reservoir.txt"
    RESERVOIR_BACKGROUND_ASSET = "assets/imgs/backgrounds/fase3-2.png"
    SOURCE_WIDTH = 1672
    SOURCE_HEIGHT = 941

    def __init__(self, window, window_width, window_height, player=None):
        super().__init__(
            window,
            window_width,
            window_height,
            self.BACKGROUND_ASSET,
            None,
            self.OBSTACLES_ASSET,
            self.INTERACTABLES_ASSET,
            self.STAGE_NAME,
            self.OBJECTIVE,
            player=player,
            fallback_background_color=(23, 48, 52),
        )
        self.__scale_x = window_width / self.SOURCE_WIDTH
        self.__scale_y = window_height / self.SOURCE_HEIGHT
        project_root = Path(__file__).resolve().parents[2]
        barricade_path = project_root / "assets/imgs/backgrounds/barricada_de_coco.png"
        barricade_sheet = pygame.image.load(str(barricade_path)).convert_alpha()
        barricade_bounds = barricade_sheet.get_bounding_rect(min_alpha=1)
        self.__barricade_image = barricade_sheet.subsurface(barricade_bounds).copy()
        self.__barricade_size = (round(150 * self.__scale_x), round(65 * self.__scale_y))
        self.__barricade_image = pygame.transform.smoothscale(
            self.__barricade_image, self.__barricade_size
        )
        self.player.teleport_to(round(110 * self.__scale_x), round(730 * self.__scale_y))
        self.__step = 1
        self.__barricade = (1590, 390)
        self.__barricade_cleared = False
        self.__barricade_obstacle = Obstacle(
            round(1515 * self.__scale_x),
            round(365 * self.__scale_y),
            round(1665 * self.__scale_x),
            round(430 * self.__scale_y),
        )
        self._add_obstacle(self.__barricade_obstacle)
        self.__point_arrow(650, 800)

        for x, y in ((375, 250), (1100, 390), (1280, 690)):
            self._add_enemy(Ratazana(round(x * self.__scale_x), round(y * self.__scale_y)))

    @property
    def step(self):
        return self.__step

    def _draw_additional_effects(self, screen):
        if not self.__barricade_cleared:
            screen.blit(
                self.__barricade_image,
                (
                    round(self.__barricade[0] * self.__scale_x - self.__barricade_size[0] / 2),
                    round(self.__barricade[1] * self.__scale_y - self.__barricade_size[1] / 2),
                ),
            )

    def __point_arrow(self, x, y):
        self.yellow_arrow.set_target(
            round(x * self.__scale_x), round(y * self.__scale_y)
        )

    def __advance(self, step, objective, target):
        self.__step = step
        self.hud.set_objective(objective)
        self.__point_arrow(*target)

    def _can_interact_with(self, interactable):
        active_tags = {
            2: "western_gate",
            3: "desinfetante",
            4: "eastern_gate",
            6: "reservoir_gate",
            7: "reservoir_gate",
        }
        return interactable.tag == active_tags.get(self.__step)

    def update(self, delta_time):
        super().update(delta_time)
        if self.__step == 1:
            target_x, target_y = (
                650 * self.__scale_x,
                800 * self.__scale_y,
            )
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            if math.hypot(player_x - target_x, player_y - target_y) <= 65:
                self.__advance(
                    2,
                    "Fechar o vazamento na comporta ocidental",
                    (276, 165),
                )
        elif self.__step == 5:
            self.__point_arrow(*self.__barricade)

    def trigger_descarga(self):
        triggered = super().trigger_descarga()
        if triggered and self.__step == 5:
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            target_x = self.__barricade[0] * self.__scale_x
            target_y = self.__barricade[1] * self.__scale_y
            if math.hypot(player_x - target_x, player_y - target_y) <= 220:
                self._remove_obstacle(self.__barricade_obstacle)
                self.__barricade_cleared = True
                self.__advance(
                    6,
                    "Seguir pelo arco de tijolos até o Reservatório Central",
                    (1615, 390),
                )
        return triggered

    def on_interact(self, interactable):
        if interactable.tag == "western_gate" and self.__step == 2:
            self.__advance(
                3,
                "Coletar o kit de desentupimento no cais sudeste",
                (1270, 680),
            )
        elif interactable.tag == "desinfetante" and self.__step == 3:
            self.increase_projectile_damage(10)
            self.add_ammo(8)
            self.__advance(
                4,
                "Acionar a manivela oriental para drenar a água",
                (1505, 267),
            )
        elif interactable.tag == "eastern_gate" and self.__step == 4:
            self.__advance(
                5,
                "Usar Q para afastar a barricada de cocos",
                self.__barricade,
            )
        elif interactable.tag == "reservoir_gate" and self.__step == 6:
            self._replace_map_assets(
                self.RESERVOIR_BACKGROUND_ASSET,
                self.RESERVOIR_OBSTACLES_ASSET,
                self.RESERVOIR_INTERACTABLES_ASSET,
            )
            self.player.teleport_to(
                round(1480 * self.__scale_x), round(470 * self.__scale_y)
            )
            self.__barricade_cleared = True
            self.__advance(
                7,
                "Atravessar a sala até a entrada do Reservatório Central",
                (835, 195),
            )
        elif interactable.tag == "reservoir_gate" and self.__step == 7:
            self._request_transition("phase4")
