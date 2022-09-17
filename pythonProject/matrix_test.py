import pygame as pg
import pygame.display as display
import pickle

WIDTH = 993
TILE_SIZE = 18
HEIGHT = 804
BG_COLOR = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
BLACK = (0, 0, 0)

world_data=[]

for row in range(55):
	r = [0] * 45
	world_data.append(r)
def draw_tile(surface, tile):
    print(tile.x_pos, tile.y_pos)
    pg.draw.rect(surface, LIGHT_GREY, [tile.x_pos, tile.y_pos, TILE_SIZE, TILE_SIZE])


# element de la matrix
##lista de listas
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
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		gameDisplay.blit(self.image, (self.rect.x, self.rect.y))

		return action

save_button = Button(WIDTH // 2 - 150, HEIGHT - 80, pg.image.load('sprites/pikachu_pequenio.png'))


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
            pos = pg.mouse.get_pos()
            x = pos[0] // TILE_SIZE
            y = pos[1] // TILE_SIZE
            if pg.mouse.get_pressed()[0] == 1:
                world_data[x][y] += 1
                if world_data[x][y]>2:
                    world_data[x][y]=0
            print(world_data)

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

    if save_button.draw():
        # save level data
        print(world.matrix)
        pickle_out = open(f'world_data.txt', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
        print(world_data)
    display.update()

pg.quit()
quit()
