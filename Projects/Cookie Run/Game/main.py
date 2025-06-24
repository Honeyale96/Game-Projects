import pygame
from pygame.locals import *
from Game.manager import GameManager

# -----------------------
# Initializations
# -----------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption('Cookie Run')  # Set window title

game = GameManager(screen)

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

    game.update(FPS)
    game.draw()

    pygame.display.update()  # Refresh screen
pygame.quit()