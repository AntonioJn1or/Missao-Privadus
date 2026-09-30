"""Jogador Privadus e sua representação visual."""

import math

import pygame
from pplay.sprite import Sprite

from objects.locomotion_hurtbox import LocomotionHurtbox


_DIRECTION_NAMES = (
    "up",
    "up_right",
    "right",
    "down_right",
    "down",
    "down_left",
    "left",
    "up_left",
)
_STATE_NAMES = ("idle", "walking", "attacking", "hurt", "dead")
_STAND_RIGHT_ASSET = "assets/imgs/privadus/stand_right.png"
_WALKING_RIGHT_ASSET = "assets/imgs/privadus/walking_right.png"

_SPRITE_TABLE = {
    direction: {state: _STAND_RIGHT_ASSET for state in _STATE_NAMES}
    for direction in _DIRECTION_NAMES
}
for _direction in _DIRECTION_NAMES:
    _SPRITE_TABLE[_direction]["walking"] = _WALKING_RIGHT_ASSET

_DIRECTION_BY_INPUT = {
    (0, -1): "up",
    (1, -1): "up_right",
    (1, 0): "right",
    (1, 1): "down_right",
    (0, 1): "down",
    (-1, 1): "down_left",
    (-1, 0): "left",
    (-1, -1): "up_left",
}
_LEFT_FACING_DIRECTIONS = frozenset(("left", "up_left", "down_left"))


class Player:
    """Encapsula o sprite, a direção, o estado e o movimento de Privadus."""

    FRAME_COUNT = 8
    SCALE_FACTOR = 1.5
    FRAME_WIDTH = int(60 * SCALE_FACTOR)
    FRAME_HEIGHT = int(70 * SCALE_FACTOR)
    MOVEMENT_SPEED = 180
    ANIMATION_DURATION_MS = 600

    DIRECTIONS = _DIRECTION_NAMES
    STATES = _STATE_NAMES

    # Por enquanto, estados sem arte própria usam stand_right como fallback.
    SPRITE_TABLE = _SPRITE_TABLE

    def __init__(self, x=0, y=0):
        self.__facing_direction = "right"
        self.__state = "idle"
        self.__x = x
        self.__y = y
        self.__sprite = None
        self.__active_sprite_key = None
        self.__load_current_spritesheet()
        self.__locomotion_hurtbox = LocomotionHurtbox(
            self.__sprite.width,
            self.__sprite.height,
        )
        self.__sync_positions()

    @property
    def facing_direction(self):
        """Direção atual do olhar, entre as oito direções suportadas."""
        return self.__facing_direction

    @property
    def state(self):
        """Estado atual de animação do personagem."""
        return self.__state

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def interaction_bounds(self):
        """Limites da hitbox dos pés para detectar objetos próximos."""
        return (
            self.__locomotion_hurtbox.x,
            self.__locomotion_hurtbox.y,
            self.__locomotion_hurtbox.width,
            self.__locomotion_hurtbox.height,
        )

    def teleport_to(self, x, y):
        """Teletransporta Privadus e alinha suas hitboxes."""
        self.__x = x
        self.__y = y
        self.__sync_positions()

    def set_facing_direction(self, direction):
        """Define para onde Privadus olha."""
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direção inválida: {direction}")

        self.__facing_direction = direction
        self.__load_current_spritesheet()
        self.__sync_positions()

    def set_state(self, state):
        """Define o estado visual de Privadus."""
        if state not in self.STATES:
            raise ValueError(f"Estado inválido: {state}")

        self.__state = state
        self.__load_current_spritesheet()
        self.__sync_positions()

    def update(self, horizontal_input, vertical_input, delta_time, obstacles=()):
        """Move Privadus nas oito direções sem limitar o tamanho da tela."""
        horizontal_input = max(-1, min(1, horizontal_input))
        vertical_input = max(-1, min(1, vertical_input))

        sign_x = (horizontal_input > 0) - (horizontal_input < 0)
        sign_y = (vertical_input > 0) - (vertical_input < 0)
        input_length = math.hypot(sign_x, sign_y)

        if input_length:
            self.__facing_direction = _DIRECTION_BY_INPUT[(sign_x, sign_y)]
            if self.__state in ("idle", "walking"):
                self.__state = "walking"
        elif self.__state == "walking":
            self.__state = "idle"

        if input_length > 1:
            horizontal_input /= input_length
            vertical_input /= input_length

        self.__load_current_spritesheet()
        distance_x = horizontal_input * self.MOVEMENT_SPEED * delta_time
        distance_y = vertical_input * self.MOVEMENT_SPEED * delta_time
        self.__move_axis("x", distance_x, obstacles)
        self.__move_axis("y", distance_y, obstacles)

        self.__sync_positions()

    def __move_axis(self, axis, distance, obstacles):
        if distance == 0:
            return

        steps = max(1, math.ceil(abs(distance)))
        step_size = distance / steps

        for _ in range(steps):
            if axis == "x":
                candidate = self.__x + step_size
                candidate_x = candidate
                candidate_y = self.__y
            else:
                candidate = self.__y + step_size
                candidate_x = self.__x
                candidate_y = candidate

            self.__locomotion_hurtbox.follow(
                candidate_x,
                candidate_y,
                self.__sprite.width,
                self.__sprite.height,
            )
            if any(
                self.__locomotion_hurtbox.collided(obstacle)
                for obstacle in obstacles
            ):
                self.__sync_positions()
                break

            if axis == "x":
                self.__x = candidate
            else:
                self.__y = candidate
            self.__sync_positions()

    def draw(self):
        """Desenha e avança um quadro da animação atual."""
        self.__sprite.draw()
        self.__sprite.update()

    def __load_current_spritesheet(self):
        relative_path = self.SPRITE_TABLE[self.__facing_direction][self.__state]
        flip_horizontally = self.__facing_direction in _LEFT_FACING_DIRECTIONS
        sprite_key = (relative_path, flip_horizontally)
        if sprite_key == self.__active_sprite_key:
            return

        self.__sprite = Sprite(relative_path, self.FRAME_COUNT)
        scaled_sheet_size = (
            self.__sprite.image.get_width() * self.SCALE_FACTOR,
            self.__sprite.image.get_height() * self.SCALE_FACTOR,
        )
        spritesheet = pygame.transform.scale(
            self.__sprite.image,
            scaled_sheet_size,
        )
        if flip_horizontally:
            spritesheet = self.__flip_spritesheet(spritesheet)

        self.__sprite.image = spritesheet
        self.__sprite.width *= self.SCALE_FACTOR
        self.__sprite.height *= self.SCALE_FACTOR
        self.__sprite.set_total_duration(self.ANIMATION_DURATION_MS)
        self.__sprite.x = self.__x
        self.__sprite.y = self.__y
        self.__active_sprite_key = sprite_key

    def __sync_positions(self):
        """Mantém o sprite e a hitbox de locomoção alinhados."""
        self.__sprite.x = self.__x
        self.__sprite.y = self.__y
        self.__locomotion_hurtbox.follow(
            self.__x,
            self.__y,
            self.__sprite.width,
            self.__sprite.height,
        )

    def __flip_spritesheet(self, spritesheet):
        frame_width = spritesheet.get_width() // self.FRAME_COUNT
        flipped_spritesheet = pygame.Surface(
            spritesheet.get_size(),
            pygame.SRCALPHA,
        )

        for frame_index in range(self.FRAME_COUNT):
            frame_area = pygame.Rect(
                frame_index * frame_width,
                0,
                frame_width,
                spritesheet.get_height(),
            )
            flipped_frame = pygame.transform.flip(
                spritesheet.subsurface(frame_area),
                True,
                False,
            )
            flipped_spritesheet.blit(
                flipped_frame,
                (frame_index * frame_width, 0),
            )

        return flipped_spritesheet
