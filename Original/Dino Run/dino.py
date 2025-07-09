import pygame
from spritesheet import SpriteSheet

BLACK = (0, 0, 0)

class Dino(pygame.sprite.Sprite):
    animation_steps = [4, 6, 3, 4, 7]  # idle, run, jump, hurt, crouch
    IDLE, RUN, JUMP, HURT, CROUCH = range(5)

    def __init__(self, x, ground_y):
        super().__init__()
        # Load dino images
        sprite_sheet_image = pygame.image.load("Assets/images/doux.png").convert_alpha()
        self.sheet = SpriteSheet(sprite_sheet_image)

        # Create animation list
        self.animation_list = []
        frame_index = 0
        # loop to add animation steps into a temp list -> animation list
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sheet.get_image(frame_index, 24, 24, 3, BLACK))
                frame_index += 1
            self.animation_list.append(temp_img_list)


        self.action = self.IDLE
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = ground_y
        self.ground_y = ground_y

    def draw(self, surface, scroll):

        surface.blit(self.image, (self.rect.x - scroll, self.rect.y))

    def _update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame = (self.frame + 1) % len(self.animation_list[self.action])
            self.last_update = current_time
        self.image = self.animation_list[self.action][self.frame]



