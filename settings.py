import math
import numpy as np
from os.path import dirname

# screen
SCREEN = WIDTH, HEIGHT = 1920, 1080
# SCREEN = WIDTH, HEIGHT = 1400, 900
CENTER = H_WIDTH, H_HEIGHT = WIDTH >> 1, HEIGHT >> 1

# fps
FPS = 60

# tile
TILE_SIZE = 20

# level
_ = 0
# test_level = np.zeros((HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE), dtype=np.uint8)
# test_level[0, :] = 1
# test_level[-1, :] = 1
# test_level[:, 0] = 1
# test_level[:, -1] = 1
test_level = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, 2, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, 3, 3, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, 1],
    [1, _, 1, 1, 1, _, _, _, _, _, 3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 5, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, 2, _, _, _, 4, _, _, _, _, _, _, 5, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 3, _, _, _, _, _, _, 2, _, _, _, _, _, 4, _, _, _, _, 5, _, 5, 5, 5, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 2, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, 1, _, _, _, _, _, 2, _, _, _, _, _, 4, _, 4, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, 2, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, 1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 4, _, 4, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 2, 2, _, _, _, _, _, _, _, _, 1, 1, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, 1],
    [1, _, _, 2, 1, 1, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 5, _, _, _, 2, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, _, _, 1, 1, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, _, _, _, _, _, 5, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.uint8)

# player
PLAYER_POS = 1.5, 5.5
PLAYER_SPEED = 0.003
PLAYER_SIZE = 70  # for collision
PLAYER_MAX_HEALTH = 100

# raycasting
FOV = math.pi / 3
H_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
H_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
SCREEN_DIST = H_WIDTH / math.tan(H_FOV)
SCALE = WIDTH // NUM_RAYS

# textures
TEXTURE_SIZE = 512
H_TEXTURE_SIZE = TEXTURE_SIZE // 2
TEXTURE_H_COEF = TEXTURE_SIZE * HEIGHT

# sound
DEFAULT_VOLUME = 0.4

# mouse
MOUSE_SENSETIVITY = 0.0001

# colors
BG = (20, 20, 20)
FPS_COLOR = 'orange'
FLOOR_COLOR = (30, 30, 30)

# paths
ROOT = dirname(__file__)
RES_DIR = f'{ROOT}/res'
TEXTURES_DIR = f'{RES_DIR}/textures'
STATIC_DIR = f'{RES_DIR}/static'
ANIMATION_DIR = f'{RES_DIR}/animation'
SOUND_DIR = f'{RES_DIR}/sounds'

# other
DIAG_SPEED_CORR = 1 / math.sqrt(2)
DELETE_DELAY = 8000  # 8 sec
