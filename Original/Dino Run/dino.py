import pygame
from spritesheet import SpriteSheet

BLACK = (0, 0, 0)

class Dino(pygame.sprite.Sprite):
    animation_steps = [4, 6, 3, 4, 7]  # idle, run, jump, hurt, crouch
    IDLE, RUN, JUMP, HURT, CROUCH = range(5)

    def __init__(self, x, ground_y, scroll_speed):
        super().__init__()
        sprite_sheet_image = pygame.image.load("Assets/images/doux.png").convert_alpha()
        self.sheet = SpriteSheet(sprite_sheet_image)

        self.animation_list = []
        frame_index = 0
        for anim_count in self.animation_steps:
            temp = []
            for _ in range(anim_count):
                temp.append(self.sheet.get_image(frame_index, 24, 24, 3, BLACK))
                frame_index += 1
            self.animation_list.append(temp)

        self.action = self.RUN  # always running visually
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.world_x = x  # world position (screen_x = world_x - scroll)
        self.rect.bottom = ground_y
        self.ground_y = ground_y
        self.scroll_speed = scroll_speed
        self.jump_count = 0     # for double jump tracking

        # Jump physics
        self.vel_y = 0
        self.gravity = 0.6
        self.jump_force = -12
        self.on_ground = True

    def update(self, keys):
        prev_action = self.action

        if not self.on_ground:
            self.action = self.JUMP
            self.world_x += 3
        elif keys[pygame.K_DOWN]:
            self.action = self.CROUCH
            self.world_x += 3
        else:
            self.action = self.RUN  # always running visually
            self.world_x += 3

        if self.action != prev_action:
            self.frame = 0

        self._apply_gravity()
        self._update_animation()

    def jump(self):
        if self.jump_count < 2:  # allow double jump
            self.vel_y = self.jump_force
            self.on_ground = False
            self.jump_count += 1

    def draw(self, surface, scroll):
        screen_x = self.world_x - scroll
        surface.blit(self.image, (screen_x, self.rect.y))

    def _apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0  # reset jump count on landing

    def _update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame = (self.frame + 1) % len(self.animation_list[self.action])
            self.last_update = current_time
        self.image = self.animation_list[self.action][self.frame]




