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

class Segment():
        def __init__(self,x,y,l,weight):
                self.a = vector2D(x,y)
                self.l = l
                self.angle = 0
                self.weight = weight
                self.b = vector2D(x+l*math.cos(math.radians(self.angle)),y+l*math.sin(math.radians(self.angle)))
                
        def updateB(self):
                self.b = vector2D(self.a.x+self.l*math.cos(math.radians(self.angle)),self.a.y+self.l*math.sin(math.radians(self.angle)))
        
        def update(self):
                self.updateB()
        
        def follow(self,target_x,target_y):
                ang = vector2D(target_x - self.a.x,target_y - self.a.y).get_angle()
                self.angle = ang                       
                self.a = vector2D(target_x - self.l*math.cos(math.radians(self.angle)),target_y - self.l*math.sin(math.radians(self.angle)))
                
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
                        line[i].follow(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                        
                else:
                        line[i].follow(line[i-1].a.x,line[i-1].a.y)
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
