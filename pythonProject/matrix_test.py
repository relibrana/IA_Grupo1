import pygame as pg
import pygame.display as display
WIDTH=993
TILESIZE=20
HEIGHT= 804
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

world = World(10, 10)
world.create_world()

print(len(world.matrix))

while not gameExit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameExit = True

    gameDisplay.fill(white)
    gameDisplay.blit(land_surface, (0, 0))
    pg.draw.rect(gameDisplay, black, [86, 180, 20, 20],3)

    display.update()

pg.quit()
quit()
