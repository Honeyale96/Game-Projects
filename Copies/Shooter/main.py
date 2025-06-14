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

# Define Colors
BG = (144,201, 120)

# Game Variables

# Define Player Action Variables
moving_left = False
moving_right = False

# -----------------------
# Helper Functions
# -----------------------

def draw_bg():
    screen.fill(BG)


# -----------------------
# Game Objects
# -----------------------

player = Soldier('player', 200, 200, 3, 5)
enemy = Soldier('enemy', 400, 200, 3, 5)

# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.draw(screen)
    enemy.draw(screen)
    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        # keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_ESCAPE:
                run = False


    pygame.display.update()
pygame.quit()