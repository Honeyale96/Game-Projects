import pygame

GRAVITY = 0.5
MAX_FALL_SPEED = 8

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'img/bird{num}.png') for num in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False
        self.flying = False

    def rotate_image(self):
        return pygame.transform.rotate(self.images[self.index], -2 * self.vel)

    def jump(self):
        self.vel = -8

    def update(self, game_over):
        if self.rect.bottom >= 568:
            # If bird has hit the ground, stop animation and movement
            self.image = self.images[self.index]  # Keep current frame
            self.vel = 0
            return  # Skip the rest of the update logic

        self.counter += 1

        if self.counter > 5:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.vel += GRAVITY
        if self.vel > MAX_FALL_SPEED:
            self.vel = MAX_FALL_SPEED
        # Move the bird down if not on the ground
        if self.rect.bottom < 568:
            self.rect.y += int(self.vel)
        else:
            self.rect.bottom = 568  # Clamp to ground
            self.vel = 0  # Stop moving once grounded
        # prevent going past top of screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel = 0

        if not game_over:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if (mouse[0] or keys[pygame.K_SPACE]) and not self.clicked:
                self.clicked = True
                self.jump()
            if not mouse[0] and not keys[pygame.K_SPACE]:
                self.clicked = False

        self.image = self.rotate_image()

