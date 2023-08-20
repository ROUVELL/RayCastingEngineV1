#include <math.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    float depth;
    float proj_height;
    uint8_t texture;
    float offset;
} RayResult;


RayResult* allocate(int size) {
    RayResult* array = (RayResult*)malloc(size * sizeof(RayResult));
    return array;
}


void ray_cast(float ox, float oy,
	      float angle, int level_w,
	      int level_h, uint8_t level_map[][level_w],
              RayResult* result_array,
       	      const int NUM_RAYS, const float H_FOV,
	      const float SCREEN_DIST, const float DELTA_ANGLE) {
    int texture_vert, texture_hor;
    int x_map = (int)ox, y_map = (int)oy;
    // RayResult* result = (RayResult*)malloc(NUM_RAYS * sizeof(RayResult));

    float ray_angle = angle - H_FOV + 0.0001;
    for (int ray = 0; ray < NUM_RAYS; ray++) {
	texture_vert = 0;
	texture_hor = 0;

        float sin_a = sin(ray_angle);
        float cos_a = cos(ray_angle);

        // horizontals
        float y_hor, hor_dy;
        if (sin_a > 0) {
            y_hor = y_map + 1;
            hor_dy = 1;
        } else {
            y_hor = y_map - 1e-6;
            hor_dy = -1;
        }

        float depth_hor = (y_hor - oy) / sin_a;
        float x_hor = ox + depth_hor * cos_a;

        float hor_delta_depth = hor_dy / sin_a;
        float hor_dx = hor_delta_depth * cos_a;

        for (int i = 0; i < level_h; i++) {
            int hx = (int)x_hor, hy = (int)y_hor;
	    if (hx >= 0 && hx < level_w && hy >= 0 && hy < level_h) {
                if (level_map[hy][hx]) {
                    texture_hor = level_map[hy][hx];
                    break;
                }
	    }
            x_hor += hor_dx;
            y_hor += hor_dy;
            depth_hor += hor_delta_depth;
        }

        // verticals
        float x_vert, vert_dx;
        if (cos_a > 0) {
            x_vert = x_map + 1;
            vert_dx = 1;
        } else {
            x_vert = x_map - 1e-6;
            vert_dx = -1;
        }

        float depth_vert = (x_vert - ox) / cos_a;
        float y_vert = oy + depth_vert * sin_a;

        float vert_delta_depth = vert_dx / cos_a;
        float vert_dy = vert_delta_depth * sin_a;

        for (int i = 0; i < level_w; i++) {
            int vx = (int)x_vert, vy = (int)y_vert;
	    if (vx >= 0 && vx < level_w && vy >= 0 && vy < level_h) {
                if (level_map[vy][vx]) {
                    texture_vert = level_map[vy][vx];
                    break;
                }
	    }
            x_vert += vert_dx;
            y_vert += vert_dy;
            depth_vert += vert_delta_depth;
        }

        float depth, offset;
        int texture;
        if (depth_vert < depth_hor) {
            depth = depth_vert;
            texture = texture_vert;
            y_vert -= floor(y_vert);
            offset = cos_a > 0 ? y_vert : (1.0 - y_vert);
        } else {
            depth = depth_hor;
            texture = texture_hor;
            x_hor -= floor(x_hor);
            offset = sin_a > 0 ? (1.0 - x_hor) : x_hor;
        }

        depth *= cos(angle - ray_angle);

        float proj_height = SCREEN_DIST / (depth + 0.0001);

        result_array[ray].depth = depth;
        result_array[ray].proj_height = proj_height;
        result_array[ray].texture = texture;
        result_array[ray].offset = offset;

        ray_angle += DELTA_ANGLE;
    }
}