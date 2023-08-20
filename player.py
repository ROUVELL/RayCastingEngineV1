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
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = self.speed * self.game.dt
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

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

    def process_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shoting and not self.weapon.reloading:
                self.sound.shot.play()
                self.shoting = True
                self.weapon.reloading = True

    def update(self):
        self.injured = False
        self.movement()
        self.rotation()
        self.weapon.update()

    # 2d
    def draw(self):
        x, y = self.level_pos
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        pg.draw.line(self.game.sc, 'yellow', (x, y),
                     (x + WIDTH * cos_a, y + WIDTH * sin_a))
        pg.draw.circle(self.game.sc, 'green', (x, y), 8)

        mx, my = self.map_pos
        x, y = mx * TILE_SIZE, my * TILE_SIZE
        pg.draw.rect(self.game.sc, 'red', (x, y, TILE_SIZE, TILE_SIZE), 1)
