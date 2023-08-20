import pygame as pg
import sys

from sprite_handler import SpriteHandler
from level_handler import LevelHandler
from path_finding import PathFinding
from raycasting import RayCasting
from renderer import Renderer
from player import Player
from sound import Sound
from settings import *


class Game:
    def __init__(self):
        pg.display.init()
        pg.mixer.init()
        pg.font.init()

        pg.event.clear()
        pg.event.set_blocked(None)
        pg.event.set_allowed([pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.USEREVENT])
        self.sc = pg.display.set_mode(SCREEN)
        self.clock = pg.time.Clock()
        self.dt = 1

        self.sprite_handler = SpriteHandler(self)
        self.level_handler = LevelHandler(self)
        self.path_finder = PathFinding(self)
        self.raycasting = RayCasting(self)
        self.render = Renderer(self)
        self.player = Player(self)
        self.sound = Sound()

        self.cursor_state = True

        self.on_init()

    def on_init(self):
        self.sprite_handler.on_init()
        self.level_handler.on_init()
        self.path_finder.on_init()
        self.raycasting.on_init()
        self.player.on_init()
        self.render.on_init()

    def new_game(self):
        # pg.mixer.music.play(-1)
        self.set_cursor_state(False)
        self.running = True

    def set_cursor_state(self, state: bool):
        pg.event.set_grab(not state)
        pg.mouse.set_visible(state)
        self.cursor_state = state

    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_F1:
                    self.set_cursor_state(not self.cursor_state)

            self.player.process_events(event)
            self.sprite_handler.process_events(event)

    def update(self):
        self.dt = self.clock.tick(FPS)
        self.player.update()
        self.raycasting.update()
        self.sprite_handler.update()
        self.player.shoting = False

    def run(self):
        self.new_game()
        while self.running:
            self.process_events()
            self.update()
            self.render.all()
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
