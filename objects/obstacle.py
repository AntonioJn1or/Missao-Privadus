"""Retângulo invisível usado como hitbox de paredes e obstáculos."""

from pplay.gameobject import GameObject


class Obstacle(GameObject):
    """Representa um retângulo de colisão definido por dois cantos opostos."""

    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__()

        self.x = min(start_x, end_x)
        self.y = min(start_y, end_y)
        self.width = abs(end_x - start_x)
        self.height = abs(end_y - start_y)

        if self.width == 0 or self.height == 0:
            raise ValueError("Obstacle precisa ter largura e altura maiores que zero")
