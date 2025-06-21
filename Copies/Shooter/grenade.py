import pygame

from explosion import Explosion

class Grenade(pygame.sprite.Sprite):
    def __init__(self, grenade_img, x, y, direction, obstacle_list):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction
        self.obstacle_list = obstacle_list

    def update(self, screen_width, tile_size, gravity, explosion_group, enemy_group, player):
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        # check for collision with level
        for tile in self.obstacle_list:
            # check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
                # check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # check if below the ground i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom


        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            # do damage to player if nearby
            if abs(self.rect.centerx - player.rect.centerx) < tile_size * 2 and \
                abs(self.rect.centery - player.rect.centery) < tile_size * 2:
                player.health -= 50
            for enemy in enemy_group:
                # do damage to enemy if nearby
                if abs(self.rect.centerx - enemy.rect.centerx) < tile_size * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < tile_size * 2:
                    enemy.health -= 50
