import pygame as pg
import pygame.display as display
WIDTH=993
TILESIZE=18
HEIGHT= 804
BGCOLOR = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
import numpy as np
from pygame.locals import *

#elemento de la matrix
class WorldTile:
    def __init__(self, _is_wall):
        self.isWall = _is_wall #casa
        self.value = 0



#Matrix
class World:
    def __init__(self, width, height):
        self.matrix = None
        self.width = width
        self.height = height

    def create_world(self):
        self.matrix = [[WorldTile(False)] * self.width] * self.height #crear matrix


pg.init()

white = (255, 255, 255)
black = (0, 0, 0)

land_surface = pg.image.load('sprites/map.png')

gameDisplay = display.set_mode((WIDTH, HEIGHT))

display.update()

gameExit = False

world = World(45, 55)
world.create_world()

print(len(world.matrix))

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True

    gameDisplay.fill(white)
    gameDisplay.blit(land_surface, (0, 0))
    pg.draw.rect(gameDisplay, black, [86, 180, 18, 18],3)
    for x in range(0, WIDTH, TILESIZE):
       pg.draw.line(gameDisplay, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
       pg.draw.line(gameDisplay, LIGHTGREY, (0, y), (WIDTH, y))

    display.update()

pg.quit()
quit()
