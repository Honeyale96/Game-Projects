import pygame
from pygame.locals import *

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60


# -----------------------
# Initialization
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption('Block Blast')  # Set window title



# -----------------------
# Helper Functions
# -----------------------



# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    # Handle Events
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False


    pygame.display.update()  # Refresh screen
pygame.quit()