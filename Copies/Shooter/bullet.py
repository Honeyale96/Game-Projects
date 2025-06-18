import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self, screen_width, bullet_group, enemy_group, player):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > screen_width:
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