"""Primeira fase de Missão Privada."""

from scenes.phase import Phase


class Phase1(Phase):
    """Fase inicial, ambientada no banheiro da estrutura da UFF."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase1.png"
    OVERLAY_ASSET = "assets/imgs/backgrounds/fase1-overlay.png"
    OBSTACLES_ASSET = "scenes/phase1_obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase1/interactable.txt"
    STAGE_NAME = "1 - Banheiro da UFF"
    OBJECTIVE = "Encontrar o gnomo"

    def __init__(self, window, window_width, window_height, spawn_pos=None):
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
        if spawn_pos is not None:
            self.player.teleport_to(spawn_pos[0], spawn_pos[1])

        # Seta amarela guia apontando para a porta que leva ao próximo cômodo
        scale_x = window_width / 1697
        scale_y = window_height / 927
        self.yellow_arrow.set_target(
            round(1460 * scale_x),
            round(600 * scale_y),
        )
