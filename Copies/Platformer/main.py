import pygame
from pygame.locals import *

from button import Button
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
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Game Variables
game_over = 0
main_menu = True

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
restart_button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, restart_img)
start_button = Button(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 25, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2 - 25, exit_img)

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
    if main_menu:
        if exit_button.draw(screen):
            run = False
        if start_button.draw(screen):
            main_menu = False
    else:
        world.draw(screen)
        # --- Update and draw sprites ---
        blob_group.draw(screen)
        lava_group.draw(screen)

        if game_over == 0:
            blob_group.update()

        game_over = player.update(screen, SCREEN_HEIGHT, world, blob_group, lava_group, game_over)

        #if player has died
        if game_over == -1:
            if restart_button.draw(screen):
                player.reset(100, (SCREEN_HEIGHT - 130))
                game_over = 0

    # draw_grid()  # Uncomment to see grid lines

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Cleanup
pygame.quit()