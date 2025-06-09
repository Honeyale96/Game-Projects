import pygame

from fighter import Fighter

# -----------------------
# Game Configuration
# -----------------------
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL
FPS = 60

# -----------------------
# Initializations
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle")

# Load images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()


# -----------------------
# Helper Functions
# -----------------------

def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))

# -----------------------
# Game Objects
# -----------------------


knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)


bandit_list = [bandit1, bandit2]
# -----------------------
# Game Loop
# -----------------------
run = True
while run:

    clock.tick(FPS)

    # Draw onto screen
    draw_bg()
    draw_panel()
    # draw fighters
    knight.draw(screen)
    for bandit in bandit_list:
        bandit.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()
pygame.quit()