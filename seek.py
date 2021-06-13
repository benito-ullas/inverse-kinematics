import pygame
from vector import vector2D
import math

pygame.init()
key = pygame.key.get_pressed()

fps = 60
fpsClock = pygame.time.Clock()

scr_width = 800
scr_height = 600

line = []

#################################################################################

class Flowfield:
        def __init__(self):
                self.res = 20
                self.cols = int(scr_width / self.res) + 1
                self.rows = int(scr_height / self.res) + 1 
                self.time_loop = 60
                self.flow = [[[vector2D(0,0)for p in range(self.time_loop)] for i in range(self.rows)]for j in range(self.cols)]
                self.k = 0
                self.size = 100
                
                
        def gen_flowfield(self):
                for i in range(self.cols):
                        for j in range(self.rows):
                                for p in range(self.time_loop):
                                        v = vector2D(0,0)
                                        v.from_angle(self.res,noise([i/self.size,j/self.size,p/self.size])*360)
                                        self.flow[i][j][p] = v
        def lookup(self,i,j,p):
                return self.flow[i][j][p]
                
        
        def show(self,p):
                for i in range(self.cols):
                        for j in range(self.rows):
                                        pygame.draw.aaline(screen,(150,150,150),(i*self.res,j*self.res),(i*self.res + self.flow[i][j][p].x,j*self.res + self.flow[i][j][p].y))

#################################################################################

class Segment():
        def __init__(self,x,y,l,weight):
                self.a = vector2D(x,y)
                self.l = l
                self.angle = 0
                self.weight = weight
                self.b = vector2D(x+l*math.cos(math.radians(self.angle)),y+l*math.sin(math.radians(self.angle)))
                self.vel = vector2D(0,0)
                self.acc = vector2D(0,0)
                self.maxspeed = 5
                self.maxacc = 0.25
                
        def updateB(self):
                self.b = vector2D(self.a.x+self.l*math.cos(math.radians(self.angle)),self.a.y+self.l*math.sin(math.radians(self.angle)))
                
        def update(self):
                self.updateB()
                
                self.vel.add(self.acc)
                self.b.add(self.vel)
                self.a = vector2D(self.b.x - self.l*math.cos(math.radians(self.angle)),self.b.y - self.l*math.sin(math.radians(self.angle)))
                
                self.acc.mult(0)
        
        def follow(self,target):
                ang = vector2D(target.x - self.a.x,target.y - self.a.y).get_angle()
                self.angle = ang                       
                self.a = vector2D(target.x - self.l*math.cos(math.radians(self.angle)),target.y - self.l*math.sin(math.radians(self.angle)))
                
        def seek(self,target):
                desired = vector2D(0,0)
                desired.subtract(target,self.b)
                desired.set_mag(self.maxspeed)
                
                self.angle = vector2D(target.x - self.a.x,target.y - self.a.y).get_angle()
                   
                
                steering = vector2D(0,0)
                steering.subtract(desired,self.vel)
                steering.limit(self.maxacc)
                
                self.acc.add(steering)
               
        def show(self):
                pygame.draw.line(screen,(0,0,0),(self.a.x,self.a.y),(self.b.x,self.b.y),self.weight)                

#################################################################################

def setup():
        global screen, scr_width, scr_height
        global line
        screen = pygame.display.set_mode((scr_width,scr_height))
        no = 50
        for i in range(no):        
                line.append(Segment(scr_width/2,scr_height/2,10,1))
        
def draw():
        
        global screen, scr_width, scr_height
        global line
        screen.fill((255,255,255))
        for i in range(len(line)):
                if i == 0:
                        line[i].seek(vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))
                        
                else:
                        line[i].follow(line[i-1].a)
                line[i].update()
                line[i].show()
                        
        
        pygame.display.flip()
        
#################################################################################

setup()
running = True
while running:
        # Quiting program when pygame window is closed
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
                        running = False
        draw()
        pygame.display.update()
         
        fpsClock.tick(fps)       
