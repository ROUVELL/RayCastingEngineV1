import pygame as pg
from random import randint

import npc
from sprite import StaticSprite, AnimatedSprite
from npc import Soldier, CacoDemon, CyberDemon

from settings import DELETE_DELAY


class SpriteHandler:
    def __init__(self, game):
        self.game = game
        self.sprites = []
        self.npc = []
        self.npc_positions = set()
        self.delete_event = pg.USEREVENT
        self.spawn()

    def on_init(self):
        [sprite.on_init() for sprite in self.sprites]
        [npc.on_init() for npc in self.npc]

        pg.time.set_timer(self.delete_event, DELETE_DELAY, -1)

    def spawn(self):
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # add_sprite(StaticSprite(self.game, 'candlebra.png', (11.5, 4.5)))
        # add_sprite(AnimatedSprite(self.game, 'green_light', (7.5, 7.5)))
        # add_sprite(AnimatedSprite(self.game, 'red_light', (10.5, 5.5)))

        for i in range(20):
            x, y = randint(6, 29) + 0.5, randint(6, 29) + 0.5
            add_npc(Soldier(self.game, (x, y)))
        # add_npc(CacoDemon(self.game, (17.5, 20.5)))
        # add_npc(CyberDemon(self.game, (27.5, 27.5)))

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def add_npc(self, npc):
        self.npc_positions.add(npc.map_pos)
        self.npc.append(npc)

    def clear_level(self):
        self.npc = list(filter(lambda npc: not npc.need_delete, self.npc))
        self.npc_positions = {npc.map_pos for npc in self.npc if npc.alive}

    def process_events(self, event):
        if event.type == self.delete_event:
            self.clear_level()

    def update(self):
        [sprite.update() for sprite in self.sprites]
        [npc.update() for npc in self.npc]

    def draw(self):
        [pg.draw.circle(self.game.sc, 'blue', sprite.level_pos, 6)
         for sprite in self.sprites]
        [pg.draw.circle(self.game.sc, 'red', npc.level_pos, 6)
         for npc in self.npc if npc.alive]
