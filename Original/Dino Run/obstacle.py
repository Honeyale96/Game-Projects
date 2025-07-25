import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, world_x, ground_y):
        super().__init__()

        self.type = obstacle_type  # Save type
        self.ground_y = ground_y  # Needed for ground alignment
        self.world_x = world_x  # Position in world space
        self.index = 0
        self.counter = 0

        # Load and position the image
        if obstacle_type == "stump":
            self.image = pygame.image.load("Assets/images/stump.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.bottom = ground_y  # Sit on the ground

        elif obstacle_type == "stone":
            self.image = pygame.image.load("Assets/images/stone.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100,100))
            self.rect = self.image.get_rect()
            self.rect.bottom = ground_y  # Sit on the ground

        elif obstacle_type == "bird":
            self.images = [pygame.transform.scale(
                            pygame.transform.flip(
                                pygame.image.load(f"Assets/images/bird{num}.png").convert_alpha(),
                                True, False),
                        (80, 80)) for num in range(1, 5)]
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            # Randomly place bird high or low for variety
            high_or_low = random.choice(["high", "low"])
            if high_or_low == "high":
                self.rect.y = ground_y - 150  # High bird: no ducking needed
            else:
                self.rect.bottom = ground_y - 50  # Low bird: must duck

    def update(self, scroll_speed):
        self.world_x -= scroll_speed  # Move left with scroll

        if self.type == "bird":
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

    def draw(self, surface, scroll):
        screen_x = self.world_x - scroll  # Convert to screen position
        surface.blit(self.image, (screen_x, self.rect.y))  # Draw to screen

    def get_rect(self, scroll):
        screen_x = self.world_x - scroll
        return pygame.Rect(screen_x, self.rect.y, self.rect.width, self.rect.height)

