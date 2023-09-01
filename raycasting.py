import pygame as pg
from ctypes import c_int, c_uint8, c_float, Structure, POINTER, CDLL

from uttils import load_texture
from settings import *


class RayCastResult(Structure):
    _fields_ = [
        ('depth', c_float),
        ('proj_height', c_float),
        ('texture', c_uint8),
        ('offset', c_float)
    ]


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.to_render = set()
        self.dist = 1

        self.wall_textures = {i: load_texture(f'{i}.png')
                              for i in range(1, 6)}

        lib = CDLL('./raycasting.so')

        self.raycast_result = (RayCastResult * NUM_RAYS)()

        self.c_ray_cast = lib.ray_cast
        self.c_ray_cast.argtypes = (c_float, c_float, c_float, c_int, c_int, POINTER(POINTER(c_uint8)),
                                    POINTER(RayCastResult), c_int, c_float, c_float, c_float)

    def on_init(self):
        self.player = self.game.player
        self.level = self.game.level_handler

    def get_walls(self):
        self.to_render = set()
        for ray, ray_data in enumerate(self.raycast_result):

            texture_num = ray_data.texture
            if texture_num == 0:
                continue

            proj_height = ray_data.proj_height
            if proj_height < HEIGHT:
                wall_column = self.wall_textures[texture_num].subsurface(
                    ray_data.offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, H_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_H_COEF / proj_height
                wall_column = self.wall_textures[texture_num].subsurface(
                    ray_data.offset * (TEXTURE_SIZE - SCALE), H_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.to_render.add((ray_data.depth, wall_column, wall_pos))

            if ray == H_NUM_RAYS:
                self.dist = ray_data.depth

    # def ray_cast(self):
    #     self.raycast_result = []
    #     texture_vert, texture_hor = 1, 1
    #     ox, oy = self.player.pos
    #     x_map, y_map = self.player.map_pos
    #
    #     ray_angle = self.player.angle - H_FOV + 0.0001
    #     for ray in range(NUM_RAYS):
    #         sin_a = math.sin(ray_angle)
    #         cos_a = math.cos(ray_angle)
    #
    #         # horizontals
    #         y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
    #
    #         depth_hor = (y_hor - oy) / sin_a
    #         x_hor = ox + depth_hor * cos_a
    #
    #         delta_depth = dy / sin_a
    #         dx = delta_depth * cos_a
    #
    #         for i in range(self.level.height):
    #             tile_hor = int(x_hor), int(y_hor)
    #             if value := self.level.map.get(tile_hor):
    #                 texture_hor = value
    #                 break
    #             x_hor += dx
    #             y_hor += dy
    #             depth_hor += delta_depth
    #
    #         # verticals
    #         x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
    #
    #         depth_vert = (x_vert - ox) / cos_a
    #         y_vert = oy + depth_vert * sin_a
    #
    #         delta_depth = dx / cos_a
    #         dy = delta_depth * sin_a
    #
    #         for i in range(self.level.width):
    #             tile_vert = int(x_vert), int(y_vert)
    #             if value := self.level.map.get(tile_vert):
    #                 texture_vert = value
    #                 break
    #             x_vert += dx
    #             y_vert += dy
    #             depth_vert += delta_depth
    #
    #         # depth, texture offset
    #         if depth_vert < depth_hor:
    #             depth, texture = depth_vert, texture_vert
    #             y_vert -= int(y_vert)
    #             offset = y_vert if cos_a > 0 else (1 - y_vert)
    #         else:
    #             depth, texture = depth_hor, texture_hor
    #             x_hor -= int(x_hor)
    #             offset = (1 - x_hor) if sin_a > 0 else x_hor
    #
    #         # remove fishbowl effect
    #         depth *= math.cos(self.player.angle - ray_angle)
    #
    #         proj_height = SCREEN_DIST / (depth + 0.0001)
    #
    #         self.raycast_result.append((depth, proj_height, texture, offset))  # for texturing
    #         # self.raycast_result.append((depth, cos_a, sin_a))                  # for 2d
    #         # self.raycast_result.append(proj_height)                            # for 3d
    #
    #         ray_angle += DELTA_ANGLE

    def fast_ray_cast(self):
        self.c_ray_cast(*self.player.pos,
                        self.player.angle,
                        self.level.width,
                        self.level.height,
                        self.level.array_ptr,
                        self.raycast_result,
                        NUM_RAYS, H_FOV,
                        SCREEN_DIST, DELTA_ANGLE)

    def update(self):
        self.fast_ray_cast()
        self.get_walls()
