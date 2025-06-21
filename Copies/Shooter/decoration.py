import pygame

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, tile_size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, tile_size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, tile_size, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
