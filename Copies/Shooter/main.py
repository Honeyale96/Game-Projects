import pygame

from player import Soldier

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
FPS = 60

# -----------------------
# Initializations
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

# Game Variables

# -----------------------
# Helper Functions
# -----------------------


# -----------------------
# Game Objects
# -----------------------

player = Soldier(200, 200, 3)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()
pygame.quit()