import pygame

from dino import Dino

# -----------------------
# Game Configuration
# -----------------------
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 490
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")


# -----------------------
# Initializations
# -----------------------
ground_image = pygame.image.load("Assets/images/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"Assets/images/plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

scroll = 0

ground_y = SCREEN_HEIGHT - (ground_height - 10)
dino = Dino(200, ground_y)

# -----------------------
# Helper Functions
# -----------------------
def draw_bg():
    for index, img in enumerate(bg_images):
        speed = 1 + index * 0.2                     # increasing speeds for each bg layer
        offset = (-scroll * speed) % bg_width
        x = offset - bg_width
        while x < SCREEN_WIDTH:
            screen.blit(img, (x, 0))
            x += bg_width

def draw_ground():
    speed = 2.5
    offset = (-scroll * speed) % ground_width
    x = offset - ground_width
    while x < SCREEN_WIDTH:
        screen.blit(ground_image, (x, SCREEN_HEIGHT - ground_height))
        x += ground_width


# -----------------------
# Game Loop
# -----------------------
run = True
while run:
    clock.tick(FPS)

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        scroll += 3

    dino.update(keys)

    # Draw world
    draw_bg()
    draw_ground()

    dino.draw(screen, scroll)


    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

