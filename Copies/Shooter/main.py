import pygame
from pygame import mixer
import csv
import button
from grenade import Grenade
from screenfade import ScreenFade
from world import World

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
FPS = 60

# Game Variables
GRAVITY = 0.75
SCROLL_THRESHOLD = 200
ROWS = 16
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 0
start_game = False
start_intro = False

# Define Colors
BG = (144,201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

# -----------------------
# Initializations
# -----------------------
mixer.init()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

# Define Font
font = pygame.font.SysFont('Futura', 30)

# Load Music and Sounds
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.3)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.3)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.3)


# Load Images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# collectibles
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health'    :   health_box_img,
    'Ammo'      :   ammo_box_img,
    'Grenade'   :   grenade_box_img
}

# Define Player Action Variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# -----------------------
# Helper Functions
# -----------------------

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    # infinite scrolling and parallex scrolling
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_text (text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLUMNS
        data.append(r)
    return data


# -----------------------
# Game Objects
# -----------------------

# Create Buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# Groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)


# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    world_data.append(r)
# Load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(TILE_SIZE, world_data, img_list,
                                        enemy_group, item_box_group, decoration_group,
                                        water_group, exit_group, item_boxes)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    if not start_game:
        # main menu
        screen.fill(BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:

        # Update background
        draw_bg()
        # Draw world map
        world.draw(screen, screen_scroll)
        health_bar.draw(screen, RED, GREEN, BLACK, player.health)
        draw_text('AMMO: ', font, WHITE, 10, 30)
        for x in range(player.ammo):
            screen.blit(bullet_img, (130 + (x * 10), 50))
        draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (190 + (x * 15), 75))

        # Updates
        player.update()
        player.draw(screen)
        for enemy in enemy_group:
            enemy.ai(player, GRAVITY, TILE_SIZE, bullet_group, bullet_img, screen_scroll, shot_fx)
            enemy.update()
            enemy.draw(screen)

        # Update and draw groups
        bullet_group.update(SCREEN_WIDTH, bullet_group, enemy_group, player, screen_scroll)
        bullet_group.draw(screen)
        grenade_group.update(SCREEN_WIDTH, TILE_SIZE, GRAVITY, explosion_group,
                             enemy_group, player, screen_scroll, grenade_fx)
        grenade_group.draw(screen)
        explosion_group.update(screen_scroll)
        explosion_group.draw(screen)
        item_box_group.update(player,screen_scroll)
        item_box_group.draw(screen)
        decoration_group.update(screen_scroll)
        decoration_group.draw(screen)
        water_group.update(screen_scroll)
        water_group.draw(screen)
        exit_group.update(screen_scroll)
        exit_group.draw(screen)

        # Show Intro
        if start_intro:
            if intro_fade.fade(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
                start_intro = False
                intro_fade.fade_counter = 0


        # Update player actions
        if player.alive:
            if shoot:
                player.shoot(bullet_group, bullet_img, shot_fx)
            # throw grenades
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(grenade_img, player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction, world.obstacle_list)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)  # 2=Jump
            elif moving_left or moving_right:
                player.update_action(1) # 1=Run
            else:
                player.update_action(0) # 0=Idle
            screen_scroll, level_complete = player.move(moving_left, moving_right, GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_THRESHOLD,
                                        bg_scroll, TILE_SIZE, water_group, exit_group)
            bg_scroll -= screen_scroll
            # check if player completed level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player, health_bar = world.process_data(TILE_SIZE, world_data, img_list,
                                                            enemy_group, item_box_group, decoration_group,
                                                            water_group, exit_group, item_boxes)
        else:
            screen_scroll = 0
            if death_fade.fade(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player, health_bar = world.process_data(TILE_SIZE, world_data, img_list,
                                                            enemy_group, item_box_group, decoration_group,
                                                            water_group, exit_group, item_boxes)

    # Event Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_j:
                shoot = True
            if event.key == pygame.K_k:
                grenade = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_j:
                shoot = False
            if event.key == pygame.K_k:
                grenade = False
                grenade_thrown = False


    pygame.display.update()
pygame.quit()