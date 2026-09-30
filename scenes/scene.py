"""Superclasse para as telas e fases do jogo."""


class Scene:
    """Define a interface comum de entrada, atualização e desenho."""

    def __init__(self, window):
        self.__window = window
        self.__requested_transition = None

    @property
    def window(self):
        """Janela do jogo, disponibilizada às cenas de forma somente leitura."""
        return self.__window

    def process_input(self):
        """Lê entradas específicas da cena atual."""
        pass

    def update(self, delta_time):
        """Atualiza o estado da cena atual."""
        pass

    def draw(self):
        """Limpa a tela; subclasses desenham seu conteúdo depois disso."""
        self.__window.set_background_color((0, 0, 0))

    def _request_transition(self, transition_name):
        """Solicita ao Game a troca para outra cena."""
        self.__requested_transition = transition_name

    def consume_transition_request(self):
        """Retorna e limpa uma solicitação de troca de cena pendente."""
        transition_name = self.__requested_transition
        self.__requested_transition = None
        return transition_name
