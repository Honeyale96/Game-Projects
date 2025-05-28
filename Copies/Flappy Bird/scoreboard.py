import pygame

# Define the Scoreboard class
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, x, y, font, color, coin_sound=None):
        super().__init__()
        self.score = 0
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.coin_sound = coin_sound

    def increment(self):
        self.score += 1
        if self.coin_sound:
            self.coin_sound.play()

    def draw(self, surface):
        text_img = self.font.render(str(self.score), True, self.color)
        surface.blit(text_img, (self.x, self.y))