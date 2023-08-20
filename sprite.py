import pygame as pg
import math

from uttils import load_sprite_img, load_animation
from settings import *


class SpriteObject:
    def __init__(self, game, pos, scale=1.0, shift=0.0):
        self.game = game
        self.x, self.y = pos
        self.scale = scale
        self.shift = shift
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0.0001, 0, 1, 1
        self.sprite_h_width = 0

        # Every sprite MUST have an image
        self.image = None

    @property
    def level_pos(self):
        return self.x * TILE_SIZE, self.y * TILE_SIZE

    def on_init(self):
        self.player = self.game.player
        self.raycasting = self.game.raycasting

        self.img_width = self.image.get_width()
        self.h_img_width = self.img_width >> 1
        self.image_ratio = self.img_width / self.image.get_height()

    def get_sprite(self):
        self.dx = dx = self.x - self.player.x
        self.dy = dy = self.y - self.player.y
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (H_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.img_width < self.screen_x < (WIDTH + self.img_width) and self.norm_dist > 0.7:
            self.get_projection()

    def get_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.scale
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_h_width = proj_width // 2
        height_shift = proj_height * self.shift
        pos = self.screen_x - self.sprite_h_width, H_HEIGHT - proj_height // 2 + height_shift

        self.raycasting.to_render.add((self.norm_dist, image, pos))


class StaticSprite(SpriteObject):
    def __init__(self, game, file_name, pos, scale=1.0, shift=0.0):
        super().__init__(game, pos, scale, shift)
        self.image = load_sprite_img(file_name)

    def update(self):
        self.get_sprite()


class AnimatedObject:
    def __init__(self, anim_time=100):
        # Every animated sprite MUST have an image and a list of images (animation)
        self.image = None
        self.images = None

        self.anim_time = anim_time
        self.last_animate = 0
        self.animation_trigger = False

    def check_animation_time(self):
        self.animation_trigger = False
        now = pg.time.get_ticks()
        if now - self.last_animate >= self.anim_time:
            self.last_animate = now
            self.animation_trigger = True

    def animate(self):
        if self.animation_trigger:
            self.images.rotate(-1)
            self.image = self.images[0]
            
            
class AdvancedSprite(SpriteObject, AnimatedObject):
    def __init__(self, game, pos, scale=1.0, shift=0.0, anim_time=100):
        SpriteObject.__init__(self, game, pos, scale, shift)
        AnimatedObject.__init__(self, anim_time)


class AnimatedSprite(AdvancedSprite):
    def __init__(self, game, dir_name, pos, scale=1.0, shift=0.0, anim_time=100):
        super().__init__(game, pos, scale, shift, anim_time)
        self.images = load_animation(dir_name)
        self.image = self.images[0]

    def update(self):
        self.check_animation_time()
        self.animate()
        self.get_sprite()

