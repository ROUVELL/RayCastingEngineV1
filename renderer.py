import pygame as pg
from math import degrees as to_degrees

from uttils import load_texture
from settings import *


class Renderer:
    def __init__(self, game):
        self.game = game
        self.sc = game.sc

        self.sky = load_texture('sky.png', (WIDTH, H_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = load_texture('blood_screen.png', SCREEN, alpha=True)

        self.font = pg.font.SysFont('calibri', 24)

    def on_init(self):
        self.raycasting = self.game.raycasting
        self.player = self.game.player
        self.level = self.game.level_handler

        self.get_fps = self.game.clock.get_fps

    def bg(self):
        self.sky_offset = (self.sky_offset + (self.player.rel * 3)) % WIDTH
        self.sc.blit(self.sky, (-self.sky_offset, 0))
        self.sc.blit(self.sky, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.sc, FLOOR_COLOR, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def objects(self):
        objects = sorted(self.raycasting.to_render, key=lambda t: t[0], reverse=True)
        for _, img, pos in objects:
            self.sc.blit(img, pos)

    def player_damage(self):
        if self.player.injured:
            self.sc.blit(self.blood_screen, (0, 0))

    def get_render(self, text):
        return self.font.render(text, True, FPS_COLOR)

    def fps(self):
        render = self.get_render(f'{self.get_fps():.1f}')
        self.sc.blit(render, (0, 0))

    def debug_info(self):
        pos = self.get_render(f'{self.player.map_pos}')
        angle = self.get_render(f'{self.player.angle : .2f}')

        self.sc.blit(pos, (0, 50))
        self.sc.blit(angle, (0, 80))

    def all(self):
        self.bg()
        self.objects()
        self.player.weapon.draw()
        self.player_damage()
        self.level.draw()
        self.player.draw()
        self.game.sprite_handler.draw()
        self.fps()
        self.debug_info()
        pg.display.flip()
