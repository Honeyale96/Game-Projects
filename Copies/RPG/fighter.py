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
        self.animation_list = []
        self.frame_index = 0
        self.action = 0     # 0=idle, 1=attack, 2=hurt, 3=dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(8):
            image = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            temp_list.append(image)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown = 100
        # Handle animations
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def draw(self, screen):
        screen.blit(self.image, self.rect)