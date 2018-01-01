import pygame,sys
import math
import robohat,time
from pygame.math import Vector2
from pygame.locals import *

speed = 30
print ("Tests the motors by using the arrow keys to control")
print ("Use , or < to slow down")
print ("Use . or > to speed up")
print ("Speed changes take effect when the next arrow key is pressed")
print ("Press Ctrl-C to end")
robohat.init()

pygame.init()
WIDTH = 300
HEIGHT = 300
DISPLAYSURF=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Brain')

#tank = Tank()

while 1:
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
         #               if event.key == pygame.K_LEFT:
         #                        
         #               if event.key == pygame.K_RIGHT:
         #                        
         #               if event.key == pygame.K_UP:
         #                   
         #               if event.key == pygame.K_DOWN:
                            
        #pygame.display.update()


class Tank():  
        def __init__(self):
                print("created tank")


#        def forward():
#                robohat.forward
