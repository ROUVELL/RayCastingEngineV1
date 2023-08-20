import pygame as pg

from uttils import load_sound, load_music


class Sound:
    def __init__(self):
        self.shot = load_sound('shot.wav')
        self.npc_pain = load_sound('npc_pain.wav')
        self.npc_attack = load_sound('npc_attack.wav')
        self.npc_death = load_sound('npc_death.wav')
        self.player_pain = load_sound('player_pain.wav')

        load_music('theme.mp3')
