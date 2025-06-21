import pygame
import os
import random

from bullet import Bullet

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, obstacle_list, level_length):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1  # 1=right -1=left
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0     # 0=Idle 1=Run 2=Jump  3=Death
        self.update_time = pygame.time.get_ticks()
        self.obstacle_list = obstacle_list
        self.level_length = level_length

        # AI specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # Load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            # Creates a temp list to store Idle images
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)   # Add temp list to animation list as index [0]

        # Access the list of self.action and the frames within that list
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right, gravity, screen_width, scroll_threshold, bg_scroll, tile_size):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        self.in_air = True

        # horizontal collision check
        self.rect.x += dx
        for tile in self.obstacle_list:
            if tile[1].colliderect(self.rect):
                if dx > 0:  # moving right
                    self.rect.right = tile[1].left
                if dx < 0:  # moving left
                    self.rect.left = tile[1].right

        # vertical collision check
        self.rect.y += dy
        for tile in self.obstacle_list:
            if tile[1].colliderect(self.rect):
                if dy > 0:  # falling
                    self.rect.bottom = tile[1].top
                    self.vel_y = 0
                    self.in_air = False
                elif dy < 0:  # jumping
                    self.rect.top = tile[1].bottom
                    self.vel_y = 0

        # check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                dx = 0

        # update scroll based on player position
        if self.char_type == 'player':
            if ((self.rect.right > screen_width - scroll_threshold and bg_scroll < (self.level_length * tile_size - screen_width))
                    or self.rect.left < scroll_threshold and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll



    def ai_move(self, moving_left, moving_right, gravity):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        self.in_air = True

        # horizontal collision check
        self.rect.x += dx
        for tile in self.obstacle_list:
            if tile[1].colliderect(self.rect):
                if dx > 0:  # moving right
                    self.rect.right = tile[1].left
                    self.direction *= -1  # turn left
                    self.move_counter = 0
                if dx < 0:  # moving left
                    self.rect.left = tile[1].right
                    self.direction *= 1  # turn right
                    self.move_counter = 0

        # vertical collision check
        self.rect.y += dy
        for tile in self.obstacle_list:
            if tile[1].colliderect(self.rect):
                if dy > 0:  # falling
                    self.rect.bottom = tile[1].top
                    self.vel_y = 0
                    self.in_air = False
                elif dy < 0:  # jumping
                    self.rect.top = tile[1].bottom
                    self.vel_y = 0


    def shoot(self, bullet_group, bullet_img):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(bullet_img, self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),
                            self.rect.centery, self.direction, self.obstacle_list)
            bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1

    def ai(self, player, gravity, tile_size, bullet_group, bullet_img, screen_scroll):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)   # 0=Idle
                self.idling = True
                self.idling_counter = 50
            # check if the AI is near player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)   # 0=Idle
                self.shoot(bullet_group, bullet_img)
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.ai_move(ai_moving_left, ai_moving_right, gravity)
                    self.update_action(1)   # 1=Run
                    self.move_counter += 1
                    # update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    # pygame.draw.rect(screen, RED, self.vision)    USE FOR SEEING AI VISION BOX

                    if self.move_counter > tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # update animation
        animation_cooldown = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation runs out reset to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)