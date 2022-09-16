import pygame
import pygame.display as display
import numpy as np
from pygame.locals import *


class WorldTile:
    def __init__(self, _is_wall):
        self.isWall = _is_wall
        self.value = 0


class World:
    def __init__(self, width, height):
        self.matrix = None
        self.width = width
        self.height = height

    def create_world(self):
        self.matrix = [[WorldTile(False)] * self.width] * self.height


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

land_surface = pygame.image.load('sprites/map.png')

gameDisplay = display.set_mode((993, 804))

display.update()

gameExit = False

world = World(10, 10)
world.create_world()

print(len(world.matrix))

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

    gameDisplay.fill(white)
    gameDisplay.blit(land_surface, (0, 0))
    pygame.draw.rect(gameDisplay, black, [86, 180, 20, 20])

    display.update()

pygame.quit()
quit()
