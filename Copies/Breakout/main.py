import pygame
from pygame.locals import *

from ball import Ball
from paddle import Paddle
from wall import Wall

# -----------------------
# Game Configuration
# -----------------------
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

# -----------------------
# Initialization
# -----------------------
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the game window
pygame.display.set_caption('Breakout')  # Set window title


# Define Colors
bg = (234, 218, 184)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

# Text Colors
font = pygame.font.SysFont('Constantia', 30)
text_color = (78, 81, 139)

# Game Variables
columns = 6
rows = 6
live_ball = False
game_over = 0


# Instances
wall = Wall(SCREEN_WIDTH, columns, rows)
wall.create_wall()
paddle = Paddle(SCREEN_WIDTH, SCREEN_HEIGHT, columns)
ball = Ball(paddle.x + (paddle.width // 2), paddle.y - paddle.height)

# -----------------------
# Helper Function
# -----------------------
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# -----------------------
# Game Loop
# -----------------------
run = True
while run:
    clock.tick(FPS)
    screen.fill(bg)

    # Draw all objects
    wall.draw_wall(screen, block_red, block_green, block_blue, bg)
    paddle.draw(screen, paddle_color, paddle_outline)
    ball.draw(screen, paddle_color, paddle_outline)

    if live_ball:
        paddle.move(SCREEN_WIDTH)
        game_over = ball.move(SCREEN_WIDTH, SCREEN_HEIGHT, paddle, wall)
        if game_over != 0:
            live_ball = False

    # Print player instructions
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, SCREEN_HEIGHT // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_color, 240, SCREEN_HEIGHT // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, SCREEN_HEIGHT // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_color, 240, SCREEN_HEIGHT // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_color, 100, SCREEN_HEIGHT // 2 + 100)

    # Run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(paddle.x + (paddle.width // 2), paddle.y - paddle.height)
            paddle.reset()
            wall.create_wall()

    pygame.display.update()
pygame.quit()
