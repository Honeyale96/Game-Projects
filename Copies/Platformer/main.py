import pygame
from pygame.locals import *

from player import Player
from world import World

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 40


# -----------------------
# Initialization
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

# Load Background Images
bg_img = pygame.image.load('img/sky.png')
sun_img = pygame.image.load('img/sun.png')

# -----------------------
# Level Data (Map)
# -----------------------
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# -----------------------
# Create Game Objects
# -----------------------
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
player = Player(100, (SCREEN_HEIGHT - 130))
world = World(world_data, TILE_SIZE, blob_group, lava_group)


# -----------------------
# Helper Functions
# -----------------------
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))


# -----------------------
# Game Loop
# -----------------------
run = True
while run:
    clock.tick(FPS)

    # --- Draw Everything ---
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))
    world.draw(screen)
    player.update(screen, SCREEN_HEIGHT, world)
    blob_group.update()
    blob_group.draw(screen)
    lava_group.draw(screen)
    # draw_grid()  # Uncomment to see grid lines

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Cleanup
pygame.quit()