"""Centraliza o ciclo de vida e o estado geral do jogo."""

import pygame
from pplay.window import Window
from scenes.ending import Ending
from scenes.game_over import GameOver
from scenes.menu import Menu
from objects.audio import Audio
from scenes.phase1.phase import Phase1
from scenes.phase2.phase import Phase2
from scenes.phase3.phase import Phase3
from scenes.phase4.phase import Phase4
from scenes.phase5.phase import Phase5
from scenes.phase6.phase import Phase6


class Game:
    """Coordena a janela e o loop principal de Missão Privada."""

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 700

    def __init__(self):
        self.__window = Window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.__window.set_title("Missão Privada")

        self.__is_running = True
        self.__elapsed_time = 0.0
        self.__current_scene = Menu(self.__window)

    def run(self):
        """Executa o loop principal até o jogo ser encerrado."""
        while self.__is_running:
            delta_time = self.__window.delta_time()

            pygame.event.pump()
            self.__current_scene.process_input()
            self.__update(delta_time)
            self.__current_scene.draw()

            self.__window.update()

    def stop(self):
        """Solicita o encerramento do loop principal."""
        self.__is_running = False

    def __update(self, delta_time):
        """Atualiza o estado do jogo usando o tempo do último quadro."""
        self.__elapsed_time += delta_time
        self.__current_scene.update(delta_time)

        if (
            hasattr(self.__current_scene, "player")
            and not self.__current_scene.player.is_alive
        ):
            Audio.stop_music()
            self.__current_scene = GameOver(self.__window)
            return

        transition_name = self.__current_scene.consume_transition_request()
        if transition_name:
            carry_player = None
            if hasattr(self.__current_scene, "player"):
                carry_player = self.__current_scene.player

            if transition_name == "phase1":
                self.__current_scene = Phase1(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "phase2":
                self.__current_scene = Phase2(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "phase3":
                self.__current_scene = Phase3(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "phase4":
                self.__current_scene = Phase4(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "phase5":
                self.__current_scene = Phase5(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "phase6":
                self.__current_scene = Phase6(
                    self.__window,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    player=carry_player,
                )
            elif transition_name == "ending":
                self.__current_scene = Ending(self.__window)
            elif transition_name == "menu":
                self.__current_scene = Menu(self.__window)
            elif transition_name == "quit":
                self.stop()
