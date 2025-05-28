import pygame
from pygame.locals import *
import random

from bird import Bird
from pipe import Pipe
from scoreboard import Scoreboard
from button import Button

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 664
SCREEN_HEIGHT = 736
FPS = 60
SCROLL_SPEED = 4  # Speed at which the ground and pipes move
PIPE_GAP = 150  # Space between the top and bottom pipes
PIPE_FREQUENCY = 1500  # Time (in milliseconds) between pipe spawns
GROUND_HEIGHT = 568  # Y position of the ground

# -----------------------
# Initialization
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption('Flappy Bird')  # Set window title

# Load Images
bg = pygame.image.load('img/bg.png')  # Load background image
ground_img = pygame.image.load('img/ground.png')  # Load ground image
button_img = pygame.image.load('img/restart.png')  # Load restart button image

# Load Sound Effects
coin_sound = pygame.mixer.Sound('sounds/coin.wav')  # Load scoring sound

# Sprite Groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Create Bird instance
flappy = Bird(100, SCREEN_HEIGHT // 2)
bird_group.add(flappy)

# Font & Colors
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)
black = (0, 0, 0)

# Create Scoreboard and Restart Button
scoreboard = Scoreboard(20, 20, font, black, coin_sound)
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, button_img)

# Game State Variables
ground_scroll = 0  # Used to animate ground movement
game_over = False
last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
PASS_PIPE = False  # To detect passing through pipes

# -----------------------
# Helper Functions
# -----------------------

def draw_background():
    """Draw background, bird, pipes, and ground"""
    screen.blit(bg, (0, 0))  # Draw background
    bird_group.draw(screen)  # Draw bird(s)
    pipe_group.draw(screen)  # Draw all pipes
    screen.blit(ground_img, (ground_scroll, GROUND_HEIGHT))  # Draw ground

def check_collisions():
    """Check for collisions with pipes or ground"""
    global game_over  # So we can permanently set it
    if game_over:
        return True  # If already game over, don't recheck
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        flappy.flying = False  # Stop bird from flapping
        return True  # Collision with pipe
    if flappy.rect.bottom >= GROUND_HEIGHT:
        flappy.flying = False
        return True  # Bird hit ground
    return False


def check_score():
    """Check if bird passed through pipe and update score"""
    global PASS_PIPE
    if len(pipe_group) > 0:
        bird = bird_group.sprites()[0]
        pipe = pipe_group.sprites()[0]
        if bird.rect.left > pipe.rect.left and bird.rect.right < pipe.rect.right and not PASS_PIPE:
            PASS_PIPE = True
        if PASS_PIPE and bird.rect.left > pipe.rect.right:
            scoreboard.increment()
            PASS_PIPE = False

def countdown():
    """Display 3-2-1 countdown at restart"""
    for num in range(3, 0, -1):
        screen.blit(bg, (0, 0))
        screen.blit(ground_img, (0, GROUND_HEIGHT))
        countdown_text = font.render(str(num), True, white)
        text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.update()
        pygame.time.delay(1000)  # Wait 1 second per number

def reset_game():
    """Reset the game state"""
    global PASS_PIPE
    pipe_group.empty()  # Remove all pipes
    flappy.rect.x = 100  # Reset bird position
    flappy.rect.y = SCREEN_HEIGHT // 2
    flappy.vel = 0  # Reset velocity
    scoreboard.score = 0  # Reset score
    countdown()  # Show countdown before resuming

# -----------------------
# Game Loop
# -----------------------
run = True
while run:
    clock.tick(FPS)
    draw_background()  # Draw game elements
    bird_group.update(game_over)
    if not game_over:
        pipe_group.update()

    game_over = check_collisions()  # Update collision state

    if not game_over and flappy.flying:
        # Create pipes when game starts
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            middle_y = SCREEN_HEIGHT // 2 + pipe_height
            pipe_group.add(Pipe(SCREEN_WIDTH, middle_y, -1, PIPE_GAP, SCROLL_SPEED))  # Bottom
            pipe_group.add(Pipe(SCREEN_WIDTH, middle_y, 1, PIPE_GAP, SCROLL_SPEED))   # Top
            last_pipe = time_now

        ground_scroll -= SCROLL_SPEED
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        check_score()  # Check if bird passed pipe

    # Handle Events
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        # Only allow start input if game is NOT over
        if not game_over:
            if (event.type == MOUSEBUTTONDOWN or
                (event.type == KEYDOWN and event.key == K_SPACE)) and not flappy.flying:
                flappy.flying = True

    # If game over, show restart button
    if game_over:
        if button.draw(screen):
            game_over = False
            reset_game()

    scoreboard.draw(screen)  # Draw the score
    pygame.display.update()  # Refresh screen

pygame.quit()
