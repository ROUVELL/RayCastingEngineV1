import pygame as pg
from collections import deque

from sprite import AnimatedObject
from uttils import load_animation
from settings import *


class Weapon(AnimatedObject):
    def __init__(self, owner, dir_name='weapon', scale=0.4, anim_time=90):
        super().__init__(anim_time)
        self.game = owner.game
        self.owner = owner

        self.images = deque([
            pg.transform.smoothscale(img, (img.get_width() * scale, img.get_height() * scale))
            for img in load_animation(dir_name)
        ])
        self.image = self.images[0]
        self.num_images = len(self.images)
        self.frame = 0

        self.position = (H_WIDTH - self.image.get_width() // 2, HEIGHT - self.image.get_height())
        self.damage = 50
        self.reloading = False

    def animate(self):
        if self.reloading:
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame += 1
                if self.frame == self.num_images:
                    self.reloading = False
                    self.frame = 0

    def draw(self):
        self.game.sc.blit(self.image, self.position)

    def update(self):
        self.check_animation_time()
        self.animate()
