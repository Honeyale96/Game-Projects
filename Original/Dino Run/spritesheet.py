import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        # create a black box surface
        image = pygame.Surface((width, height)).convert_alpha()
        # take the image from spritesheet and add it to the "black box"
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        # scale image to be bigger
        image = pygame.transform.scale(image, (width *scale, height * scale))
        # remove the black box
        image.set_colorkey(color)

        return image