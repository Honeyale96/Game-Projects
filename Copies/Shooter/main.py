import pygame

from grenade import Grenade
from healthbar import HealthBar
from items import ItemBox
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

# Load Images
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
# collectibles
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health'    :   health_box_img,
    'Ammo'      :   ammo_box_img,
    'Grenade'   :   grenade_box_img
}

# Define Colors
BG = (144,201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


# Define Font
font = pygame.font.SysFont('Futura', 30)

# Game Variables
GRAVITY = 0.75
TILE_SIZE = 40

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
    pygame.draw.line(screen, RED, (0,300), (SCREEN_WIDTH, 300))

def draw_text (text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

# -----------------------
# Game Objects
# -----------------------

# Groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

# Temp - create item boxes
item_box = ItemBox('Health', TILE_SIZE, item_boxes, 100, 260)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', TILE_SIZE, item_boxes, 400, 260)
item_box_group.add(item_box)
item_box = ItemBox('Grenade',TILE_SIZE, item_boxes, 500,260)
item_box_group.add(item_box)

# Instances
player = Soldier('player', 200, 200, 3, 5, 20, 5)
health_bar = HealthBar(10, 10, player.health, player.health)

enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)
enemy_group.add(enemy)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    # Draw
    draw_bg()
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
        enemy.update()
        enemy.draw(screen)

    # Update and draw groups
    bullet_group.update(SCREEN_WIDTH, bullet_group, enemy_group, player)
    bullet_group.draw(screen)
    grenade_group.update(SCREEN_WIDTH, TILE_SIZE, GRAVITY, explosion_group, enemy_group, player)
    grenade_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)
    item_box_group.update(player)
    item_box_group.draw(screen)

    # Update player actions
    if player.alive:
        if shoot:
            player.shoot(bullet_group, bullet_img)
        # throw grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(grenade_img, player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            player.grenades -= 1
            grenade_thrown = True
        if player.in_air:
            player.update_action(2)  # 2=Jump
        elif moving_left or moving_right:
            player.update_action(1) # 1=Run
        else:
            player.update_action(0) # 0=Idle
        player.move(moving_left, moving_right, GRAVITY)

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