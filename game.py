"""Centraliza o ciclo de vida e o estado geral do jogo."""

from pplay.window import Window
from scenes.menu import Menu
from scenes.phase1.phase import Phase1
from scenes.phase2.phase import Phase2


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

        transition_name = self.__current_scene.consume_transition_request()
        if transition_name == "phase1":
            self.__current_scene = Phase1(
                self.__window,
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT,
            )
        elif transition_name == "phase2":
            self.__current_scene = Phase2(
                self.__window,
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT,
            )
        elif transition_name == "quit":
            self.stop()
