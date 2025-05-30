import pygame
from pygame.locals import *

# -----------------------
# Game Configurations
# -----------------------
screen_width = 1000
screen_height = 800


# -----------------------
# Initializations
# -----------------------
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('')

# Game variables
tile_size = 50


# -----------------------
# Helper Function
# -----------------------
def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


# -----------------------
# Game Loop
# -----------------------
run = True
while run:

	draw_grid()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	pygame.display.update()
pygame.quit()