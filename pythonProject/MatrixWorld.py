import pygame as pg
import pygame.display as display
import pickle

# pre established variables for this script
WIDTH = 993
TILE_SIZE = 18
HEIGHT = 804
BG_COLOR = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


# matrix element class
class WorldTile:
    def __init__(self, _is_wall):
        self.isWall = _is_wall  # casa
        self.isTarget = False
        self.value = 1  # 1 is path, 0 is walled
        self.x_pos = 0
        self.y_pos = 0

    # function to set a new position
    def set_position(self, new_x, new_y):
        self.x_pos = new_x
        self.y_pos = new_y

    # function to set whether a tile should be a wall or not
    def set_wall(self, _is_wall):
        self.isWall = _is_wall

    # function to set whether a tile should be a target, just for visual purposes
    def set_target(self, is_target):
        self.isTarget = is_target

    # function to return the center of a tile, in pixels
    def tile_center(self):
        return self.x_pos + (TILE_SIZE / 2), self.y_pos + (TILE_SIZE / 2)

    # function to allow each tile to draw itself, but will mostly be called from the matrix class
    def draw_tile(self, surface):
        if self.isTarget:
            pg.draw.rect(surface, RED, [self.x_pos, self.y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE])
        elif not self.isWall:
            pg.draw.rect(surface, BLACK, [self.x_pos, self.y_pos - TILE_SIZE, TILE_SIZE, TILE_SIZE], 3)


# Matrix
class World:
    def __init__(self, width, height):
        self.matrix = None  # this will contain every element (or node) in our tile_map
        # the next variables will store how many rows and columns the matrix will have
        self.width = width
        self.height = height

    # this initializes the world from zero, currently not being used, but still useful to have around
    def create_world(self):
        self.matrix = [[WorldTile(False) for x in range(self.width)] for y in range(self.height)]
        for col in range(len(self.matrix)):
            for row in range(len(self.matrix[col])):
                self.matrix[col][row].set_position(col * TILE_SIZE, row * TILE_SIZE)

    # this allows to load a map tile from a .txt, and it's currently the only way to have walls from the start
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

    # this function will be called on each frame update, and calls the draw function on each tile
    def draw_world(self, surface):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                self.matrix[i][j].draw_tile(surface)

    # this function returns the i and j of a tile, given its x and y positions as parameters.
    # returns None should x and y positions were out of bounds, for validation purposes
    def clicked_tile(self, x, y):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                temp = self.matrix[i][j]
                if temp.x_pos <= x < temp.x_pos + TILE_SIZE \
                        and temp.y_pos - TILE_SIZE <= y < temp.y_pos - TILE_SIZE + TILE_SIZE:
                    return i, j
        return None

    # this returns a tile itself by its x and y positions. also returns None should those positions were out of bounds
    def get_tile(self, x, y):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                temp = self.matrix[i][j]
                if temp.x_pos <= x < temp.x_pos + TILE_SIZE \
                        and temp.y_pos - TILE_SIZE <= y < temp.y_pos - TILE_SIZE + TILE_SIZE:
                    return self.matrix[i][j]
        return None

    # straight up returns a tile by its array indexes
    def get_tile_by_index(self, x, y):
        return self.matrix[x][y]