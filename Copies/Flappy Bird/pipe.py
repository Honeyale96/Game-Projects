import pygame

TOP_PIPE = 1
BOTTOM_PIPE = -1

# Define the Pipe class as a Sprite
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap, scroll_speed):
        super().__init__()
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        self.scroll_speed = scroll_speed

        if position == TOP_PIPE:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        else:
            self.rect.topleft = (x, y + pipe_gap // 2)

    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()

