"""Indicador animado de que um objeto próximo pode ser usado."""

import pygame
from pplay.sprite import Sprite


class InteractionPopup:
    """Exibe e anima o ícone da tecla E acima do objeto interagível."""

    FRAME_COUNT = 6
    SCALE_FACTOR = 1.8
    ANIMATION_DURATION_MS = 600
    VERTICAL_OFFSET = 8

    def __init__(self):
        self.__sprite = Sprite(
            "assets/imgs/buttons/interaction_popup.png",
            self.FRAME_COUNT,
        )
        scaled_sheet_size = (
            round(self.__sprite.image.get_width() * self.SCALE_FACTOR),
            round(self.__sprite.image.get_height() * self.SCALE_FACTOR),
        )
        self.__sprite.image = pygame.transform.scale(
            self.__sprite.image,
            scaled_sheet_size,
        )
        self.__sprite.width *= self.SCALE_FACTOR
        self.__sprite.height *= self.SCALE_FACTOR
        self.__sprite.set_total_duration(self.ANIMATION_DURATION_MS)
        self.__is_visible = False

    def hide(self):
        """Oculta o indicador enquanto não houver objeto ao alcance."""
        self.__is_visible = False

    def show_above(self, center_x, top_y):
        """Torna o indicador visível e o posiciona acima do objeto."""
        self.__is_visible = True
        self.__sprite.x = center_x - self.__sprite.width / 2
        self.__sprite.y = top_y - self.__sprite.height - self.VERTICAL_OFFSET

    def draw(self):
        """Desenha e atualiza a animação no ponto fixo do objeto."""
        if not self.__is_visible:
            return

        self.__sprite.draw()
        self.__sprite.update()
