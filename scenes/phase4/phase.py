"""Fase 4: Reservatório Tóxico da Ratazana Gigante."""

import math

from objects.enemies.ratazana_gigante import RatazanaGigante
from objects.audio import Audio
from objects.interactable import Interactable
from scenes.phase import Phase


class Phase4(Phase):
    STAGE_NAME = "4 - Reservatório Tóxico"
    OBJECTIVE = "Descer até o platô central do reservatório"
    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase4.png"
    OBSTACLES_ASSET = "scenes/phase4/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase4/interactable.txt"

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
            fallback_background_color=(37, 57, 42),
        )
        Audio.play_music("trilha_BossFightRatão.mp3")
        self.__scale_x = window_width / 1672
        self.__scale_y = window_height / 941
        self.__window_width = window_width
        self.__window_height = window_height
        self.player.teleport_to(round(835 * self.__scale_x), round(215 * self.__scale_y))
        self.__step = 1
        self.__boss = None
        self.__point_arrow(836, 470)

    @property
    def step(self):
        return self.__step

    def __point_arrow(self, x, y):
        self.yellow_arrow.set_target(
            round(x * self.__scale_x), round(y * self.__scale_y)
        )

    def __advance(self, step, objective, target=None):
        self.__step = step
        self.hud.set_objective(objective)
        if target is not None:
            self.__point_arrow(*target)

    def _can_interact_with(self, interactable):
        active_tags = {
            2: "aromatic_tablet",
            4: "selenium_seal",
            5: "abyssal_outlet",
        }
        return interactable.tag == active_tags.get(self.__step)

    def update(self, delta_time):
        super().update(delta_time)
        if self.__step == 1:
            target_x, target_y = 836 * self.__scale_x, 470 * self.__scale_y
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            if math.hypot(player_x - target_x, player_y - target_y) <= 70:
                self.__advance(
                    2,
                    "Colocar a pastilha aromática no pedestal central",
                    (836, 470),
                )
        elif self.__step == 3 and self.__boss is not None:
            if self.__boss.is_alive:
                self.yellow_arrow.set_target(
                    round(self.__boss.x + self.__boss.bounds[2] / 2),
                    round(self.__boss.y + self.__boss.bounds[3] / 2),
                )
            elif self.__boss not in self.enemies:
                self._add_interactable(
                    Interactable(
                        self.__boss.x - 12,
                        self.__boss.y - 12,
                        self.__boss.x + self.__boss.bounds[2] + 12,
                        self.__boss.y + self.__boss.bounds[3] + 12,
                        tag="selenium_seal",
                    )
                )
                self.__advance(
                    4,
                    "Coletar o Lacre de Selênio deixado pela Ratazana Gigante",
                )
                self.yellow_arrow.set_target(
                    round(self.__boss.x + self.__boss.bounds[2] / 2),
                    round(self.__boss.y + self.__boss.bounds[3] / 2),
                )

    def on_interact(self, interactable):
        if interactable.tag == "aromatic_tablet" and self.__step == 2:
            Audio.play_effect("sfx_rei_rato_grito.wav")
            boss = RatazanaGigante(
                round(self.__window_width / 2 - 50),
                round(self.__window_height / 2 - 50),
            )
            self.__boss = boss
            self._add_enemy(boss)
            self.__advance(
                3,
                "Derrotar a Ratazana Gigante e evitar as poças de veneno",
                (836, 410),
            )
        elif interactable.tag == "selenium_seal" and self.__step == 4:
            self.player.add_item("lacre_selenio")
            self.__advance(
                5,
                "Saltar no vertedouro que leva ao Super Esgoto",
                (836, 875),
            )
        elif interactable.tag == "abyssal_outlet" and self.__step == 5:
            Audio.stop_music()
            self._request_transition("phase5")
