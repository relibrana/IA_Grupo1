import numpy as np
import pygame as pg
import sys
import pygame.display as display
from pygame.locals import *
WIDTH=993
TILESIZE=18
HEIGHT= 804
BGCOLOR = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

file = 'sprites/map.png'
class Player:
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image=pg.image.load('pikachu_pequenio.png')
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('pruebita')
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        land_surface = pg.image.load('sprites/map.png')
        gameDisplay.blit(land_surface, (0, 0))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.draw_grid()
        pg.display.flip()

    def events(self):
        #A*
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()


# create the game object
g = Game()

while True:
    gameDisplay = display.set_mode((WIDTH, HEIGHT))
    g.new()
    g.run()

