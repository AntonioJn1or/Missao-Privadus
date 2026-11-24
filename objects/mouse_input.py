"""Leitura do estado atual do mouse sem depender do cache do PPlay."""

import pygame


def read_mouse(window):
    """Retorna posição virtual e botões pressionados no frame atual."""
    position = pygame.mouse.get_pos()
    to_virtual = getattr(window, "screen_to_virtual_coords", None)
    if callable(to_virtual):
        position = to_virtual(*position)

    return position, pygame.mouse.get_pressed()


def mouse_position(window):
    """Retorna a posição atual do mouse na resolução lógica da janela."""
    position = pygame.mouse.get_pos()
    to_virtual = getattr(window, "screen_to_virtual_coords", None)
    if callable(to_virtual):
        return to_virtual(*position)
    return position
