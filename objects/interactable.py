"""Retângulo que detecta a proximidade do jogador para interação."""

import math

from pplay.gameobject import GameObject


class Interactable(GameObject):
    """Área retangular que não bloqueia movimento e mede proximidade."""

    def __init__(self, start_x, start_y, end_x, end_y, tag="default"):
        super().__init__()
        self.x = min(start_x, end_x)
        self.y = min(start_y, end_y)
        self.width = abs(end_x - start_x)
        self.height = abs(end_y - start_y)
        self.__tag = tag

        if self.width == 0 or self.height == 0:
            raise ValueError(
                "Interactable precisa ter largura e altura maiores que zero"
            )

    @property
    def tag(self):
        """Identificador ou tipo da interação associada a esta área."""
        return self.__tag

    def distance_to(self, bounds):
        """Distância euclidiana entre esta área e outro retângulo."""
        bounds_x, bounds_y, bounds_width, bounds_height = bounds
        horizontal_gap = max(
            self.x - (bounds_x + bounds_width),
            bounds_x - (self.x + self.width),
            0,
        )
        vertical_gap = max(
            self.y - (bounds_y + bounds_height),
            bounds_y - (self.y + self.height),
            0,
        )
        return math.hypot(horizontal_gap, vertical_gap)

    @property
    def popup_position(self):
        """Centro da borda superior, para fixar o indicador neste objeto."""
        return (self.x + self.width / 2, self.y)
