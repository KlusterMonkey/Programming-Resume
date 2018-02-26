import pygame
class Trail(pygame.sprite.Sprite):
    def __init__(self, bounds, chunk_size, x, y, image):
        super().__init__()
        self.bounds = bounds
        self.chunk_size = chunk_size
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * chunk_size
        self.rect.y = y * chunk_size
    def move(x, y):
        self.rect.x = self.bounds * x
        self.rect.y = self.bounds * y
