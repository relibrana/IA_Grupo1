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
BLUE = (0, 0, 255)


# element de la matrix
class WorldTile:
    def __init__(self, _is_wall):
        self.isWall = _is_wall  # casa
        self.isTarget = False
        self.value = 1  # 1 is path, 0 is walled
        self.x_pos = 0
        self.y_pos = 0

    def set_position(self, new_x, new_y):
        self.x_pos = new_x
        self.y_pos = new_y

    def set_wall(self, _is_wall):
        self.isWall = _is_wall

    def set_target(self, is_target):
        self.isTarget = is_target

    def tile_center(self):
        return self.x_pos + (TILE_SIZE / 2), self.y_pos + (TILE_SIZE / 2)

    def draw_tile(self, surface):
        if self.isTarget:
            pg.draw.rect(surface, RED, [self.x_pos, self.y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE], 1)
        elif not self.isWall:
            pg.draw.rect(surface, BLACK, [self.x_pos, self.y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE], 1)


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
                self.matrix[i][j].draw_tile(surface)

    def clicked_tile(self, x, y):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                temp = self.matrix[i][j]
                if temp.x_pos <= x < temp.x_pos + TILE_SIZE \
                        and temp.y_pos - TILE_SIZE <= y < temp.y_pos - TILE_SIZE + TILE_SIZE:
                    return i, j
        return None

    def get_tile(self, x, y):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                temp = self.matrix[i][j]
                if temp.x_pos <= x < temp.x_pos + TILE_SIZE \
                        and temp.y_pos - TILE_SIZE <= y < temp.y_pos - TILE_SIZE + TILE_SIZE:
                    return self.matrix[i][j]
        return None

    def get_tile_by_index(self, x, y):
        return self.matrix[x][y]