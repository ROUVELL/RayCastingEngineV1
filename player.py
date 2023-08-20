import pygame as pg
import math

from weapon import Weapon
from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.speed = PLAYER_SPEED
        self.angle = 0
        self.rel = 0

        self.sin_a = 0.0
        self.cos_a = 0.0

        self.weapon = Weapon(self)
        self.health = PLAYER_MAX_HEALTH
        self.injured = False
        self.shoting = False

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    @property
    def level_pos(self):
        return self.x * TILE_SIZE, self.y * TILE_SIZE


    def on_init(self):
        self.level = self.game.level_handler
        self.sound = self.game.sound

    def get_damage(self, damage):
        self.health -= damage
        self.sound.player_pain.play()
        self.injured = True

    def check_wall_collision(self, dx, dy):

        scale = PLAYER_SIZE / self.game.dt
        if not self.level.is_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if not self.level.is_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def movement(self):
        dx, dy = 0, 0
        speed = self.speed * self.game.dt
        speed_sin = speed * self.sin_a
        speed_cos = speed * self.cos_a

        pressed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            pressed += 1
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            pressed += 1
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            pressed += 1
            dx -= speed_sin
            dy += speed_cos

        # diagonal speed correction
        if pressed > 1:
            dx *= DIAG_SPEED_CORR
            dy *= DIAG_SPEED_CORR

        self.check_wall_collision(dx, dy)

    def rotation(self):
        self.rel = pg.mouse.get_rel()[0]
        self.angle += self.rel * MOUSE_SENSETIVITY * self.game.dt
        self.angle %= math.tau

        self.sin_a = math.sin(self.angle)
        self.cos_a = math.cos(self.angle)

    def process_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shoting and not self.weapon.reloading:
                self.sound.shot.play()
                self.shoting = True
                self.weapon.reloading = True
            if event.button == 3:
                dist = self.game.raycasting.dist + 0.1
                x, y = int(self.x + self.cos_a * dist), int(self.y + self.sin_a * dist)
                self.level.delete_wall(x, y)

    def update(self):
        self.injured = False
        self.rotation()
        self.movement()
        self.weapon.update()

    # 2d
    def draw(self):
        x, y = self.level_pos
        l = self.game.raycasting.dist * TILE_SIZE
        pg.draw.line(self.game.sc, 'yellow', (x, y),
                     (x + l * self.cos_a, y + l * self.sin_a))
        pg.draw.circle(self.game.sc, 'green', (x, y), 6)

        # mx, my = self.map_pos
        # x, y = mx * TILE_SIZE, my * TILE_SIZE
        # pg.draw.rect(self.game.sc, 'red', (x, y, TILE_SIZE, TILE_SIZE), 1)
