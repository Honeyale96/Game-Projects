import pygame

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y