#importing modules
import pygame, math, sys, time


#setup
pygame.init()
wn = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

#Setting class
class Setting:
    def __init__(self):
        self.FPS = 600
        self.angle = 0
        self.vertices = [[[1], [1], [1]], [[-1], [1], [1]], [[-1], [-1], [1]], [[1], [-1], [1]], [[1], [1], [-1]], [[-1], [1], [-1]], [[-1], [-1], [-1]], [[1], [-1], [-1]]]
        self.scale = 500
        self.x_offset = 300
        self.y_offset = 300

    #handling events / input from user
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.scale += 1
        elif keys[pygame.K_s]:
            self.scale -= 1
        elif keys[pygame.K_LEFT]:
            self.x_offset -= 1
        elif keys[pygame.K_RIGHT]:
            self.x_offset += 1
        elif keys[pygame.K_UP]:
            self.y_offset -= 1
        elif keys[pygame.K_DOWN]:
            self.y_offset += 1
            
                
    #multiplying two matrices
    def multiply_matrices(self, a, b):
        matrix = [[0 for i in range(len(b[0]))] for j in range(len(a))]
        for i in range(len(b[0])):
            for j in range(len(a)):
                total = 0
                for k in range(len(b)):
                    total += a[j][k] * b[k][i]
                matrix[j][i] = total
        return matrix


    #connecting the edges of the faces to form a polygon
    def connect(self, face, color):
        pygame.draw.polygon(wn, color, [[face[0][0], face[0][1]], [face[1][0], face[1][1]], [face[2][0], face[2][1]], [face[3][0], face[3][1]]])
        pygame.draw.polygon(wn, (255, 255, 255), [[face[0][0], face[0][1]], [face[1][0], face[1][1]], [face[2][0], face[2][1]], [face[3][0], face[3][1]]], 4)


    #rotating the 3d vertices of the cube and projecting them to 2d
    def project(self):
        self.new_vertices = []
        for vertex in self.vertices:
            rotation_z_matrix = [[math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)), 0],
                                      [math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle)), 0],
                                      [0, 0, 1]]
            rotation_y_matrix = [[math.cos(math.radians(self.angle)), 0, math.sin(math.radians(self.angle))],
                                      [0, 1, 0],
                                      [-math.sin(math.radians(self.angle)), 0, math.cos(math.radians(self.angle))]]
            rotation_x_matrix = [[1, 0, 0],
                                      [0, math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))],
                                      [0, math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle))]]
            
            product = self.multiply_matrices(rotation_x_matrix, rotation_z_matrix)
            #product = self.multiply_matrices(product, rotation_y_matrix)
            vertex = self.multiply_matrices(product, vertex)

            z = 1 / (6 + vertex[2][0])
            vertex[0][0] = self.x_offset + (vertex[0][0] * z) * self.scale
            vertex[1][0] = self.y_offset + (vertex[1][0] * z) * self.scale
            self.new_vertices.append([vertex[0][0], vertex[1][0], vertex[2][0]])
     
        self.angle += 0.25


    #ordering the faces by depth - only the faces which are visible in real life will show
    def order_faces(self):
        closer_faces_rank = [0, 0, 0, 0, 0, 0]
        self.faces = [[self.new_vertices[0], self.new_vertices[1], self.new_vertices[2], self.new_vertices[3], (255, 0, 0)],
                      [self.new_vertices[0], self.new_vertices[3], self.new_vertices[7], self.new_vertices[4], (0, 255, 0)],
                      [self.new_vertices[1], self.new_vertices[2], self.new_vertices[6], self.new_vertices[5], (0, 0, 255)],
                      [self.new_vertices[4], self.new_vertices[5], self.new_vertices[6], self.new_vertices[7], (255, 255, 0)],
                      [self.new_vertices[1], self.new_vertices[0], self.new_vertices[4], self.new_vertices[5], (0, 255, 255)],
                      [self.new_vertices[2], self.new_vertices[3], self.new_vertices[7], self.new_vertices[6], (255, 0, 255)]]
        
        for i in range(len(self.faces) - 1):
            for j in range(i + 1, len(self.faces)):
                for k in range(4):
                    for l in range(4):
                        if self.faces[i][k][2] < self.faces[j][l][2]:
                            closer_faces_rank[i] += 1
                        elif self.faces[i][k][2] > self.faces[j][l][2]:
                            closer_faces_rank[j] += 1

        for i in range(len(closer_faces_rank) - 1):
            swapped = False
            for j in range(len(closer_faces_rank) - 1 - i):
                if closer_faces_rank[j] > closer_faces_rank[j + 1]:
                    self.faces[j], self.faces[j + 1] = self.faces[j + 1], self.faces[j]
                    closer_faces_rank[j], closer_faces_rank[j + 1] = closer_faces_rank[j + 1], closer_faces_rank[j]
                    swapped = True
            if swapped == False:
                break
        

    #rendering the cube the the window
    def render(self):
        for i in range(3, 6):
            self.connect(self.faces[i], self.faces[i][4])
            #for j in range(4):
                #z = 1 / (6 + self.faces[i][j][2])
                #pygame.draw.circle(wn, (255, 255, 255), (self.faces[i][j][0], self.faces[i][j][1]), z * 30)


    #updating the window
    def update(self):
        pygame.display.update()
        wn.fill((0, 0, 0))
        self.display = [[" " for i in range(40)] for j in range(40)]
        clock.tick(self.FPS)


#instanciating the setting class
setting = Setting()


#main loop
while True:
    setting.events()
    setting.project()
    setting.order_faces()
    setting.render()
    setting.update()

