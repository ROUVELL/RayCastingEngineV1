import math
from random import randint, random, choice

from sprite import AdvancedSprite
from uttils import load_animation
from settings import *


class NPC(AdvancedSprite):
    def __init__(self, game, root_dir_name, pos, scale=1.0, shift=0.0, anim_time=180):
        super().__init__(game, pos, scale, shift, anim_time)

        path = f'npc/{root_dir_name}'
        self.attack_images = load_animation(f'{path}/attack')
        self.death_images = load_animation(f'{path}/death')
        self.idle_images = load_animation(f'{path}/idle')
        self.pain_images = load_animation(f'{path}/pain')
        self.walk_images = load_animation(f'{path}/walk')
        self.images = self.idle_images
        self.image = self.images[0]
        self.frame = 0

        self.attack_dist = 1
        self.speed = 0.03
        self.size = 50
        self.health = 1
        self.damage = 0
        self.accuracy = 0

        self.alive = True
        self.pain = False
        self.need_delete = False
        self.raycast_value = False
        self.player_search_trigger = False

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def on_init(self):
        super().on_init()
        self.sound = self.game.sound
        self.level = self.game.level_handler
        self.path_finder = self.game.path_finder
        self.sprite_handler = self.game.sprite_handler

    def animate_attack(self):
        self.images = self.attack_images
        if self.animation_trigger:
            self.sound.npc_attack.play()
            if random() < self.accuracy:
                self.player.get_damage(self.damage)

    def animate_pain(self):
        self.images = self.pain_images
        if self.animation_trigger:
            self.pain = False

    def animate_death(self):
        self.images = self.death_images
        if self.animation_trigger:
            if self.frame < len(self.death_images) - 2:
                self.frame += 1
            else:
                self.need_delete = True

    def check_health(self):
        if self.health <= 0:
            self.sound.npc_death.play()
            self.alive = False

    def check_hit(self):
        if self.player.shoting and self.raycast_value:
            if H_WIDTH - self.sprite_h_width < self.screen_x < H_WIDTH + self.sprite_h_width:
                self.game.sound.npc_pain.play()
                self.game.player.shoting = False
                self.pain = True
                self.health -= self.player.weapon.damage
                self.check_health()

    def movement(self):
        self.images = self.walk_images

        next_x, next_y = self.path_finder.get_path(self.map_pos, self.player.map_pos)
        if (next_x, next_y) not in self.sprite_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def check_wall_collision(self, dx, dy):
        is_wall = self.level.is_wall

        if not is_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if not is_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def ray_cast_player_npc(self):
        if self.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.player.pos
        x_map, y_map = self.player.map_pos

        sin_a = math.sin(self.theta)
        cos_a = math.cos(self.theta)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(self.level.height):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.level.map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(self.level.height):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.level.map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            self.player_search_trigger = True
            return True
        return False

    def run_logic(self):
        if self.alive:
            self.raycast_value = self.ray_cast_player_npc()
            self.check_hit()

            if self.pain:
                self.animate_pain()
            elif self.raycast_value:
                if self.dist <= self.attack_dist:
                    self.animate_attack()
                else:
                    self.movement()
            elif self.player_search_trigger:
                self.movement()
            else:
                self.images = self.idle_images

        else:
            self.anim_time = 40
            self.animate_death()

    def update(self):
        if not self.need_delete:
            self.check_animation_time()
            self.run_logic()
            self.animate()
        self.get_sprite()


class Soldier(NPC):
    def __init__(self, game, pos, scale=0.7, shift=0.38, anim_time=180):
        super().__init__(game, 'soldier', pos, scale, shift, anim_time)
        self.attack_dist = randint(3, 6)
        self.health = 100
        self.damage = 10
        self.accuracy = 0.18


class CacoDemon(NPC):
    def __init__(self, game, pos, scale=0.7, shift=0.27, anim_time=250):
        super().__init__(game, 'caco_demon', pos, scale, shift, anim_time)
        self.attack_dist = 2
        self.health = 150
        self.damage = 25
        self.accuracy = 0.35


class CyberDemon(NPC):
    def __init__(self, game, pos, scale=1.0, shift=0.04, anim_time=210):
        super().__init__(game, 'cyber_demon', pos, scale, shift, anim_time)
        self.attack_dist = 6
        self.health = 350
        self.damage = 15
        self.accuracy = 0.25
