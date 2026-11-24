"""Segunda fase de Missão Privada: Galerias de Manutenção da UFF."""

from objects.enemies.alimento_zumbi import AlimentoZumbi
from objects.enemies.coco import Coco
from objects.enemies.rei_coco import ReiCoco
from objects.audio import Audio
from objects.interactable import Interactable
from scenes.phase import Phase


class Phase2(Phase):
    """Cômodo subterrâneo de manutenção, conectando o banheiro às galerias."""

    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase2.png"
    OVERLAY_ASSET = "assets/imgs/backgrounds/fase2-overlay.png"
    OBSTACLES_ASSET = "scenes/phase2/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase2/interactable.txt"

    STAGE_NAME = "2 - Galerias de Manutenção da UFF"
    OBJECTIVE = "Eliminar a patrulha de dejetos nas galerias"

    def __init__(self, window, window_width, window_height, player=None):
        super().__init__(
            window,
            window_width,
            window_height,
            self.BACKGROUND_ASSET,
            self.OVERLAY_ASSET,
            self.OBSTACLES_ASSET,
            self.INTERACTABLES_ASSET,
            self.STAGE_NAME,
            self.OBJECTIVE,
            player=player,
        )
        Audio.stop_music()
        self.__scale_x = window_width / 1697
        self.__scale_y = window_height / 927

        # Privadus surge vindo da queda do encanamento à esquerda
        self.player.teleport_to(140, 380)

        self.__step = 1
        self.__boss = None
        self.__gate_opened = False

        # Passo 1: Patrulha inicial de inimigos nas galerias
        self._add_enemy(Coco(round(600 * self.__scale_x), round(420 * self.__scale_y)))
        self._add_enemy(Coco(round(950 * self.__scale_x), round(320 * self.__scale_y)))
        self._add_enemy(AlimentoZumbi(round(1200 * self.__scale_x), round(450 * self.__scale_y)))

    @property
    def step(self):
        """Etapa atual da progressão de objetivos da Fase 2."""
        return self.__step

    def __point_arrow(self, base_x, base_y):
        self.yellow_arrow.set_target(
            round(base_x * self.__scale_x),
            round(base_y * self.__scale_y),
        )

    def _can_interact_with(self, interactable):
        """Restringe as interações estritamente à etapa ativa do roteiro."""
        tag = interactable.tag
        if self.__step == 2:
            return tag == "electrical_panel"
        elif self.__step == 3:
            return tag == "hydraulic_pump"
        elif self.__step == 5:
            return tag == "master_key"
        elif self.__step == 6:
            return tag == "sewer_gate"
        return False

    def update(self, delta_time):
        super().update(delta_time)

        # Passo 1: Aponta para o inimigo mais próximo até limpar a patrulha inicial
        if self.__step == 1:
            if len(self.enemies) > 0:
                nearest = min(
                    self.enemies,
                    key=lambda e: (e.x - self.player.x) ** 2 + (e.y - self.player.y) ** 2,
                )
                self.yellow_arrow.set_target(
                    round(nearest.x + nearest.bounds[2] / 2),
                    round(nearest.y + nearest.bounds[3] / 2),
                )
            else:
                self.__step = 2
                self.hud.set_objective("Religar a chave geral no painel de energia")
                self.__point_arrow(810, 300)

        # Passo 4: Rei Coco e minions invocados.
        elif self.__step == 4:
            if self.__boss is not None and self.__boss.is_alive:
                # Coleta minions gerados por transição de fase do chefe
                new_minions = self.__boss.pop_pending_minions()
                for minion in new_minions:
                    self._add_enemy(minion)

                self.yellow_arrow.set_target(
                    round(self.__boss.x + self.__boss.bounds[2] / 2),
                    round(self.__boss.y + self.__boss.bounds[3] / 2),
                )
            elif self.enemies:
                nearest = min(
                    self.enemies,
                    key=lambda enemy: (enemy.x - self.player.x) ** 2
                    + (enemy.y - self.player.y) ** 2,
                )
                self.yellow_arrow.set_target(
                    round(nearest.x + nearest.bounds[2] / 2),
                    round(nearest.y + nearest.bounds[3] / 2),
                )
                self.hud.set_objective("Eliminar os Cocos invocados pelo Rei Coco")
            else:
                # Chefe e minions eliminados: buscar a chave que ele deixou.
                Audio.stop_music()
                self.__step = 5
                self._add_interactable(
                    Interactable(
                        self.__boss.x - 12,
                        self.__boss.y - 12,
                        self.__boss.x + self.__boss.bounds[2] + 12,
                        self.__boss.y + self.__boss.bounds[3] + 12,
                        tag="master_key",
                    )
                )
                self.hud.set_objective("Coletar a Chave Mestra da Grelha Sanitária")
                self.yellow_arrow.set_target(
                    round(self.__boss.x + self.__boss.bounds[2] / 2),
                    round(self.__boss.y + self.__boss.bounds[3] / 2),
                )

        elif self.__step == 6:
            self.__point_arrow(1560, 480)

    def on_interact(self, interactable):
        """Executa as ações interativas da Fase 2 na ordem correta."""
        if interactable.tag == "electrical_panel" and self.__step == 2:
            self.__step = 3
            self.hud.set_objective("Ativar a bomba hidráulica para drenar o lodo")
            self.__point_arrow(1235, 340)

        elif interactable.tag == "hydraulic_pump" and self.__step == 3:
            # Drenagem concluída — surge o Chefe Rei Coco
            Audio.play_effect("EfeitoProReiCocoAparecendo.mp3")
            Audio.play_music("trilha_BossFightRatão.mp3")
            self.__boss = ReiCoco(
                round(880 * self.__scale_x),
                round(440 * self.__scale_y),
            )
            self._add_enemy(self.__boss)
            self.__step = 4
            self.hud.set_objective("Derrotar o temível Rei Coco")

        elif interactable.tag == "master_key" and self.__step == 5:
            self.__step = 6
            self.hud.set_objective("Abrir o alçapão enferrujado para descer ao esgoto")
            self.__point_arrow(1560, 480)

        elif interactable.tag == "sewer_gate" and self.__step == 6:
            self.__gate_opened = True
            self.hud.set_objective("Comporta aberta! Descendo ao Labirinto de Galerias")
            self._request_transition("phase3")
