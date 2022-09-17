import pygame as pg
import pygame.display as display
import pickle

WIDTH = 993
TILE_SIZE = 18
HEIGHT = 804
BG_COLOR = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# element de la matrix
class WorldTile:
    def __init__(self, _is_wall):
        self.isWall = _is_wall  # casa
        self.value = 1  # 1 is path, 0 is walled
        self.x_pos = 0
        self.y_pos = 0

    def set_position(self, new_x, new_y):
        self.x_pos = new_x
        self.y_pos = new_y

    def set_wall(self, _is_wall):
        self.isWall = _is_wall

    def tile_center(self):
        return self.x_pos + (TILE_SIZE / 2), self.y_pos + (TILE_SIZE / 2)


# Matrix
class World:
    def __init__(self, width, height):
        self.matrix = None
        self.width = width
        self.height = height

    def create_world(self):
        self.matrix = [[WorldTile(False) for x in range(self.width)] for y in range(self.height)]
        for col in range(len(self.matrix)):
            for row in range(len(self.matrix[col])):
                self.matrix[col][row].set_position(col * TILE_SIZE, row * TILE_SIZE)

    def load_map_tile(self):
        with open('world_data.txt') as f:
            self.matrix = []
            r = -1
            for line in f:
                c = -1
                t = []
                r += 1
                for x in line.split():
                    c += 1
                    tile = WorldTile(int(x) != 1)
                    tile.set_position(c * TILE_SIZE, r * TILE_SIZE)
                    t.append(tile)
                self.matrix.append(t)

    def draw_world(self, surface):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j].isWall:
                    pg.draw.rect(surface, LIGHT_GREY,
                                 [self.matrix[i][j].x_pos, self.matrix[i][j].y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE], 1)
                else:
                    pg.draw.rect(surface, BLACK,
                                 [self.matrix[i][j].x_pos, self.matrix[i][j].y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE], 1)

    def clicked_tile(self, event):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                temp = self.matrix[i][j]
                if temp.x_pos <= event.pos[0] < temp.x_pos + TILE_SIZE \
                        and temp.y_pos - TILE_SIZE <= event.pos[1] < temp.y_pos - TILE_SIZE + TILE_SIZE:
                    return i, j
        return None
        # temp.set_wall(True)
