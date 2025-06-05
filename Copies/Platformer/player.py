import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Instance attributes
        self.images_right = []
        self.images_left = []
        self.image = None
        self.dead_image = None
        # Initial animation/frame setup
        self.index = 0
        self.counter = 0
        self.direction = 0
        # Physics and movement
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.width = 0
        self.height = 0
        self.vel_y = 0
        self.jumped = False
        # Constants
        self.gravity = 1
        self.jump_strength = -15
        self.walk_speed = 5
        self.walk_cooldown = 5

        self.reset(x, y)  # Do image loading and positioning


    def update(self, screen, screen_height, world, blob_group,lava_group, exit_group, game_over):
        """Updates the player's state each frame."""
        if game_over == 0:
            dx, dy = self.handle_input()
            dy += self.apply_gravity()

            # Check for collision
            for tile in world.tile_list:
                #  Horizontal(x) direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Vertical(y) direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:  # Jumping into tile
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:  # Falling onto tile
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False  # Only reset jump here


            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                self.image = self.dead_image
            # Check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                self.image = self.dead_image
            # Check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            if self.rect.y > 100:
                self.rect.y += -5

            # # Prevent player from falling off-screen
            # if self.rect.bottom > screen_height:
            #     self.rect.bottom = screen_height
            #     self.vel_y = 0
            # No longer needed once wall collision is introduced

        # Draw player
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def handle_input(self):
        """Handles keyboard input for movement and jumping."""
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()

        # Jump
        if keys[pygame.K_SPACE] and not self.jumped:
            self.vel_y = self.jump_strength
            self.jumped = True

        # Move Left
        if keys[pygame.K_LEFT]:
            dx = -self.walk_speed
            self.counter += 1
            self.direction = -1
        # Move Right
        elif keys[pygame.K_RIGHT]:
            dx = self.walk_speed
            self.counter += 1
            self.direction = 1
        # Idle
        else:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == -1:
                self.image = self.images_left[self.index]

        # Handle animation if walking
        self.animate()

        return dx, dy

    def apply_gravity(self):
        """Applies gravity to the player each frame."""
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        return self.vel_y

    def animate(self):
        """Updates player animation frames based on movement."""
        if self.counter > self.walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == -1:
                self.image = self.images_left[self.index]

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[0]
        self.direction = 0
        self.index = 0
        self.counter = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
