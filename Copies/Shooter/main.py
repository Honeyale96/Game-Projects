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

# Load Images
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# Define Colors
BG = (144,201, 120)
RED = (255, 0, 0)

# Game Variables
GRAVITY = 0.75

# Define Player Action Variables
moving_left = False
moving_right = False
shoot = False

# -----------------------
# Helper Functions
# -----------------------

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0,300), (SCREEN_WIDTH, 300))


# -----------------------
# Game Objects
# -----------------------

# Groups
bullet_group = pygame.sprite.Group()

# Instances
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    draw_bg()

    # Updates
    player.update()
    player.draw(screen)
    enemy.update()
    enemy.draw(screen)

    # Update and draw groups
    bullet_group.update(SCREEN_WIDTH, bullet_group, player, enemy)
    bullet_group.draw(screen)

    # Update player actions
    if player.alive:
        if shoot:
            player.shoot(bullet_group, bullet_img)
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
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False


    pygame.display.update()
pygame.quit()