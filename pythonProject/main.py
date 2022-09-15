# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    W, H = 1080, 780
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("IA")
    clock = pygame.time.Clock()

    """
        N = number of Edges
        step = "speed" of the character
        pos_x_pika, pos_y_pika = (x,y) of character
        div = number of div
        """
    ################
    # Sprite player
    land_surface = pygame.image.load('sprites/Escenario.png')
    land_surface = pygame.transform.scale(land_surface, (1080, 780))

    player = pygame.image.load('sprites/professor_walk_cycle_no_hat.png').convert_alpha()

    #########################
    # Dimensions
    player_x = player.get_width()
    player_y = player.get_height()


    #########################
    # Matrix
    shape_x = int(W/(player_x/9))
    shape_y = int(H/(player_y/4))

    matrix = np.zeros((shape_y, shape_x), dtype=int)
    matrix[1:-1, 1:-1] = 1

    dic = {}
    y_temp = -1
    # Graph
    for i in range(shape_x*shape_y):
        x_temp = (i % shape_x)
        if x_temp == 0:
            y_temp += 1
        # y_temp = int(i / shape_y)
        dic[i] = [(int(player_x/18) + int(player_x/9) * x_temp,
                   int(player_y/8) + int(player_y/4) * y_temp)
            , (y_temp, x_temp)]
    """
    for i in range(N):
        c = 150
        x_temp = (i % div)
        y_temp = int(i / div)
        dic[i] = (40 + c * x_temp, 40 + c * y_temp)
    """
    graph_visible = False
    print(shape_x, " ", shape_y)
    print(dic)
    #########################
    sp_pl_x = 0
    sp_pl_y = 0

    pixel_arr = pygame.PixelArray(player)
    player1 = pixel_arr[int(player_x/9)*sp_pl_x:int(player_x/9)*(sp_pl_x+1),
                        int(player_y/4)*sp_pl_y:int(player_y/4)*(sp_pl_y+1)].make_surface()
    player_rect = player1.get_rect(midbottom=(dic[0][0][0] + 20, dic[0][0][1] + 20))
    pygame.PixelArray.close(pixel_arr)
    ##########################
    step = 4
    ad = 1
    # Path from algorithm
    path = [0, 1, 4, 3, 6, 7, 8, 5, 2]
    path2 = path[::-1]
    path = path + path2
    follow = path[0]
    while True:
        # Follow
        if path:
            follow = path[0]
        else:
            step = 0
            ad = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Show
        screen.blit(land_surface, (0, 0))
        screen.blit(player1, player_rect)

        """
        # Movement
        # pos_x_pika += step
        # pika_rect.left += step
        """
        if player_rect.centerx < dic[follow][0][0] - step:
            player_rect.centerx += step
            sp_pl_y = 3
        elif player_rect.centerx > dic[follow][0][0] + step:
            player_rect.centerx -= step
            sp_pl_y = 1
        if player_rect.centery < dic[follow][0][1] - step:
            player_rect.centery += step
            sp_pl_y = 2
        elif player_rect.centery > dic[follow][0][1] + step:
            player_rect.centery -= step
            sp_pl_y = 0
        if sp_pl_x < 8:
            sp_pl_x += ad
        else:
            sp_pl_x = 0

        # Collision
        if player_rect.collidepoint(dic[follow][0]) and len(path) != 0:
            path.pop(0)

        if graph_visible:
            for i in range(shape_x*shape_y):
                font = pygame.font.Font(None, 40)
                text = font.render(str(i), False, 'black')
                text_rect = text.get_rect(center=(200, 200))
                pygame.draw.circle(screen, 'red', dic[i][0], 15)
                screen.blit(text, (dic[i][0][0] - 10, dic[i][0][1] - 10))

        #######
        pixel_arr = pygame.PixelArray(player)
        player1 = pixel_arr[int(player_x / 9) * sp_pl_x:int(player_x / 9) * (sp_pl_x + 1), int(player_y / 4) * sp_pl_y:int(player_y / 4) * (sp_pl_y + 1)].make_surface()
        pygame.PixelArray.close(pixel_arr)

        #######
        pygame.display.update()
        clock.tick(60)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
