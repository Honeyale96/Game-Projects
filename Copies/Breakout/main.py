import pygame
from pygame.locals import *

from wall import Wall

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# -----------------------
# Initialization
# -----------------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption('Breakout')  # Set window title

# Define Colors
bg = (234, 218, 184)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

# Game Variables
columns = 6
rows = 6

# Instances
wall = Wall(SCREEN_WIDTH, columns, rows)
wall.create_wall()

# -----------------------
# Game Loop
# -----------------------
run = True
while run:
    screen.fill(bg)
    wall.draw_wall(screen, block_red, block_green, block_blue, bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
