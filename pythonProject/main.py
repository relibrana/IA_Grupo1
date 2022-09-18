# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from random import randint
import pygame
import MatrixWorld

# Press the green button in the gutter to run the script.
class Graph:
    #InITIALIZE THE GRAPH
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
        self.H = {}
        lis = list(adjac_lis)
        for i in range(len(self.adjac_lis)):
            self.H[lis[i]] = 1

    #GET ADJACENCY LIST
    def get_neighbors(self, v):
        return self.adjac_lis[v]

    # This is heuristic function which is having equal values for all nodes
    def h(self, n):
        """H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }"""

        return self.H[n]

    #A-STAR ALGORITHM
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's
        # neighbours haven't all been always inspected, It starts off with the start
        # node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])

        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0

        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = start

        while len(open_lst) > 0:
            n = None

            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all the neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node is not presentin both open_lst and closed_lst
                # add it to open_lst and note n as it's par
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    par[m] = n
                    poo[m] = poo[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update par data and poo data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of his neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)

        print('Path does not exist!')
        return None



class Adult(pygame.sprite.Sprite):
    #Initialize adult class
    def __init__(self, width, height, pos_x, pos_y, img, prob):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.problem = prob

    #Change sprite's position
    def change_pos(self, newX, newY):
        self.kill()#Once we change pos, we use the kill function to delete our sprite from any list where is included
        self.rect.center = [newX, newY] #Change the rect center with new coordinates

    def get_problem(self):
        return self.problem #Return the type of problem the adult has

    def change_problem(self, newP):
        self.problem = newP #Change the problem type

    def get_rect(self):
        return self.rect #Get the rect of the adult, this will help to check collisions



if __name__ == '__main__':
    #########################
    #Read matrix, this will get us the possible roads
    with open('world_data.txt') as f:
        L = []
        for line in f:
            L.append([int(x) for x in line.split()])

        shape_y = len(L)
        shape_x = len(L[0])
        matrix = L

    
    ##########################################################
    # #INITIAL DATA OF PROBLEM TEXTS#
    # textos = {
    #     1: "Ayudame con mis compras del supermercado",
    #     2: "Ayudame con mis compras en la farmacia",
    #     3: "Llevale este presente a la casa de mi nieto (35)",
    #     4: "Recoge mis resultados medicos del hospital"
    # }
    #POSITIONS WHERE THE ADULT COULD BE LOCATED#
    positions = {
        1: (801, 711),
        2: (192, 585),
        3: (633, 558),
        4: (346, 617),
        5: (117, 315),
        6: (45, 423),
        7: (585, 441),
        8: (783, 405),
        9: (405, 261),
        10: (873, 459),
        11: (729, 279),
        12: (171, 387),
        13: (297, 567),
        14: (243, 459),

    }

 
    #PLACES OF INTEREST OF THE ADULT#
    places_of_interest = {
        1: ([423, 585, 33, 23], "SUPERMARKET"),  # SUPERMARKET
        2: ([243, 284, 15, 13], "DRUGSTORES"),  # DRUGSTORE
        3: ([81, 477, 26, 4], "HOME"),  # HOME
        4: ([153, 235, 12, 8], "HOSPITAL"),  # HOSPITAL
    }
    ##

    #WE INITIALIZE A DICTIONARY
    graph = {}
    edges = 0
    y_temp = -1

    #######################################################################
    ##WE ITERATE THE MATRIX AND ASSING A NUMERIC ID TO OUR NODES
    ##THIS ID IS THE RESULT OF MULTIPLIYING THE POSITION OF Y WITH THE WIDTH OF OUR MATRIX
    ##PLUS THE POSITION OF X
    for i in range(shape_y * shape_x):
        x_temp = (i % shape_x)
        if x_temp == 0:
            y_temp += 1
        if matrix[y_temp][x_temp] == 1:
            edges += 1
            key1 = None
            if y_temp > 0:
                if matrix[y_temp - 1][x_temp] == 1:
                    graph[i] = [(i - shape_x, 1)]
                    key1 = True
            if y_temp < shape_y - 1:
                if matrix[y_temp + 1][x_temp] == 1:
                    if key1:
                        graph[i].append((i + shape_x, 1))
                    else:
                        graph[i] = [(i + shape_x, 1)]
                        key1 = True
            if x_temp > 0:
                if matrix[y_temp][x_temp - 1] == 1:
                    if key1:
                        graph[i].append((i - 1, 1))
                    else:
                        graph[i] = [(i - 1, 1)]
                        key1 = True
            if x_temp < shape_x - 1:
                if matrix[y_temp][x_temp + 1] == 1:
                    if key1:
                        graph[i].append((i + 1, 1))
                    else:
                        graph[i] = [(i + 1, 1)]
    ########################################################################



    ##WE CONVERT OUR DICTIONARY TO A GRAPH CLASS OBJECT
    graph1 = Graph(graph)
    ##WE ASSIGN THE INITIAL POSITION TO OUR PLAYER
    graph_init = 460
    graph_fin = 460

    ##WE USE FOR THE FIRST TIME THE ALGORITHM STAR TO DETERMINE A PATH, IF NO PATH IS AVAILABLE WE DONT CHANGE THE PREVIOUS PATH VALUE
    if graph1.a_star_algorithm(graph_init, graph_fin) != None:
        path = graph1.a_star_algorithm(graph_init, graph_fin)

    #########################

    pygame.init()

    ##WE START A CLASS WORLD OBJECT THAT IS IMPLEMENTED ON THE MATRIXWORLD.PY FILE
    world = MatrixWorld.World(45, 55)
    ##READ MATRIX VALUE AND LOAD IT TO THE OBJECT
    world.load_map_tile()

    # Change
    # W, H = shape_x, shape_y
    ##WIDHT AND HEIGHT OF OUR INITIAL SCREEN
    W, H = 990, 810
    screen = pygame.display.set_mode((W, H))
    ##CHANGE CAPTION OF THE SCREEN
    pygame.display.set_caption("Help Granny")
    ##INITIALIZE A CLOCK OBJECT
    clock = pygame.time.Clock()

    """
        N = number of Edges
        step = "speed" of the character
        pos_x_pika, pos_y_pika = (x,y) of character
        div = number of div
        """
    ################
    # Sprite player
    
    ##WE LOAD ALL THE IMAGES WE ARE GONNA NEED FOR THE GAME
    land_surface = pygame.image.load('sprites/map.png')
    background=pygame.image.load('sprites/fondo_rosa.jpg')
    land_surface = pygame.transform.scale(land_surface, (W, H))
    menu=pygame.image.load('sprites/start.png')
    request_supermarket = pygame.image.load('sprites/pedido_supermercado.png')
    request_home = pygame.image.load('sprites/pedido_nieto.png')
    request_drugstore = pygame.image.load('sprites/pedido_farmacia.png')
    request_hospital_results = pygame.image.load('sprites/pedido_hospital.png')
    
    ##WE INITIALIZE IMAGE VALUES, TO EASILY CHANGE THE IMAGE DEPENDING ON THE PROBLEM
    requests = {
        1: request_supermarket,
        2: request_drugstore,
        3: request_home,
        4: request_hospital_results
    }

    ##LOAD PLAYER IMAGE
    player = pygame.image.load('sprites/professor_walk_cycle_no_hat.png').convert_alpha()
    
    ##GET WIDTH AND HEIGHT FROM THE PLAYER IMAGE
    player_x = player.get_width()
    player_y = player.get_height()

    ##ADULT SPRITE
    adult_original = pygame.image.load('sprites/adulto.png')
    adult = pygame.transform.scale(adult_original, (30, 30))
    adult_x = adult.get_width()
    adult_y = adult.get_height()
    last = 1

    ##WE INITIALIZE AN ADULT CLASS OBJECT
    adult = Adult(adult_x, adult_y, 801, 711, adult, 4)

    ##WE CREATE A SPRITE GROUP
    adult_sprite = pygame.sprite.Group()

    ##WE ADD THE ADULT CLASS OBJECT TO A SPRITE GROUP
    adult_sprite.add(adult)
    """player_x = player_x*0.9
    player_y = player_y*0.9
    player = pygame.transform.scale(player, (player_x, player_y))"""
    #########################
    # Variable
    ##WE ARE GONNA USE THIS VARIABLE FOR CONDITIONAL PURPOSES, WE CANT ANALIZE COLLISIONS IF THE PLAYER IS MOVING
    moving = False

    ## THIS IS GOING TO BE OUR STRUCTURE TO SAVE OUR NODES AND THEIR POSITIONS
    ## AND WE'RE GOING TO UES THE ITERATE y_temp FOR THE SAME PURPOSE TO HAVE ALL THE POSITIONS OF THE MATRIX
    dic = {}
    y_temp = -1
    # Graph
    ## WE SAVE THE WIDTH AND HEIGHT OF ONE TILE IN THE MAP
    each_shape_x = W / shape_x
    each_shape_y = H / shape_y

    for i in range(shape_x * shape_y):
        x_temp = (i % shape_x)
        if x_temp == 0:
            y_temp += 1
        ## WITH A SIMPLE LOGIC WE DISTRIBUTE ALL THE POSITIONS OF THE CENTER OF THE TILES
        ## WITH THE POSITIONS OF THE PIXEL IN THE MAP
        dic[i] = [(int(each_shape_x / 2) + int(each_shape_x) * x_temp,
                   int(each_shape_y / 2) + int(each_shape_y) * y_temp)
            , (y_temp, x_temp)]

    ## WE USE THIS VARIABLE TO SHOW THE GRAPH IN RUN-TIME OF THE PROGRAM
    ## BUT FOR THE HIGH AMOUNT OF NODES IN OUR GRAPH WE ARE NOT GONIG TO SET IT TRUE THIS VARIABLE
    graph_visible = False

    ## WE'RE GOING TO USE THIS VARIABLES TO ITERATE THE IMAGE OF THE PLAYER AND
    ## GIVE HIM ANIMATION
    sp_pl_x = 0
    sp_pl_y = 0

    ## WE USE THIS PART OF THE CODE TO SPLIT THE IMAGE IN 36 PARTS TO GIVE ANIMATION TO THE PLAYER
    pixel_arr = pygame.PixelArray(player)
    ## AGAIN, WE USE A SIMPLE MATH LOGIC TO GIVE HIM CORRECT POSITIONS
    ## BUT FIRST WE NEED TO TREAT IT AS A MATRIX AND CONVERT IT TO A SURFACE
    player1 = pixel_arr[int(player_x / 9) * sp_pl_x:int(player_x / 9) * (sp_pl_x + 1),
              int(player_y / 4) * sp_pl_y:int(player_y / 4) * (sp_pl_y + 1) + 10].make_surface()
    player_rect = player1.get_rect(midbottom=(dic[graph_init][0][0], dic[graph_init][0][1] + 20))
    pygame.PixelArray.close(pixel_arr)
    ##########################
    ## SPPED OF THE PLAYER
    step = 2
    ## TO INTERPOLATE THE DIVISIONS OF THE IMAGE
    ad = 1

    ## FIRST VERSION OF THE FOLLOWED PATH
    path2 = path[::-1]
    path = path + path2
    follow = None
    ##THIS VARIABLE WILL HELP TO DETERMINE IF THE PLAYER HAS DONE THE REQUEST BEFORE GOING WITH THE ADULT
    item = False
    start=True
    game=False


    ##SET THE OBJECT TILE THAT IS OUR FIRST TARGET, THIS WILL HELP TO DETERMINE WHERE WE GOTTA CLICK ON THE SCREEN
    world.get_tile_by_index(places_of_interest[adult.get_problem()][0][2], places_of_interest[adult.get_problem()][0][3]) \
        .set_target(True)

    while True:
        ## WE START TO GIVE HIM TO THE PLAYER THE FIRST POSITION TO FOLLOW IF THE PATH HAS CONTENT
        # Follow
        if path:
            follow = path[0]
        ## WE'RE GOING TO SET THE STEP TO 0 TO AVOID THE ANIMATION
        else:
            step = 0
            ad = 0
            moving = False

        ## THIS PART OF THE CODE CONTAIN OR MANAGE ALL THE EVENTS IN THE GAME
        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and moving is False and game==True:
                moving = True
                temp = world.clicked_tile(event.pos[0], event.pos[1])
                if temp is not None:
                    print(temp[0], temp[1])
                    m = world.matrix
                    print(dic[graph_init][0][0], dic[graph_init][0][1] + 20)
                    print(m[temp[0]][temp[1]].tile_center())

                    graph_fin = temp[1] + temp[0] * shape_x
                    node = graph1.a_star_algorithm(graph_init, graph_fin)
                    if node is not None:
                        path = node
                        follow = path[0]
                        step = 5
                        ad = 1
            if event.type == pygame.MOUSEBUTTONDOWN and game==False:
                game=True

        # SHOW MENU SCREEN
        if game ==False:
            screen.blit(menu, (0, 0))
        else:

            ##PUT BACKGROUND IMAGE, THE SURFACE IMAGE, DRAW THE PLAYER AND THE REQUEST
            screen.blit(background,(0,0))
            screen.blit(land_surface, (0, 0))
            world.draw_world(screen)
            screen.blit(player1, player_rect)
            screen.blit(requests[adult.get_problem()], (0, 670))

            ## THIS PART OF THE CODE IS TO GIVE HIM ANIMATION TO THE PLAYER IN BASE OF THE INDEX AS A RESUSLT OF THE MATH SPLIT OF THE IMAGE
            if sp_pl_x < 8:
                sp_pl_x += ad
            else:
                sp_pl_x = 0
            if player_rect.centery < dic[follow][0][1] - step:
                player_rect.centery += step
                sp_pl_y = 2
            elif player_rect.centery > dic[follow][0][1] + step:
                player_rect.centery -= step
                sp_pl_y = 0
            elif player_rect.centerx < dic[follow][0][0] - step:
                player_rect.centerx += step
                sp_pl_y = 3
            elif player_rect.centerx > dic[follow][0][0] + step:
                player_rect.centerx -= step
                sp_pl_y = 1

            # Collision
            if path is not None and (player_rect.centerx - step <= dic[follow][0][0] <= player_rect.centerx + step) and (
                    player_rect.centery - step <= dic[follow][0][1] <= player_rect.centery + step):
                path.pop(0)
                graph_init = graph_fin

            ##WE CREATE RECTS TO CHECK COLLITIONS
            place_rect = pygame.rect.Rect(places_of_interest[adult.get_problem()][0][0], places_of_interest[adult.get_problem()][0][1], 5, 5)
            play_rect = pygame.rect.Rect(dic[graph_init][0][0], dic[graph_init][0][1] + 20, 18, 18)


            if pygame.Rect.colliderect(player_rect, adult.get_rect()) and item is not False:
                ##WE MAKE THIS LOOP TO AVOID REPEATING SAME POSITIONS
                while 1:
                    num = randint(1, 14)
                    if num == last:
                        continue
                    else:
                        last = num
                        break
                ##GET X AND Y POSITIONS
                x_pos,y_pos = positions[num]
                ##CHANGE POSITIONS
                adult.change_pos(x_pos, y_pos)
                ##CHANGE PROBLEM
                adult.change_problem(randint(1, 4))
                ##ADD AGAINT TO THE GROUP
                adult_sprite.add(adult)
                ##GET NEW PATH
                path = graph1.a_star_algorithm(graph_init, graph_fin)
                ##SET ITEM FALSE, WE HAVE TO DO THE REQUEST AGAIN
                item = False
                ##GET TILE TARGET
                my_tile = world.get_tile_by_index(places_of_interest[adult.get_problem()][0][2], places_of_interest[adult.get_problem()][0][3])
                ##FILL TILE TARGET WITH RED COLOR
                my_tile.set_target(True)

            if pygame.Rect.colliderect(play_rect, place_rect) and moving is False:
                ##IF PLAYER AND PLACE COLLIDE, PLAYER CON GO WITH ADULT BY SETTING ITEM TO TRUE
                print("colision", places_of_interest[adult.get_problem()][1])
                item = True
                ##GET TILE TARGET AND SETTING IT TO FALSE, TO RETURN TO THE ORIGINAL COLOR
                my_tile = world.get_tile_by_index(places_of_interest[adult.get_problem()][0][2], places_of_interest[adult.get_problem()][0][3])
                my_tile.set_target(False)

            #######
            ## THIS PART IS FOR UPDATE THE PART SHOWN OF THE IMAGE
            pixel_arr = pygame.PixelArray(player)
            player1 = pixel_arr[int(player_x / 9) * sp_pl_x:int(player_x / 9) * (sp_pl_x + 1),
                      int(player_y / 4) * sp_pl_y:int(player_y / 4) * (sp_pl_y + 1)].make_surface()
            pygame.PixelArray.close(pixel_arr)
            if len(adult_sprite) != 0:
                adult_sprite.draw(screen)
            #######

  

        pygame.display.update()
        clock.tick(40)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
