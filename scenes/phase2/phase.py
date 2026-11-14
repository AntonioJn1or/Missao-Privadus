"""Segunda fase / cômodo de Missão Privada: Galerias de Manutenção da UFF."""

from objects.enemies.coco import Coco
from scenes.phase import Phase


class Phase2(Phase):
    """Cômodo subterrâneo de manutenção, conectando o banheiro às galerias."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase2.png"
    OVERLAY_ASSET = "assets/imgs/backgrounds/fase2-overlay.png"
    OBSTACLES_ASSET = "scenes/phase2/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase2/interactable.txt"

    STAGE_NAME = "2 - Galerias de Manutenção da UFF"
    OBJECTIVE = "Encontrar o painel de energia e religar os geradores"

    def __init__(self, window, window_width, window_height):
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
        )
        # Privadus surge vindo da porta da esquerda
        self.player.teleport_to(140, 380)

        # Seta amarela guia apontando para o painel elétrico
        self.__scale_x = window_width / 1697
        self.__scale_y = window_height / 927
        self.yellow_arrow.set_target(
            round(810 * self.__scale_x),
            round(300 * self.__scale_y),
        )

        # Cocos iniciais espalhados pelas galerias
        self._add_enemy(Coco(round(500 * self.__scale_x), round(350 * self.__scale_y)))
        self._add_enemy(Coco(round(900 * self.__scale_x), round(250 * self.__scale_y)))
        self._add_enemy(Coco(round(1200 * self.__scale_x), round(430 * self.__scale_y)))

    def on_interact(self, interactable):
        """Ao interagir com a porta de retorno, volta ao banheiro; no painel, religa geradores."""
        if interactable.tag == "back_door":
            self._request_transition("phase1")
        elif interactable.tag == "electrical_panel":
            self.hud.set_objective("Geradores religados! Explorar a comporta do esgoto")
            # Atualiza a seta para a comporta do esgoto (próximo passo do roteiro)
            self.yellow_arrow.set_target(
                round(1560 * self.__scale_x),
                round(480 * self.__scale_y),
            )
        else:
            super().on_interact(interactable)
