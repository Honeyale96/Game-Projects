import pygame
import random

from dino import Dino
from obstacle import Obstacle

# -----------------------
# Game Configuration
# -----------------------
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 490
FPS = 60
SCROLL_SPEED = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run")


# -----------------------
# Initializations
# -----------------------

# Loading images
ground_image = pygame.image.load("Assets/images/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# Adding Parallax Images to list
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"Assets/images/plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

scroll = 0

# Initialize Dino
ground = SCREEN_HEIGHT - (ground_height - 10)
dino = Dino(150, ground, SCROLL_SPEED)
obstacles = []  # Start with no obstacles
obstacle_timer = 0  # Time until next obstacle


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

    # Auto-Run
    scroll += SCROLL_SPEED

    # Obstacle Spawning
    obstacle_timer -= 1  # Countdown timer for next obstacle

    if obstacle_timer <= 0:
        # Pick a random type
        obstacle_type = random.choice(["stump", "stone", "bird"])
        # Spawn just off-screen
        new_x = scroll + SCREEN_WIDTH + 100
        obstacles.append(Obstacle(obstacle_type, new_x, SCREEN_HEIGHT - ground_height))
        # reduce delay as player runs further
        distance = scroll // 2000  # How far player has run
        min_delay = max(20, 60 - distance * 5)  # Lower limit: 20
        max_delay = max(min_delay + 10, 100 - distance * 10)  # Still some randomness

        obstacle_timer = random.randint(min_delay, max_delay)

    keys = pygame.key.get_pressed()
    dino.update(keys)

    # Draw world
    draw_bg()
    draw_ground()

    # Update and draw obstacles
    for obstacle in obstacles[:]:
        obstacle.update(SCROLL_SPEED)  # Move with the scroll
        obstacle.draw(screen, scroll)
        # Remove obstacle if it's completely off-screen (to save memory)
        if obstacle.world_x - scroll + obstacle.rect.width < 0:
            obstacles.remove(obstacle)

    dino.draw(screen, scroll)

    # Collision detection
    dino_rect = dino.get_rect(scroll)  # Dino's hitbox
    for obstacle in obstacles:
        obstacle_rect = obstacle.get_rect(scroll)  # Obstacle's screen-space hitbox
        if dino_rect.colliderect(obstacle_rect):  # If they overlap
            print("Hit!")  # TEMP — Later: lose health, restart, etc.


    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            dino.jump()

    pygame.display.update()
pygame.quit()

