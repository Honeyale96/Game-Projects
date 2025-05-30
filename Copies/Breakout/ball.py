import pygame
from pygame import Rect


class Ball():
    def __init__(self, x, y):
        super().__init__()
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.game_over = 0

    def draw(self, screen, paddle_color, paddle_outline):
        pygame.draw.circle(screen, paddle_color,
                           (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline,
                           (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def move(self, screen_width, screen_height):
        #check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        # Check for collision with top and bottom of screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

