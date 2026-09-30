"""Comportamento compartilhado pelas fases jogáveis."""

from pathlib import Path

import pygame
from pplay.gameimage import GameImage

from objects.interactable import Interactable
from objects.interaction_popup import InteractionPopup
from objects.obstacle import Obstacle
from objects.player import Player
from scenes.scene import Scene


class Phase(Scene):
    """Fase base com cenário, colisões e objetos interagíveis."""

    INTERACTION_DISTANCE = 20

    def __init__(
        self,
        window,
        window_width,
        window_height,
        background_asset,
        overlay_asset,
        obstacles_asset,
        interactables_asset,
    ):
        super().__init__(window)

        project_root = Path(__file__).resolve().parents[1]
        background_path = project_root / background_asset
        self.__background = GameImage(str(background_path))
        source_width = self.__background.width
        source_height = self.__background.height

        self.__background.image = pygame.transform.scale(
            self.__background.image,
            (window_width, window_height),
        )
        self.__background.width = window_width
        self.__background.height = window_height

        overlay_path = project_root / overlay_asset
        self.__overlay = GameImage(str(overlay_path))
        self.__overlay.image = pygame.transform.scale(
            self.__overlay.image,
            (window_width, window_height),
        )
        self.__overlay.width = window_width
        self.__overlay.height = window_height

        obstacles_path = project_root / obstacles_asset
        scale_x = window_width / source_width
        scale_y = window_height / source_height
        self.__obstacles = self.__load_rectangles(
            obstacles_path,
            scale_x,
            scale_y,
            Obstacle,
        )

        interactables_path = project_root / interactables_asset
        self.__interactables = self.__load_rectangles(
            interactables_path,
            scale_x,
            scale_y,
            Interactable,
        )

        player_x = 100
        player_y = 200
        self.__player = Player(player_x, player_y)
        self.__movement_input = (0, 0)
        self.__interaction_popup = InteractionPopup()
        self.__interaction_key_was_pressed = False
        self.__interaction_requested = False

    def process_input(self):
        keyboard = self.window.keyboard
        moving_left = keyboard.key_pressed("LEFT") or keyboard.key_pressed("A")
        moving_right = keyboard.key_pressed("RIGHT") or keyboard.key_pressed("D")
        moving_up = keyboard.key_pressed("UP") or keyboard.key_pressed("W")
        moving_down = keyboard.key_pressed("DOWN") or keyboard.key_pressed("S")

        horizontal_input = int(moving_right) - int(moving_left)
        vertical_input = int(moving_down) - int(moving_up)
        self.__movement_input = (horizontal_input, vertical_input)

        interaction_key_pressed = keyboard.key_pressed("E")
        self.__interaction_requested = (
            interaction_key_pressed and not self.__interaction_key_was_pressed
        )
        self.__interaction_key_was_pressed = interaction_key_pressed

    def update(self, delta_time):
        self.__player.update(
            self.__movement_input[0],
            self.__movement_input[1],
            delta_time,
            self.__obstacles,
        )

        nearby_interactable = self.__find_nearest_interactable()
        if self.__interaction_requested and nearby_interactable is not None:
            target_y = 280 if self.__player.y > 370 else 380
            self.__player.teleport_to(120, target_y)
            nearby_interactable = self.__find_nearest_interactable()

        self.__interaction_requested = False
        if nearby_interactable is None:
            self.__interaction_popup.hide()
            return

        center_x, top_y = nearby_interactable.popup_position
        self.__interaction_popup.show_above(center_x, top_y)

    def draw(self):
        super().draw()
        self.__background.draw()

        if self.__player.y < 370:
            self.__player.draw()
            self.__overlay.draw()
        else:
            self.__overlay.draw()
            self.__player.draw()

        self.__interaction_popup.draw()

    @staticmethod
    def __load_rectangles(rectangles_path, scale_x, scale_y, rectangle_class):
        rectangles = []

        with rectangles_path.open("r", encoding="utf-8") as rectangle_file:
            for line_number, line in enumerate(rectangle_file, start=1):
                if not line.strip():
                    continue

                try:
                    coordinates = [
                        int(coordinate.strip())
                        for coordinate in line.split(",")
                    ]
                except ValueError as error:
                    raise ValueError(
                        f"Coordenada inválida na linha {line_number} de "
                        f"{rectangles_path}"
                    ) from error

                if len(coordinates) != 4:
                    raise ValueError(
                        f"A linha {line_number} de {rectangles_path} "
                        "deve conter quatro inteiros"
                    )

                start_x, start_y, end_x, end_y = coordinates
                rectangles.append(
                    rectangle_class(
                        round(start_x * scale_x),
                        round(start_y * scale_y),
                        round(end_x * scale_x),
                        round(end_y * scale_y),
                    )
                )

        return rectangles

    def __find_nearest_interactable(self):
        player_bounds = self.__player.interaction_bounds
        nearby_interactables = (
            (
                interactable.distance_to(player_bounds),
                interactable,
            )
            for interactable in self.__interactables
        )
        nearby = [
            (distance, interactable)
            for distance, interactable in nearby_interactables
            if distance <= self.INTERACTION_DISTANCE
        ]
        if not nearby:
            return None

        return min(nearby, key=lambda candidate: candidate[0])[1]
