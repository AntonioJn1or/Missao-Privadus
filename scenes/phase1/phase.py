"""Primeira fase de Missão Privada."""

from scenes.phase import Phase


class Phase1(Phase):
    """Fase inicial, ambientada no banheiro da estrutura da UFF."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase1.png"
    OVERLAY_ASSET = "assets/imgs/backgrounds/fase1-overlay.png"
    OBSTACLES_ASSET = "scenes/phase1_obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase1/interactable.txt"

    def __init__(self, window, window_width, window_height):
        super().__init__(
            window,
            window_width,
            window_height,
            self.BACKGROUND_ASSET,
            self.OVERLAY_ASSET,
            self.OBSTACLES_ASSET,
            self.INTERACTABLES_ASSET,
        )
