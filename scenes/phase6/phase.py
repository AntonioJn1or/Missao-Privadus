"""Fase 6: confronto final contra o Gnomo Malvado."""

import math

from objects.enemies.coco import Coco
from objects.enemies.gnomo_malvado import GnomoMalvado
from objects.audio import Audio
from scenes.phase import Phase


class Phase6(Phase):
    STAGE_NAME = "6 - Trono do Super Esgoto"
    OBJECTIVE = "Alcançar o círculo ritualístico para iniciar o duelo"
    BACKGROUND_ASSET = "assets/imgs/backgrounds/fase6.jpeg"
    OBSTACLES_ASSET = "scenes/phase6/obstacles.txt"
    INTERACTABLES_ASSET = "scenes/phase6/interactable.txt"
    FIRST_WAVE_SURVIVAL = 6.0
    RITUAL_POSITION = (512, 380)

    def __init__(self, window, window_width, window_height, player=None):
        super().__init__(
            window,
            window_width,
            window_height,
            self.BACKGROUND_ASSET,
            None,
            self.OBSTACLES_ASSET,
            self.INTERACTABLES_ASSET,
            self.STAGE_NAME,
            self.OBJECTIVE,
            player=player,
            fallback_background_color=(27, 20, 46),
        )
        Audio.play_music("trilha_FinalBoss.mp3")
        self.__scale_x = window_width / 1024
        self.__scale_y = window_height / 572
        self.__window_width = window_width
        self.__window_height = window_height
        # Alinha o centro do sprite de Privadus ao círculo ritualístico.
        ritual_x = self.RITUAL_POSITION[0] * self.__scale_x
        ritual_y = self.RITUAL_POSITION[1] * self.__scale_y
        self.player.teleport_to(
            round(ritual_x - self.player.FRAME_WIDTH / 2),
            round(ritual_y - self.player.FRAME_HEIGHT / 2),
        )
        self.__boss = GnomoMalvado(
            round(512 * self.__scale_x - 44),
            round(285 * self.__scale_y - 50),
            window_width,
        )
        self._add_enemy(self.__boss)
        self.__step = 1
        self.__survival_timer = 0.0
        self.__valves = set()
        self.__magic_projectiles = []
        self.__point_arrow(*self.RITUAL_POSITION)

    @property
    def step(self):
        return self.__step

    @property
    def magic_projectiles(self):
        return tuple(self.__magic_projectiles)

    def __point_arrow(self, x, y):
        self.yellow_arrow.set_target(
            round(x * self.__scale_x), round(y * self.__scale_y)
        )

    def __advance(self, step, objective, target):
        self.__step = step
        self.hud.set_objective(objective)
        self.__point_arrow(*target)

    def _can_interact_with(self, interactable):
        if self.__step == 3:
            next_valve = "left_valve" if "left_valve" not in self.__valves else "right_valve"
            return interactable.tag == next_valve and len(self.__valves) < 2
        return self.__step == 6 and interactable.tag == "golden_flush"

    def update(self, delta_time):
        super().update(delta_time)

        if self.__boss.is_alive:
            self.__magic_projectiles.extend(self.__boss.pop_pending_projectiles())
            pending_minions = self.__boss.pop_pending_minions()
            live_cocos = sum(
                isinstance(enemy, Coco) and enemy.is_alive for enemy in self.enemies
            )
            if len(self.__magic_projectiles) > 100:
                self.__magic_projectiles = self.__magic_projectiles[-100:]
            for minion in pending_minions[:max(0, 4 - live_cocos)]:
                self._add_enemy(minion)

        self.__update_magic_projectiles(delta_time)

        if self.__step == 1:
            target_x = self.RITUAL_POSITION[0] * self.__scale_x
            target_y = self.RITUAL_POSITION[1] * self.__scale_y
            player_x = self.player.x + self.player.FRAME_WIDTH / 2
            player_y = self.player.y + self.player.FRAME_HEIGHT / 2
            if math.hypot(player_x - target_x, player_y - target_y) <= 65:
                self.__boss.activate()
                self.__advance(
                    2,
                    "Sobreviver à primeira espiral de rajadas do amuleto",
                    (512, 285),
                )
        elif self.__step == 2:
            self.__survival_timer += delta_time
            if self.__survival_timer >= self.FIRST_WAVE_SURVIVAL:
                self.__advance(
                    3,
                    "Acionar as duas válvulas laterais para romper o escudo",
                    (175, 325),
                )
        elif self.__step == 4:
            self.yellow_arrow.set_target(
                round(self.__boss.x + self.__boss.bounds[2] / 2),
                round(self.__boss.y + self.__boss.bounds[3] / 2),
            )
            if self.__boss.hp <= self.__boss.max_hp / 2 and self.__boss.is_stunned:
                self.__advance(
                    5,
                    "Golpear o amuleto enquanto o Gnomo está atordoado",
                    (512, 285),
                )
        elif self.__step == 5:
            if not self.__boss.is_alive:
                self.__advance(
                    6,
                    "Puxar a Corrente de Ouro para executar a Descarga Suprema",
                    (512, 280),
                )
            elif not self.__boss.is_stunned:
                self.__advance(
                    4,
                    "Sobreviver à fase crítica e aguardar o próximo atordoamento",
                    (512, 285),
                )

    def __update_magic_projectiles(self, delta_time):
        player_bounds = self.player.interaction_bounds
        active = []
        for projectile in self.__magic_projectiles:
            projectile.update(
                delta_time,
                self.__window_width,
                self.__window_height,
            )
            if projectile.is_active:
                px, py, pw, ph = projectile.bounds
                bx, by, bw, bh = player_bounds
                if px < bx + bw and px + pw > bx and py < by + bh and py + ph > by:
                    self.player.take_damage(projectile.damage)
                    projectile.is_active = False
            if projectile.is_active:
                active.append(projectile)
        self.__magic_projectiles = active

    def on_interact(self, interactable):
        if interactable.tag in ("left_valve", "right_valve") and self.__step == 3:
            self.__valves.add(interactable.tag)
            if len(self.__valves) == 1:
                self.__advance(
                    3,
                    "Acionar a outra válvula lateral para romper o escudo",
                    (850, 325),
                )
            else:
                self.__boss.remove_shield()
                self.__advance(
                    4,
                    "Reduzir o HP do Gnomo e sobreviver às rajadas triplas",
                    (512, 285),
                )
        elif interactable.tag == "golden_flush" and self.__step == 6:
            self.hud.set_objective("Gnomo banido. O esgoto e a UFF estão purificados!")
            Audio.stop_music()
            self._request_transition("ending")

    def _draw_additional_effects(self, screen):
        for projectile in self.__magic_projectiles:
            projectile.draw(screen)
