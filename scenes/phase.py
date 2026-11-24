"""Comportamento compartilhado pelas fases jogáveis."""

from pathlib import Path
import random

import pygame
from pplay.gameimage import GameImage

from objects.attack_hitbox import AttackHitbox
from objects.audio import Audio
from objects.dash import Dash
from objects.hud import Hud
from objects.interactable import Interactable
from objects.interaction_popup import InteractionPopup
from objects.mouse_input import read_mouse
from objects.obstacle import Obstacle
from objects.player import Player
from objects.projectile import Projectile
from objects.yellow_arrow import YellowArrow
from scenes.scene import Scene


class Phase(Scene):
    """Fase base com cenário, colisões e objetos interagíveis."""

    INTERACTION_DISTANCE = 25

    def __init__(
        self,
        window,
        window_width,
        window_height,
        background_asset,
        overlay_asset,
        obstacles_asset,
        interactables_asset,
        stage_name=Hud.DEFAULT_STAGE_NAME,
        objective=Hud.DEFAULT_OBJECTIVE,
        player=None,
        fallback_background_color=(18, 24, 29),
    ):
        super().__init__(window)

        project_root = Path(__file__).resolve().parents[1]
        self.__background = None
        source_width = 1697
        source_height = 927
        self.__fallback_background_color = fallback_background_color
        if background_asset is not None:
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

        self.__overlay = None
        if overlay_asset is not None:
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

        if player is not None:
            self.__player = player
        else:
            player_x = 100
            player_y = 200
            self.__player = Player(player_x, player_y)

        self.__movement_input = (0, 0)
        self.__interaction_popup = InteractionPopup()
        self.__interaction_key_was_pressed = False
        self.__mouse_was_pressed = False
        self.__interaction_requested = False
        self.__current_nearby_interactable = None
        self.__yellow_arrow = YellowArrow()
        self.__hud = Hud(
            self.window,
            self.__player,
            stage_name,
            objective,
        )
        if self.__player.ammo > 0:
            self.__hud.set_ammo(self.__player.ammo)

        # Mecânicas de combate e esquiva
        self.__dash = Dash()
        self.__attack_hitbox = AttackHitbox()
        self.__attack_key_was_pressed = False
        self.__dash_key_was_pressed = False
        self.__right_mouse_was_pressed = False
        self.__f_key_was_pressed = False

        # Projéteis de Papel Higiênico (BLD-06)
        self.__projectiles = []

        # Habilidade Descarga e Screen Shake (BLD-07 / GDD 6)
        self.__descarga_cooldown = 3.0
        self.__descarga_cooldown_timer = 0.0
        self.__screen_shake_timer = 0.0
        self.__screen_shake_intensity = 0
        self.__q_key_was_pressed = False

        # Lista de inimigos — populada pelas subclasses via _add_enemy()
        self.__enemies = []

    @property
    def yellow_arrow(self):
        """Seta amarela que aponta dinamicamente para o próximo objetivo."""
        return self.__yellow_arrow

    @property
    def hud(self):
        """HUD da fase com informações de vida e dados da run."""
        return self.__hud

    @property
    def player(self):
        """Instância do jogador ativo na fase."""
        return self.__player

    @property
    def enemies(self):
        """Lista de inimigos ativos na fase."""
        return self.__enemies

    @property
    def projectiles(self):
        """Lista de projéteis de papel higiênico ativos na fase."""
        return self.__projectiles

    @property
    def ammo(self):
        """Quantidade atual de munição de papel higiênico."""
        return self.__player.ammo

    def add_ammo(self, amount):
        """Adiciona munição de papel higiênico e atualiza o HUD."""
        self.__player.add_ammo(amount)
        self.__hud.set_ammo(self.__player.ammo)

    def shoot_projectile(self, target_x, target_y):
        """Dispara um projétil de papel higiênico em direção a (target_x, target_y)."""
        if self.__player.ammo <= 0:
            return None
        self.__player.set_ammo(self.__player.ammo - 1)
        self.__hud.set_ammo(self.__player.ammo)
        origin_x = self.__player.x + self.__player.FRAME_WIDTH / 2
        origin_y = self.__player.y + self.__player.FRAME_HEIGHT / 2
        proj = Projectile(
            origin_x,
            origin_y,
            target_x,
            target_y,
            damage=self.__player.projectile_damage,
        )
        self.__projectiles.append(proj)
        Audio.play_effect("disparo.mp3")
        return proj

    def increase_projectile_damage(self, amount):
        """Aplica um bônus temporário ao dano dos próximos projéteis da run."""
        return self.__player.increase_projectile_damage(amount)

    @property
    def descarga_ready(self):
        """Indica se a habilidade Descarga está pronta para uso."""
        return self.__descarga_cooldown_timer <= 0.0

    def trigger_descarga(self):
        """Habilidade Descarga (AoE de repulsão + dano leve + Screen Shake)."""
        if not self.descarga_ready:
            return False

        self.__descarga_cooldown_timer = self.__descarga_cooldown
        self.__screen_shake_timer = 0.4
        self.__screen_shake_intensity = 6
        Audio.play_effect("toilet-flush.mp3")

        player_cx = self.__player.x + self.__player.FRAME_WIDTH / 2
        player_cy = self.__player.y + self.__player.FRAME_HEIGHT / 2
        repel_radius = 220.0
        push_distance = 150.0

        for enemy in self.__enemies:
            if not enemy.is_alive:
                continue
            ex, ey, ew, eh = enemy.bounds
            ecx = ex + ew / 2
            ecy = ey + eh / 2
            dx = ecx - player_cx
            dy = ecy - player_cy
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if 0 < dist <= repel_radius:
                nx = dx / dist
                ny = dy / dist
                enemy._set_position(enemy.x + nx * push_distance, enemy.y + ny * push_distance)
                enemy.take_damage(5)

        return True

    def _add_enemy(self, enemy):
        """Registra um inimigo na lista de entidades ativas da fase."""
        self.__enemies.append(enemy)

    def _add_obstacle(self, obstacle):
        """Adiciona um obstáculo dinâmico à colisão da fase."""
        self.__obstacles.append(obstacle)

    def _remove_obstacle(self, obstacle):
        """Remove um obstáculo dinâmico já ultrapassado pelo jogador."""
        if obstacle in self.__obstacles:
            self.__obstacles.remove(obstacle)

    def _replace_map_assets(self, background_asset, obstacles_asset, interactables_asset):
        """Troca cenário, colisões e pontos de interação dentro da mesma fase."""
        project_root = Path(__file__).resolve().parents[1]
        background_path = project_root / background_asset
        background = GameImage(str(background_path))
        source_width, source_height = background.width, background.height
        window_width = self.window.width
        window_height = self.window.height
        background.image = pygame.transform.scale(
            background.image, (window_width, window_height)
        )
        background.width = window_width
        background.height = window_height
        self.__background = background

        scale_x = window_width / source_width
        scale_y = window_height / source_height
        self.__obstacles = self.__load_rectangles(
            project_root / obstacles_asset, scale_x, scale_y, Obstacle
        )
        self.__interactables = self.__load_rectangles(
            project_root / interactables_asset, scale_x, scale_y, Interactable
        )
        self.__enemies.clear()
        self.__projectiles.clear()
        self.__current_nearby_interactable = None
        self.__interaction_popup.hide()

    def _add_interactable(self, interactable):
        """Adiciona um objeto interativo criado durante a fase."""
        self.__interactables.append(interactable)

    def process_input(self):
        mouse_position, mouse_buttons = read_mouse(self.window)
        keyboard = self.window.keyboard
        moving_left = keyboard.key_pressed("LEFT") or keyboard.key_pressed("A")
        moving_right = keyboard.key_pressed("RIGHT") or keyboard.key_pressed("D")
        moving_up = keyboard.key_pressed("UP") or keyboard.key_pressed("W")
        moving_down = keyboard.key_pressed("DOWN") or keyboard.key_pressed("S")

        horizontal_input = int(moving_right) - int(moving_left)
        vertical_input = int(moving_down) - int(moving_up)
        self.__movement_input = (horizontal_input, vertical_input)

        # ----- Dash (Espaço) — edge-trigger -----
        space_pressed = keyboard.key_pressed("SPACE")
        space_triggered = space_pressed and not self.__dash_key_was_pressed
        self.__dash_key_was_pressed = space_pressed
        if space_triggered:
            dx = float(horizontal_input)
            dy = float(vertical_input)
            # Dash na direção atual; se parado, usa a última direção do olhar
            if dx == 0 and dy == 0:
                _fallback = {
                    "right": (1, 0), "left": (-1, 0),
                    "up": (0, -1), "down": (0, 1),
                    "up_right": (1, -1), "up_left": (-1, -1),
                    "down_right": (1, 1), "down_left": (-1, 1),
                }
                dx, dy = _fallback.get(self.__player.facing_direction, (1, 0))
            self.__dash.try_start(dx, dy)

        # ----- Interação (E) — edge-trigger -----
        interaction_key_pressed = keyboard.key_pressed("E")
        key_triggered = (
            interaction_key_pressed and not self.__interaction_key_was_pressed
        )
        self.__interaction_key_was_pressed = interaction_key_pressed

        # ----- Mouse -----
        mouse_pressed = bool(mouse_buttons[0]) if mouse_buttons else False
        mouse_clicked = mouse_pressed and not self.__mouse_was_pressed
        self.__mouse_was_pressed = mouse_pressed

        popup_clicked = False
        if mouse_clicked and self.__interaction_popup.is_visible:
            if self.__interaction_popup.is_mouse_over(mouse_position):
                popup_clicked = True
            elif self.__current_nearby_interactable is not None:
                obj = self.__current_nearby_interactable
                if (
                    obj.x <= mouse_position[0] <= obj.x + obj.width
                    and obj.y <= mouse_position[1] <= obj.y + obj.height
                ):
                    popup_clicked = True

        self.__interaction_requested = key_triggered or popup_clicked

        # ----- Ataque (clique esquerdo sem popup) — CTL-03 / BLD-05 -----
        if mouse_clicked and not popup_clicked:
            if self.__player.has_plunger:
                attack_started = self.__attack_hitbox.try_attack(
                    self.__player.x,
                    self.__player.y,
                    self.__player.FRAME_WIDTH,
                    self.__player.FRAME_HEIGHT,
                    self.__player.facing_direction,
                )
                if attack_started:
                    Audio.play_effect("porrada_desentupidor_classica.wav")

        # ----- Disparo à Distância (Botão Direito do Mouse ou F) — BLD-06 -----
        right_pressed = len(mouse_buttons) >= 3 and bool(mouse_buttons[2])
        right_clicked = right_pressed and not self.__right_mouse_was_pressed
        self.__right_mouse_was_pressed = right_pressed

        f_pressed = keyboard.key_pressed("F")
        f_triggered = f_pressed and not self.__f_key_was_pressed
        self.__f_key_was_pressed = f_pressed

        if (right_clicked or f_triggered) and self.__player.ammo > 0:
            self.shoot_projectile(mouse_position[0], mouse_position[1])

        # ----- Habilidade Descarga (Tecla Q) — BLD-07 -----
        q_pressed = keyboard.key_pressed("Q")
        q_triggered = q_pressed and not self.__q_key_was_pressed
        self.__q_key_was_pressed = q_pressed
        if q_triggered:
            self.trigger_descarga()

    def on_door_interacted(self):
        """Disparado ao interagir com a porta que conduz ao próximo cômodo."""
        self._request_transition("phase2")

    def on_interact(self, interactable):
        """Executa a ação correspondente ao objeto interagível acionado."""
        if interactable.tag == "door" or interactable.x > 800:
            self.on_door_interacted()
        else:
            target_y = 280 if self.__player.y > 370 else 380
            self.__player.teleport_to(120, target_y)

    def update(self, delta_time):
        # ----- Dash -----
        self.__dash.update(delta_time)
        if self.__dash.is_active:
            dx, dy = self.__dash.direction
            # Durante o dash, usa direção fixa e velocidade multiplicada
            self.__player.set_invulnerable(Dash.INVULNERABILITY)
            self.__player.update(
                dx * self.__dash.speed_multiplier,
                dy * self.__dash.speed_multiplier,
                delta_time,
                self.__obstacles,
            )
        else:
            self.__player.update(
                self.__movement_input[0],
                self.__movement_input[1],
                delta_time,
                self.__obstacles,
            )

        # ----- Ataque -----
        self.__attack_hitbox.update(delta_time)
        if self.__attack_hitbox.check_hits(self.__enemies):
            Audio.play_effect("enemy_hit.mp3")

        # ----- Inimigos -----
        player_center_x = self.__player.x + self.__player.FRAME_WIDTH / 2
        player_center_y = self.__player.y + self.__player.FRAME_HEIGHT / 2
        alive_enemies = []
        for enemy in self.__enemies:
            enemy.update(player_center_x, player_center_y, delta_time,
                         self.__obstacles)
            # Contato físico — dano ao jogador
            if enemy.is_alive:
                ex, ey, ew, eh = enemy.bounds
                px, py, pw, ph = self.__player.interaction_bounds
                if ex < px + pw and ex + ew > px and ey < py + ph and ey + eh > py:
                    self.__player.take_damage(enemy.contact_damage)
                if hasattr(enemy, "check_aura_damage") and enemy.check_aura_damage(player_center_x, player_center_y):
                    self.__player.take_damage(enemy.AURA_DAMAGE)
                alive_enemies.append(enemy)
        self.__enemies = alive_enemies

        # ----- Projéteis -----
        active_projectiles = []
        for proj in self.__projectiles:
            proj.update(delta_time, self.__obstacles)
            if proj.check_hit(self.__enemies):
                Audio.play_effect("enemy_hit.mp3")
            if proj.is_active:
                active_projectiles.append(proj)
        self.__projectiles = active_projectiles

        # ----- HUD e seta -----
        self.__hud.update(delta_time)
        self.__yellow_arrow.update(
            self.__player.x + 45,
            self.__player.y + 50,
            delta_time,
        )

        # Timers da Descarga e Screen Shake
        if self.__descarga_cooldown_timer > 0:
            self.__descarga_cooldown_timer = max(
                0.0, self.__descarga_cooldown_timer - delta_time
            )
        if self.__screen_shake_timer > 0:
            self.__screen_shake_timer = max(
                0.0, self.__screen_shake_timer - delta_time
            )

        self.__current_nearby_interactable = self.__find_nearest_interactable()
        nearby_interactable = self.__current_nearby_interactable

        if self.__interaction_requested and nearby_interactable is not None:
            self.on_interact(nearby_interactable)
            self.__current_nearby_interactable = self.__find_nearest_interactable()
            nearby_interactable = self.__current_nearby_interactable

        self.__interaction_requested = False
        if nearby_interactable is None:
            self.__interaction_popup.hide()
            return

        center_x, top_y = nearby_interactable.popup_position
        self.__interaction_popup.show_above(center_x, top_y)

    def draw(self):
        super().draw()
        if self.__background is None:
            self.window.screen.fill(self.__fallback_background_color)
        else:
            self.__background.draw()

        if self.__player.y < 370:
            self.__player.draw()
            if self.__overlay is not None:
                self.__overlay.draw()
        else:
            if self.__overlay is not None:
                self.__overlay.draw()
            self.__player.draw()

        # Desenha inimigos sobre o cenário
        for enemy in self.__enemies:
            enemy.draw()

        # Desenha projéteis sobre o cenário
        for proj in self.__projectiles:
            proj.draw(self.window.screen)

        self.__attack_hitbox.draw(self.window.screen)
        self.__interaction_popup.draw()
        self.__yellow_arrow.draw(self.window.screen)

        # Efeito Screen Shake da Descarga (vibração na câmera)
        if self.__screen_shake_timer > 0:
            shake_x = random.randint(
                -self.__screen_shake_intensity, self.__screen_shake_intensity
            )
            shake_y = random.randint(
                -self.__screen_shake_intensity, self.__screen_shake_intensity
            )
            self.window.screen.scroll(shake_x, shake_y)

        self._draw_additional_effects(self.window.screen)
        self.__hud.draw()

    def _draw_additional_effects(self, screen):
        """Ponto de extensão para efeitos específicos de uma fase."""
        pass

    @staticmethod
    def __load_rectangles(rectangles_path, scale_x, scale_y, rectangle_class):
        rectangles = []

        with rectangles_path.open("r", encoding="utf-8") as rectangle_file:
            for line_number, line in enumerate(rectangle_file, start=1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue

                parts = [part.strip() for part in clean_line.split(",")]
                if len(parts) not in (4, 5):
                    raise ValueError(
                        f"A linha {line_number} de {rectangles_path} "
                        "deve conter quatro ou cinco campos"
                    )

                try:
                    coordinates = [int(parts[i]) for i in range(4)]
                except ValueError as error:
                    raise ValueError(
                        f"Coordenada inválida na linha {line_number} de "
                        f"{rectangles_path}"
                    ) from error

                start_x, start_y, end_x, end_y = coordinates
                tag = parts[4] if len(parts) == 5 else "default"

                if rectangle_class is Interactable:
                    rectangles.append(
                        Interactable(
                            round(start_x * scale_x),
                            round(start_y * scale_y),
                            round(end_x * scale_x),
                            round(end_y * scale_y),
                            tag=tag,
                        )
                    )
                else:
                    rectangles.append(
                        rectangle_class(
                            round(start_x * scale_x),
                            round(start_y * scale_y),
                            round(end_x * scale_x),
                            round(end_y * scale_y),
                        )
                    )

        return rectangles

    def _can_interact_with(self, interactable):
        """Define se um determinado objeto pode ser interagido na etapa atual."""
        return True

    def _find_nearest_interactable(self):
        """Retorna o objeto interagível mais próximo do alcance de Privadus."""
        return self.__find_nearest_interactable()

    def __find_nearest_interactable(self):
        player_bounds = self.__player.interaction_bounds
        nearby_interactables = (
            (
                interactable.distance_to(player_bounds),
                interactable,
            )
            for interactable in self.__interactables
            if self._can_interact_with(interactable)
        )
        nearby = [
            (distance, interactable)
            for distance, interactable in nearby_interactables
            if distance <= self.INTERACTION_DISTANCE
        ]
        if not nearby:
            return None

        return min(nearby, key=lambda candidate: candidate[0])[1]
