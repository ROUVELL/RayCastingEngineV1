import pygame as pg
from collections import deque
from os import listdir

from settings import *


def load_img(path, size=None, alpha=True):
    img = pg.image.load(path)
    img = img.convert_alpha() if alpha else img.convert()
    return img if size is None else pg.transform.scale(img, size)


def load_texture(file_name, size=(TEXTURE_SIZE, TEXTURE_SIZE), alpha=False):
    return load_img(f'{TEXTURES_DIR}/{file_name}', size, alpha)


def load_sprite_img(file_name, size=None, alpha=True):
    return load_img(f'{STATIC_DIR}/{file_name}', size, alpha)


def load_animation(dir_name, size=None, alpha=True):
    path = f'{ANIMATION_DIR}/{dir_name}'
    return deque([load_img(f'{path}/{file_name}', size, alpha) for file_name in listdir(path)])


def load_sound(file_name, volume=DEFAULT_VOLUME):
    sound = pg.mixer.Sound(f'{SOUND_DIR}/{file_name}')
    sound.set_volume(volume)
    return sound


def load_music(file_name, volume=DEFAULT_VOLUME):
    pg.mixer.music.load(f'{SOUND_DIR}/{file_name}')
    pg.mixer.music.set_volume(volume)
