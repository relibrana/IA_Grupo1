# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from random import randint
import pygame
import MatrixWorld


# Press the green button in the gutter to run the script.
class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
        self.H = {}
        lis = list(adjac_lis)
        for i in range(len(self.adjac_lis)):
            self.H[lis[i]] = 1

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

class Adulto(pygame.sprite.Sprite):
    def __init__(self, width,height,pos_x,pos_y,img,prob):
        super().__init__()
        self.image=pygame.Surface([width,height])
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.center=[pos_x,pos_y]
        self.problem=prob
    def change_pos(self,newX,newY):
        self.kill()
        self.rect.center=[newX,newY]
    def get_problem(self):
        return self.problem
    def change_problem(self,newP):
        self.problem=newP
    def get_rect(self):
        return self.rect
def pushInfo_Text2(posInd,s:str):
    with open(s,'w+',newline='\n') as f:
        for i in posInd.keys():
            try: 
                int(i)
                f.write(f"{i}: "+ str(posInd.get(i))+"\n")
            except:
                continue  
if __name__ == '__main__':
    #########################
    with open('world_data.txt') as f:
        L = []
        for line in f:
            L.append([int(x) for x in line.split()])
        # Change
        # L = np.asarray(L)
        # L = np.transpose(L)

        shape_y = len(L)
        shape_x = len(L[0])

        matrix = L
        # print(len(matrix[0]))

    #ultimo
    textos={
        1:"Ayudame con mis compras del supermercado",
        2:"Ayudame con mis compras en la farmacia",
        3:"Llevale este presente a la casa de mi nieto"
    }
    posiciones={
        1:[801,711],
        2:[192,585],
        3:[633,558],
        4:[346,617],
    }
    lugares={
        1:[415,575]
    }
    ##

    graph = {}
    edges = 0
    y_temp = -1
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

    print(graph)
    graph1 = Graph(graph)
    pushInfo_Text2(graph,"dicitionary.txt")
    #print(graph[277239])
    graph_init = 460
    graph_fin = 460

    if graph1.a_star_algorithm(graph_init, graph_fin) != None:
        path = graph1.a_star_algorithm(graph_init, graph_fin)

    print(shape_x, shape_y)
    #########################
    pygame.init()

    world = MatrixWorld.World(45, 55)
    world.load_map_tile()

    # Change
    # W, H = shape_x, shape_y
    W, H = 990, 810
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

    land_surface = pygame.image.load('sprites/map.png')
    land_surface = pygame.transform.scale(land_surface, (W, H))

    player = pygame.image.load('sprites/professor_walk_cycle_no_hat.png').convert_alpha()
    player_x = player.get_width()
    player_y = player.get_height()

    # Sprite adulto
    ad_original=pygame.image.load('sprites/adulto.png')
    ad=pygame.transform.scale(ad_original,(30,30))
    adulto_x = ad.get_width()
    adulto_y = ad.get_height()
    last=1
    adulto=Adulto(adulto_x,adulto_y,801,711,ad,1)
    adulto_sprite=pygame.sprite.Group()
    adulto_sprite.add(adulto)
    """player_x = player_x*0.9
    player_y = player_y*0.9
    player = pygame.transform.scale(player, (player_x, player_y))"""
    #########################
    # Variable
    moving=False
    # Dimensions


    #########################
    # Matrix
    # shape_x = int(W/(player_x/9))
    # shape_y = int(H/(player_y/4))
    """
        # Change
        # shape_x = W
        # shape_y = H
    """
    shape_x = shape_x
    shape_y = shape_y
    # matrix = np.zeros((shape_y, shape_x), dtype=int)
    # matrix[1:-1, 1:-1] = 1
    dic = {}
    y_temp = -1
    # Graph
    print(shape_x, shape_y)

    each_shape_x = W/shape_x
    each_shape_y = H/shape_y

    for i in range(shape_x*shape_y):
        x_temp = (i % shape_x)
        if x_temp == 0:
            y_temp += 1
        # y_temp = int(i / shape_y)
        """dic[i] = [(int(player_x/18) + int(player_x/9) * x_temp,
                   int(player_y/8) + int(player_y/4) * y_temp)
            , (y_temp, x_temp)]"""
        dic[i] = [(int(each_shape_x / 2) + int(each_shape_x) * x_temp,
                   int(each_shape_y / 2) + int(each_shape_y) * y_temp)
            , (y_temp, x_temp)]

        # Change
        """dic[i] = [(x_temp, y_temp), (y_temp, x_temp)]"""
    """
    for i in range(N):
        c = 150
        x_temp = (i % div)
        y_temp = int(i / div)
        dic[i] = (40 + c * x_temp, 40 + c * y_temp)
    """
    graph_visible = False
    #print(shape_x, " ", shape_y)
    print(dic)
    #########################
    sp_pl_x = 0
    sp_pl_y = 0

    pixel_arr = pygame.PixelArray(player)
    player1 = pixel_arr[int(player_x/9)*sp_pl_x:int(player_x/9)*(sp_pl_x+1),
                        int(player_y/4)*sp_pl_y:int(player_y/4)*(sp_pl_y+1) + 10].make_surface()
    player_rect = player1.get_rect(midbottom=(dic[graph_init][0][0], dic[graph_init][0][1] + 20))
    pygame.PixelArray.close(pixel_arr)
    ##########################
    step = 2
    ad = 1
    # Path from algorithm
    #path = [212291, 212292, 212293, 212294]
    path2 = path[::-1]
    path = path + path2
    follow = None
    while True:
        # Follow
        if path:
            follow = path[0]
        else:
            step = 0
            ad = 0
            moving=False
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and moving==False:
                moving=True
                temp = world.clicked_tile(event)
                if temp is not None:
                    print(temp[0], temp[1])
                    m=world.matrix
                    print(dic[graph_init][0][0], dic[graph_init][0][1] + 20)
                    print(m[temp[0]][temp[1]].tile_center())
                    
                    graph_fin = temp[1]+temp[0]*shape_x
                    node = graph1.a_star_algorithm(graph_init, graph_fin)
                    if node is not None:
                        path = node
                        follow = path[0]
                        step = 5
                        ad = 1

        # Show
        screen.fill([255, 255, 255])
        screen.blit(land_surface, (0, 0))
        world.draw_world(screen)
        screen.blit(player1, player_rect)

        """
        # Movement
        # pos_x_pika += step
        # pika_rect.left += step
        """
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
        """if player_rect.collidepoint(dic[follow][0]) and len(path) != 0:
            path.pop(0)"""
        if path!=None and (player_rect.centerx - step <= dic[follow][0][0] <= player_rect.centerx + step) and (player_rect.centery - step <= dic[follow][0][1] <= player_rect.centery + step):
            path.pop(0)
            graph_init = graph_fin
        
       

        # if len(path)==0 & help==True:
        #     while(1):
        #         num=randint(1,3)
        #         if(num==last):
        #             continue
        #         else:
        #             last=num
        #             break
        #     positions=posiciones[randint(1,3)]
        #     adulto.change_pos(positions[0],positions[1])
        #     adulto_sprite.add(adulto)
        #     graph_fin=positions[1]*965+positions[0]
        #     print(positions[1]*965+positions[0])
        #     path = graph1.a_star_algorithm(graph_init, graph_fin)
        #     help=False
        #     # adulto_sprite.add(adulto)

        lugar_rect=pygame.rect.Rect(lugares[1][0],lugares[1][1],5,5)
        jugador_rect=pygame.rect.Rect(dic[graph_init][0][0], dic[graph_init][0][1]+20 ,18,18)

        if pygame.Rect.colliderect(player_rect,adulto.get_rect()):
            while(1):
                num=randint(1,4)
                if(num==last):
                    continue
                else:
                    last=num
                    break
            positions=posiciones[randint(1,4)]
            adulto.change_pos(positions[0],positions[1])
            adulto_sprite.add(adulto)
            # graph_fin=positions[1]*965+positions[0]
            # print(positions[1]*965+positions[0])
            path = graph1.a_star_algorithm(graph_init, graph_fin)
            # help=False
        
        
        # if path!=None and (player_rect.centerx - step <= lugares[1][0] <= player_rect.centerx + step) and (player_rect.centery - step <= lugares[1][1] <= player_rect.centery + step):
        
        if pygame.Rect.colliderect(jugador_rect,lugar_rect):
            print("colision supermercado")

        
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
        if len(adulto_sprite)!=0:
            adulto_sprite.draw(screen)
        #######
        pygame.display.update()
        clock.tick(40)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
