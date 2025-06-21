import pygame

class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen, screen_width, screen_height):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, screen_width // 2, screen_height))
            pygame.draw.rect(screen, self.color, (screen_width // 2 + self.fade_counter, 0, screen_width, screen_height))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, screen_width, screen_height // 2))
            pygame.draw.rect(screen, self.color, (0, screen_height // 2 + self.fade_counter, screen_width, screen_height))
        if self.direction == 2: # vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, screen_width, 0 + self.fade_counter))
        if self.fade_counter >= screen_width:
            fade_complete = True

        return fade_complete