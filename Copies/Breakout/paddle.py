import pygame
from pygame import Rect


class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, columns):
        super().__init__()
        self.columns = columns
        self.height = 20
        self.width = screen_width // columns
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self, screen_width):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self, screen, paddle_color, paddle_outline):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)