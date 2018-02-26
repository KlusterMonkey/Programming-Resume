import pygame
import random
class Food(pygame.sprite.Sprite):
    def __init__(self, bounds, chunk_size, image):
        super().__init__()
        self.bounds = bounds
        self.chunk_size = chunk_size
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, (bounds[0] / chunk_size) - 1) * chunk_size
        self.rect.y = random.randint(0, (bounds[1] / chunk_size) - 1) * chunk_size
