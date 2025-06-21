import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, x, y, direction, obstacle_list):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.obstacle_list = obstacle_list

    def update(self, screen_width, bullet_group, enemy_group, player, screen_scroll):
        # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        # check for collision with level
        for tile in self.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # check collision with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()