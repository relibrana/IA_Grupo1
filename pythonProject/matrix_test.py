import pygame as pg
import pygame.display as display

WIDTH = 993
TILE_SIZE = 18
HEIGHT = 804
BG_COLOR = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
BLACK = (0, 0, 0)


def draw_tile(surface, tile):
    print(tile.x_pos, tile.y_pos)
    pg.draw.rect(surface, LIGHT_GREY, [tile.x_pos, tile.y_pos, TILE_SIZE, TILE_SIZE])


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

    def load_map_tile(self):
        # definir funcion para leer un txt y obtener el map tile
        return self.matrix

    def print_world(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                print(self.matrix[i][j].x_pos, self.matrix[i][j].y_pos)


pg.init()

white = (255, 255, 255)
black = (0, 0, 0)

land_surface = pg.image.load('sprites/map.png')

gameDisplay = display.set_mode((WIDTH, HEIGHT))

display.update()

gameExit = False

world = World(45, 55)
world.create_world()

for col in range(len(world.matrix)):
    for row in range(len(world.matrix[col])):
        world.matrix[col][row].set_position(col * TILE_SIZE, row * TILE_SIZE)

# world.print_world()

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            for col in range(len(world.matrix)):
                for row in range(len(world.matrix[col])):
                    temp = world.matrix[col][row]
                    if temp.x_pos <= event.pos[0] < temp.x_pos + TILE_SIZE \
                            and temp.y_pos <= event.pos[1] < temp.y_pos + TILE_SIZE:
                        print("clicked tile ", col, row)
                        temp.set_wall(True)

    gameDisplay.fill(white)
    gameDisplay.blit(land_surface, (0, 0))

    for col in range(len(world.matrix)):
        for row in range(len(world.matrix[col])):
            if world.matrix[col][row].isWall:
                pg.draw.rect(gameDisplay, BLACK,
                             [world.matrix[col][row].x_pos, world.matrix[col][row].y_pos, TILE_SIZE, TILE_SIZE])
            else:
                pg.draw.rect(gameDisplay, LIGHT_GREY,
                             [world.matrix[col][row].x_pos, world.matrix[col][row].y_pos, TILE_SIZE, TILE_SIZE], 1)

    display.update()

pg.quit()
quit()
