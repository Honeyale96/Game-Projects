import pygame

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size //2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
