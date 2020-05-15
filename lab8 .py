#import required modules
import pygame as pg
import sys
import math, random
from math import cos, sin, pi



#Screen Dimensions
WIDTH, HEIGHT = 1200, 1100
FPS = 60

#Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (176, 58, 46)
GREEN = (94, 176, 46)
LIGHTBLUE = (173,216,230)
YELLOW =(255,255,0)

def draw_sun(surface, color, x, y, size): 
        pg.draw.circle(surface, YELLOW, (x, y), size) #draws a circle with x,y and size that'll be defined at the end

def draw_moon(surface, color, x, y, size):
        pg.draw.circle(surface, GREY, (x, y), size)#draws a circle with x,y that'll be defined at the end

def xy_elliptical(degrees, center_x, center_y, radius, stretch_x = 1, stretch_y = 1):
    """A function that returns (x, y) coordinates
       for a point traveling on a circular/elliptical path

       degrees: number of degrees (0 - 360) through rotation
       center_x: x coordinate of rotational center
       center_y: y coordinate of rotational center
       radius:   radius of circular path to travel
       stretch_x: amount of horizontal stretch (for elliptical path)
       stretch_y: amount of vertical stretch (for elliptical path)"""

    radians = degrees / (2 * pi)
    x = int(center_x + stretch_x * radius * cos(radians))
    y = int(center_y - stretch_y * radius * sin(radians))

    return (x, y)

def add_shading(color, shading, max_shading = 255): #function to make the gradually darker.
    shading = min(shading, max_shading)
    return (max(0, color[0] - shading),
            max(0, color[1] - shading),
            max(0, color[2] - shading))

def get_crowd(): #function to get crowd
        crowd = [] #makes a list
        for i in range(200): 
                x = random.randrange(0, WIDTH) #where along the x-axis should the crowd spawn
                y = random.randrange(300, 480) #what is the y-axis limit for them to spawn
                crowd.append((x, y)) #puts necessary x,y coordinates into crowd 
        return crowd

def draw_stick_figure(screen, x, y, size):
    #x, y is the center of the chest
    #size is the width of the chest

    chest_width = size
    chest_height = chest_width * 1.5
    pg.draw.rect(screen, BLACK,
                 (int(x - chest_width / 2),  #left side of rectangle
                  int(y - chest_height / 2), #top side of the rectangle
                  chest_width,           #width of rectangle
                  chest_height), 1)         #height of rectangle
    head_x = x
    head_r = int(chest_width / 2)
    head_y = int(y - chest_height / 2) - head_r
    pg.draw.circle(screen, BLACK, (head_x, head_y), head_r, 1)#head of figure

    leg_width = int(size / 3) #leg of figure
    leg_length = chest_height
    left_leg_x = int(x - chest_width / 2)
    left_leg_y = int(y + chest_height / 2)

    right_leg_x = int(left_leg_x + (2 / 3) * chest_width)
    right_leg_y = left_leg_y #leg of figure

    line_start_x = x+2  #right arm
    line_start_y = y-6
    line_end_x = line_start_x + 50
    line_end_y = line_start_y

    line2_end_x = -x+2  #left arm
    line2_start_x = x - 50

   #draws legs
    pg.draw.rect(screen, BLACK, (left_leg_x, left_leg_y, leg_width, leg_length), 1) 
    pg.draw.rect(screen, BLACK, (right_leg_x, right_leg_y, leg_width, leg_length), 1)
   #draws arms
    pg.draw.line(screen,BLACK, (line_start_x,line_start_y), (line_end_x,line_end_y))
    pg.draw.line(screen,BLACK, (line2_start_x,line_start_y), (line_end_x,line_end_y))



    
#Pygame setup
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()



#speed at which each figure on the track will move
speed_r = random.randint(2, 6)#random.randint chooses a random integer between 2 numbers
speed_b = random.randint(2, 6)
speed_g =random.randint(2, 6)
speed_h = random.randint(2, 6)
speed_i = random.randint(2, 6)

#offsets required to move elements like the figure
offset_r = 0
offset_b = 0
offset_g = 0
offset_h = 0
offset_i = 0

crowd_timer = 0
crowd = []
degrees = 0

while True:
    
    #Event loop keeps display up until "X" is clicked
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


    #Update
    offset_r += speed_r
    offset_b += speed_b
    offset_g += speed_g
    offset_h += speed_h
    offset_i += speed_i
    crowd_timer += 1

      #controls movement for the figures on the track
    if offset_r > WIDTH + 100:
        offset_r = - 500

    if offset_b > WIDTH + 100:
        offset_b = - 500

    if offset_g > WIDTH + 100:
        offset_g = - 500
        
    if offset_h > WIDTH + 100:
        offset_h = - 500
        
    if offset_i > WIDTH + 100:
        offset_i = - 500

    degrees += .1
    (sun_x, sun_y) = xy_elliptical(degrees, WIDTH // 2, HEIGHT // 2, WIDTH // 2, stretch_y=.9) # sun rotation
    (moon_x, moon_y) = xy_elliptical(degrees + 180, WIDTH // 2, HEIGHT // 2, WIDTH // 2, stretch_y=.9) # moon rotation
    black_degree = int(.2 * sun_y) #the degree to which it will make sky_color darker
    sky_color = add_shading(LIGHTBLUE, black_degree)#gradually makes sky_color darker

    #Draw

    pg.draw.rect(screen,sky_color,[0,0,1200,280])
    
    #draws the sun and moon
    draw_sun(screen, YELLOW, sun_x, sun_y, 50)
    draw_moon(screen, GREY, moon_x, moon_y, 30)

    pg.draw.rect(screen, RED,[0,280,WIDTH,HEIGHT])

    
    if crowd_timer == 10: #limit
            crowd_timer = 0
            crowd = get_crowd()

    for (x, y) in crowd: #draws stick figure with the help of x,y coordinates specified above.
            draw_stick_figure(screen, x, y, 12)
          
    #Calls the functions and pre-made pygame methods.    
    pg.draw.line(screen,WHITE,(0,500),(9000,500),6)
    pg.draw.line(screen,WHITE,(0,600),(9000,600),6)
    pg.draw.line(screen,WHITE,(0,700),(9000,700),6)
    pg.draw.line(screen,WHITE,(0,800),(9000,800),6)
    pg.draw.line(screen,WHITE,(0,900),(9000,900),6)

    draw_stick_figure(screen, 75+ offset_i, 549, 25)
    draw_stick_figure(screen, 75+ offset_r, 649, 25)
    draw_stick_figure(screen, 75+ offset_g, 749, 25)
    draw_stick_figure(screen, 75+ offset_h, 849, 25)
    draw_stick_figure(screen, 75+ offset_b, 949, 25)
    
    pg.draw.rect(screen,GREEN,[1,1000,1200,1200])

           

            
    pg.display.update() #updates display
    clock.tick(FPS) 
