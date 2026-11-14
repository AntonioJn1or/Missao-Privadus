"""Pequena seta amarela indicadora do próximo passo/objetivo da fase."""

import math
import pygame


class YellowArrow:
    """Indica a direção euclidiana para o próximo objetivo da fase."""

    ARROW_WIDTH = 20
    ARROW_HEIGHT = 16
    COLOR_YELLOW = (255, 220, 20)
    COLOR_OUTLINE = (50, 40, 10)
    ORBIT_RADIUS = 55

    def __init__(self):
        self.__target_x = None
        self.__target_y = None
        self.__player_x = 0.0
        self.__player_y = 0.0
        self.__angle_degrees = 0.0
        self.__is_visible = True
        self.__pulse_timer = 0.0
        self.__base_surface = self.__create_arrow_surface()

    @property
    def is_visible(self):
        """Retorna se a seta amarela está visível."""
        return self.__is_visible and self.__target_x is not None

    @property
    def target(self):
        """Retorna as coordenadas atuais do alvo (x, y) ou None."""
        if self.__target_x is None:
            return None
        return (self.__target_x, self.__target_y)

    def set_target(self, target_x, target_y):
        """Define o ponto de destino para o qual a seta deve apontar."""
        self.__target_x = float(target_x)
        self.__target_y = float(target_y)
        self.__is_visible = True

    def clear_target(self):
        """Remove o alvo ativo e oculta a seta."""
        self.__target_x = None
        self.__target_y = None
        self.__is_visible = False

    def update(self, player_center_x, player_center_y, delta_time=0.0):
        """Calcula o ângulo em direção ao alvo e anima a flutuação da seta."""
        self.__player_x = float(player_center_x)
        self.__player_y = float(player_center_y)
        self.__pulse_timer += delta_time

        if self.__target_x is None or self.__target_y is None:
            return

        delta_x = self.__target_x - self.__player_x
        delta_y = self.__target_y - self.__player_y
        distance = math.hypot(delta_x, delta_y)

        # Se já estiver muito perto do alvo (dentro de 25px), oculta suavemente
        if distance <= 25:
            self.__is_visible = False
            return

        self.__is_visible = True
        angle_radians = math.atan2(delta_y, delta_x)
        self.__angle_degrees = -math.degrees(angle_radians)

    def draw(self, screen):
        """Desenha a seta amarela orientada na direção do próximo passo."""
        if not self.is_visible:
            return

        # Animação suave de pulso na órbita
        current_orbit = self.ORBIT_RADIUS + math.sin(self.__pulse_timer * 6.0) * 4.0
        angle_rad = -math.radians(self.__angle_degrees)
        pos_x = self.__player_x + math.cos(angle_rad) * current_orbit
        pos_y = self.__player_y + math.sin(angle_rad) * current_orbit

        # Rotaciona o sprite da seta
        rotated_arrow = pygame.transform.rotate(self.__base_surface, self.__angle_degrees)
        draw_rect = rotated_arrow.get_rect(center=(round(pos_x), round(pos_y)))
        screen.blit(rotated_arrow, draw_rect.topleft)

    def __create_arrow_surface(self):
        surf = pygame.Surface((self.ARROW_WIDTH, self.ARROW_HEIGHT), pygame.SRCALPHA)
        # Formato de seta apontando para a direita (0 graus padrão do pygame)
        points = [
            (self.ARROW_WIDTH - 2, self.ARROW_HEIGHT // 2),
            (2, 2),
            (6, self.ARROW_HEIGHT // 2),
            (2, self.ARROW_HEIGHT - 3),
        ]
        pygame.draw.polygon(surf, self.COLOR_OUTLINE, points)
        # Preenchimento interno ligeiramente menor
        inner_points = [
            (self.ARROW_WIDTH - 4, self.ARROW_HEIGHT // 2),
            (4, 4),
            (7, self.ARROW_HEIGHT // 2),
            (4, self.ARROW_HEIGHT - 5),
        ]
        pygame.draw.polygon(surf, self.COLOR_YELLOW, inner_points)
        return surf
