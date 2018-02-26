import pygame
import sys
import Trail
class Player(pygame.sprite.Sprite):
    def __init__(self, bounds, chunk_size, startX, startY, image, trail_image):
        super().__init__()
        self.bounds = bounds
        self.chunk_size = chunk_size
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = startX * chunk_size
        self.rect.y = startY * chunk_size
        self.velocity = 1
        self.direction = 2 #0: Up, 1: Right, 2: Down, 3: Left
        self.score = 0
        self.trail_image = trail_image
        self.trail = []
    def change_dir_up(self):
        if not self.direction == 2:
            self.direction = 0
    def change_dir_down(self):
        if not self.direction == 0:
            self.direction = 2
    def change_dir_left(self):
        if not self.direction == 1:
            self.direction = 3
    def change_dir_right(self):
        if not self.direction == 3:
            self.direction = 1
    def update(self):
        trail = self.trail
        tempX = self.rect.x
        tempY = self.rect.y
        #Up
        if self.direction == 0:
            self.rect.y -= self.chunk_size * self.velocity
        #Right
        if self.direction == 1:
            self.rect.x += self.chunk_size * self.velocity
        #Down
        if self.direction == 2:
            self.rect.y += self.chunk_size * self.velocity
        #Left
        if self.direction == 3:
            self.rect.x -= self.chunk_size * self.velocity
        #Trails (ugh)
        if len(trail) == self.score and len(trail) > 0:
            #Moves every space in the array up one (end is pushed off)
            for i in range(0, self.score - 1):
                    trail[i] = trail[i + 1]
            #Sets the new head space
            trail[self.score - 1] = Trail.Trail(self.bounds, self.chunk_size, tempX / self.chunk_size, tempY / self.chunk_size, self.trail_image)
        while len(trail) < self.score:
            trail.append(Trail.Trail(self.bounds, self.chunk_size, tempX / self.chunk_size, tempY / self.chunk_size, self.trail_image))
        #Set new head space
        if len(trail) > 0:
            trail[self.score - 1] = Trail.Trail(self.bounds, self.chunk_size, tempX / self.chunk_size, tempY / self.chunk_size, self.trail_image)
