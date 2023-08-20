import pygame as pg
from ctypes import POINTER, c_uint8

from settings import *


class LevelHandler:
    def __init__(self, game):
        self.game = game
        self.map = dict()
        self.width = 0
        self.height = 0

        self.get_map(test_level)

    def on_init(self):
        pass

    def get_map(self, level):
        self.width = len(level[0])
        self.height = len(level)
        self.array = level
        self.map.clear()

        self.array_ptr = test_level.ctypes.data_as(POINTER(POINTER(c_uint8)))

        for j, row in enumerate(level):
            for i, value in enumerate(row):
                if value:
                    self.map[(i, j)] = value

    def is_wall(self, x, y):
        return (x, y) in self.map

    # 2d
    def draw(self):
        [pg.draw.rect(self.game.sc, 'gray',
                      (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
         for i, j in self.map]
