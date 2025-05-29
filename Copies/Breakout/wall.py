import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen_width, columns, rows):
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.width = screen_width // columns
        self.height = 50
        self.blocks = []

    def create_wall(self):
        self.blocks = []
        for row in range(self.rows):
            block_row = []
            for column in range(self.columns):
                block_x = column * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self, screen, block_red, block_green, block_blue, bg):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_color = block_blue
                elif block[1] == 2:
                    block_color = block_green
                elif block[1] == 1:
                    block_color = block_red
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)



