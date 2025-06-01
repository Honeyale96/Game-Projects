import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load('img/guy1.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False

    def update(self, screen, screen_height):
        dx = 0
        dy = 0
        # Player Movement
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE] :
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
                self.vel_y = 10
        dy += self.vel_y
        # check for collision

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)