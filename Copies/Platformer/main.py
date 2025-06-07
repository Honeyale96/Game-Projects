import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

from button import Button
from coin import Coin
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
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

# Load Background Images
bg_img = pygame.image.load('img/sky.png')
sun_img = pygame.image.load('img/sun.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# Load Sounds
pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('sounds/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
game_over_fx.set_volume(0.5)

# Define Font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Define Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Game Variables
game_over = 0
main_menu = True
level = 0
max_levels = 7
score = 0

# -----------------------
# Helper Functions
# -----------------------
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
        pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))

def draw_text(text, font,  text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x + 10, y))


def reset_level(level):
    global world_data
    player.reset(100, (SCREEN_HEIGHT - 130))
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    # load in level data and create world
    if path.exists(f'level_data/level{level}_data'):
        pickle_in = open(f'level_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data, TILE_SIZE, blob_group, lava_group, coin_group, exit_group, platform_group)
    return world

# -----------------------
# Create Game Objects
# -----------------------
# Create Groups
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Create dummy coin for showing the score
score_coin = Coin(TILE_SIZE // 2, TILE_SIZE // 2 + 10, TILE_SIZE)
coin_group.add(score_coin)

# Create Player
player = Player(100, (SCREEN_HEIGHT - 130))
# Load in level_data and create world
if path.exists(f'level_data/level{level}_data'):
    pickle_in = open(f'level_data/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data, TILE_SIZE, blob_group, lava_group, coin_group, exit_group, platform_group)

# Create Buttons
restart_button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, restart_img)
start_button = Button(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 25, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 80, SCREEN_HEIGHT // 2 - 25, exit_img)

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
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            # update score - check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_fx.play()
                score += 1
            draw_text("X " + str(score), font_score, white, TILE_SIZE - 10, 10)


        game_over = player.update(screen, SCREEN_HEIGHT, world, blob_group, lava_group, exit_group,
                                  game_over, jump_fx, game_over_fx)

        #if player has died
        if game_over == -1:
            if restart_button.draw(screen):
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        #if player has completed a level
        if game_over == 1:
            # reset game and go to next level
            level += 1
            if level <= max_levels:
                # reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, blue, (SCREEN_WIDTH // 2) - 140, SCREEN_HEIGHT // 2 + 100)
                # restart game
                if restart_button.draw(screen):
                    level = 1
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0


    # draw_grid()  # Uncomment to see grid lines

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Cleanup
pygame.quit()