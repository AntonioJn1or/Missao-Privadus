"""Hitbox baixa usada apenas para colisões durante a locomoção."""

from pplay.gameobject import GameObject


class LocomotionHurtbox(GameObject):
    """Acompanha os pés do jogador, mantendo a largura do sprite."""

    HEIGHT_RATIO = 0.3

    def __init__(self, sprite_width, sprite_height):
        super().__init__()
        self.width = sprite_width
        self.height = sprite_height * self.HEIGHT_RATIO

    def follow(self, sprite_x, sprite_y, sprite_width, sprite_height):
        """Alinha a hitbox à largura do sprite e à faixa inferior dos pés."""
        self.width = sprite_width
        self.height = sprite_height * self.HEIGHT_RATIO
        self.x = sprite_x
        self.y = sprite_y + sprite_height - self.height
