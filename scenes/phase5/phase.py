"""Fase 5: Santuário do Lodo Proibido."""

import math

from objects.enemies.alimento_zumbi import AlimentoZumbi
from objects.enemies.coco_blindado import CocoBlindado
from scenes.phase import Phase


class Phase5(Phase):
    STAGE_NAME = "5 - Santuário do Lodo Proibido"
    OBJECTIVE = "Atravessar o portal e vencer a formação de Cocos arcanos"
    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase5.png"
    OBSTACLES_ASSET = "scenes/phase5/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase5/interactable.txt"

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
            fallback_background_color=(42, 31, 57),
        )
        self.__scale_x = window_width / 1672
        self.__scale_y = window_height / 941
        # A coordenada marca o topo do sprite (105 px), então Privadus começa
        # mais acima no piso para manter os pés dentro da plataforma e da janela.
        self.player.teleport_to(round(835 * self.__scale_x), round(745 * self.__scale_y))
        self.__step = 1
        self.__destroyed_runes = set()
        self.__point_arrow(835, 520)

        # Distribui a patrulha nas três plataformas superiores de pedra.
        for x, y in ((300, 320), (610, 340), (1040, 340), (1370, 320)):
            self._add_enemy(
                CocoBlindado(round(x * self.__scale_x), round(y * self.__scale_y))
            )
        for x, y in ((455, 365), (1210, 365)):
            self._add_enemy(
                AlimentoZumbi(round(x * self.__scale_x), round(y * self.__scale_y))
            )

    @property
    def step(self):
        return self.__step

    @property
    def destroyed_runes(self):
        return frozenset(self.__destroyed_runes)

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
            2: "west_rune",
            4: "east_rune",
            6: "throne_portal",
        }
        return interactable.tag == active_tags.get(self.__step)

    def update(self, delta_time):
        super().update(delta_time)
        if self.__step == 1:
            if self.enemies:
                nearest = min(
                    self.enemies,
                    key=lambda enemy: (enemy.x - self.player.x) ** 2
                    + (enemy.y - self.player.y) ** 2,
                )
                self.yellow_arrow.set_target(
                    round(nearest.x + nearest.bounds[2] / 2),
                    round(nearest.y + nearest.bounds[3] / 2),
                )
            else:
                self.__advance(
                    2,
                    "Destruir a Runa do Mau Cheiro na ala oeste",
                    (150, 275),
                )
        elif self.__step == 3:
            target_x, target_y = 835 * self.__scale_x, 370 * self.__scale_y
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            if math.hypot(player_x - target_x, player_y - target_y) <= 65:
                self.__advance(
                    4,
                    "Destruir a Runa da Corrupção na ala leste",
                    (1520, 275),
                )
        elif self.__step == 5:
            self.__point_arrow(835, 760)

    def trigger_descarga(self):
        triggered = super().trigger_descarga()
        if triggered and self.__step == 5:
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            rune_x, rune_y = 835 * self.__scale_x, 760 * self.__scale_y
            if math.hypot(player_x - rune_x, player_y - rune_y) <= 220:
                self.__destroyed_runes.add("center")
                self.__advance(
                    6,
                    "Atravessar a plataforma até o portal do Trono",
                    (835, 125),
                )

    def on_interact(self, interactable):
        if interactable.tag == "west_rune" and self.__step == 2:
            self.__destroyed_runes.add("west")
            self.__advance(
                3,
                "Atravessar a ponte até a plataforma central",
                (835, 370),
            )
        elif interactable.tag == "east_rune" and self.__step == 4:
            self.__destroyed_runes.add("east")
            self.__advance(
                5,
                "Destruir a Runa Central com a Descarga",
                (835, 760),
            )
        elif interactable.tag == "throne_portal" and self.__step == 6:
            self._request_transition("phase6")
