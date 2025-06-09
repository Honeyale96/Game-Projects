import pygame

class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        image = pygame.image.load(f'img/{self.name}/Idle/0.png')
        self.image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


    def draw(self, screen):
        screen.blit(self.image, self.rect)