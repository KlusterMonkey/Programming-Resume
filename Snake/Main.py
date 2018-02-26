import random
import sys
import time

import pygame

import Food
import Player
import Trail

pygame.init()

active_state = None

CHUNK_SIZE = 16
CHUNK_AMOUNT = 32
RESOLUTION = (CHUNK_SIZE * CHUNK_AMOUNT, CHUNK_SIZE * CHUNK_AMOUNT)
#Colors
BACKGROUND = (51, 51, 51)
WHITE = (255, 255, 255)
FOOD = (94, 12, 119)

should_update = False
time_ticked = time.clock()

keys = {pygame.K_w: False, pygame.K_s: False, pygame.K_a: False, pygame.K_d: False, pygame.K_RETURN: False}
screen = pygame.display.set_mode(RESOLUTION)

#Textures
SNAKE = pygame.transform.scale(pygame.image.load('Snake.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))
TRAIL = pygame.transform.scale(pygame.image.load('Trail.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))

HEAD_1 = pygame.transform.scale(pygame.image.load('Tron_Head 1.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))
TRAIL_1 = pygame.transform.scale(pygame.image.load('Tron_Trail 1.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))

HEAD_2 = pygame.transform.scale(pygame.image.load('Tron_Head 2.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))
TRAIL_2 = pygame.transform.scale(pygame.image.load('Tron_Trail 2.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))

FOOD = pygame.transform.scale(pygame.image.load('Food.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))

#if TRON == True:
#    player_sprite = Player.Player(RESOLUTION, CHUNK_SIZE, 2, 0, HEAD_1, TRAIL_1)
#    player_sprite2 = Player.Player(RESOLUTION, CHUNK_SIZE, CHUNK_AMOUNT - 3, 0, HEAD_2, TRAIL_2)
#    player_sprite_group = pygame.sprite.Group()
#    player_sprite_group.add(player_sprite)
#    player_sprite_group.add(player_sprite2)
#    players = [player_sprite, player_sprite2]
#elif TRON == False:
#    player_sprite = Player.Player(RESOLUTION, CHUNK_SIZE, 2, 0, SNAKE, TRAIL)
#    player_sprite_group = pygame.sprite.Group()
#    player_sprite_group.add(player_sprite)
#    players = [player_sprite]

food_sprite = Food.Food(RESOLUTION, CHUNK_SIZE, FOOD)
food_sprite_group = pygame.sprite.Group()
food_sprite_group.add(food_sprite)

trail_sprite = Trail.Trail(RESOLUTION, CHUNK_SIZE, 2, 2, FOOD)
trail_sprite_group = pygame.sprite.Group()
trail_sprite_group.add(trail_sprite)

score_font = pygame.font.SysFont('monospace', 16)
def change_state():
    global active_state
    global CHUNK_AMOUNT
    global CHUNK_SIZE
    active_state.exit()
    if active_state.name == 'GameState':
        active_state = StartState()
        active_state.enter()
    elif active_state.name == 'StartState':
        active_state = GameState()
        active_state.enter(16, 32)

def event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        if event.type == pygame.KEYUP:
            keys[event.key] = False
class StartState():
    def __init__(self):
        super().__init__()
        self.name = "StartState"
        self.background = (51, 51, 51)
        self.white = (255, 255, 255)
    def handle_keys(self):
        if keys[pygame.K_RETURN]:
            change_state()
    def update(self):
        self.handle_keys()
    def render(self):
        screen.fill(self.background)
        label = score_font.render(('Game over! Press enter to play.'), 1, self.white)
        screen.blit(label, (RESOLUTION[0] / 2 - label.get_rect().width / 2, RESOLUTION[1] / 2 - label.get_rect().height))
        pygame.display.flip()
    def enter(self):
        pass
    def exit(self):
        pass
    def is_done(self):
        return False
class GameState():
    def __init__(self):
        super().__init__()
        self.name = "GameState"

        #Textures
        self.snake = pygame.transform.scale(pygame.image.load('Snake.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))
        self.trail = pygame.transform.scale(pygame.image.load('Trail.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))
        self.food = pygame.transform.scale(pygame.image.load('Food.png').convert(), (CHUNK_SIZE, CHUNK_SIZE))

        self.highscore = int(open('Score.dat', 'r').readline())
        #Colors
        self.background = (51, 51, 51)
        self.white = (255, 255, 255)

        #Sprites
        self.player_sprite = Player.Player(RESOLUTION, CHUNK_SIZE, 2, 0, SNAKE, TRAIL)
        self.player_sprite_group = pygame.sprite.Group()

        self.food_sprite = Food.Food(RESOLUTION, CHUNK_SIZE, FOOD)
        self.food_sprite_group = pygame.sprite.Group()
        self.food_sprite_group.add(self.food_sprite)

        self.trail_sprite = Trail.Trail(RESOLUTION, CHUNK_SIZE, 2, 2, FOOD)
        self.trail_sprite_group = pygame.sprite.Group()
        self.trail_sprite_group.add(self.trail_sprite)

        #Other
        self.chunk_size = 16
        self.chunk_amount = 32
        self.resolution = (self.chunk_size * self.chunk_amount, self.chunk_size * self.chunk_amount)

    def handle_keys(self):
        if keys[pygame.K_w]:
            self.player_sprite.change_dir_up()
        if keys[pygame.K_s]:
            self.player_sprite.change_dir_down()
        if keys[pygame.K_a]:
            self.player_sprite.change_dir_left()
        if keys[pygame.K_d]:
            self.player_sprite.change_dir_right()

    def update(self):
        self.handle_keys()

        self.trail_sprite_group.empty()
        #Collision
        for player in self.players:
            player.update()
            for i in player.trail:
                self.trail_sprite_group.add(i)
        for player in self.players:
            #Border Collision
            if player.rect.x < 0 or player.rect.x > (RESOLUTION[0] - CHUNK_SIZE):
                change_state()
            if player.rect.y < 0 or player.rect.y > (RESOLUTION[1] - CHUNK_SIZE):
                change_state()
            #Food Collision
            for hit in pygame.sprite.spritecollide(player, self.food_sprite_group, True):
                player.score += 1
                self.food_sprite = Food.Food(self.resolution, self.chunk_size, self.food)
                for sprite in self.trail_sprite_group.sprites():
                    if sprite.rect.x == self.food_sprite.rect.x and sprite.rect.y == self.food_sprite.rect.y:
                        self.food_sprite = Food.Food(self.resolution, self.chunk_size, self.food)
                self.food_sprite_group.add(self.food_sprite)
            for hit in pygame.sprite.spritecollide(player, self.trail_sprite_group, False):
                change_state()
    def render(self):
        screen.fill(self.background)

        score_label = score_font.render(('Current: {}'.format(self.player_sprite.score)), 1, self.white)
        screen.blit(score_label, (self.resolution[0] / 2 - score_label.get_rect().width / 2, 10))
        score_label = score_font.render(('Highscore: {}'.format(self.highscore)), 1, self.white)
        screen.blit(score_label, (self.resolution[0] / 2 - score_label.get_rect().width / 2, 25))

        self.food_sprite_group.draw(screen)
        self.trail_sprite_group.draw(screen)
        self.player_sprite_group.draw(screen)
        pygame.display.flip()
    def enter(self, chunk_size, chunk_amount):
        self.player_sprite = Player.Player(self.resolution, self.chunk_size, 2, 2, self.snake, self.trail)
        self.player_sprite_group = pygame.sprite.Group()
        self.player_sprite_group.add(self.player_sprite)
        self.players = [self.player_sprite]

        #Setup for food
        self.food_sprite = Food.Food(self.resolution, self.chunk_size, self.food)
        self.food_sprite_group = pygame.sprite.Group()
        self.food_sprite_group.add(self.food_sprite)

        #Setup for trails
        self.trail_sprite = Trail.Trail(self.resolution, self.chunk_size, 2, 2, self.food)
        self.trail_sprite_group = pygame.sprite.Group()
        self.trail_sprite_group.add(self.trail_sprite)
    def exit(self):
        if self.player_sprite.score >= self.highscore:
            highscore = self.player_sprite.score
            f = open('Score.dat', 'w')
            f.write(str(highscore))
    def is_done(self):
        return False

active_state = GameState()
active_state.enter(16, 32)
while True:
    event()
    if time.clock() - time_ticked >= 0.05:
        time_ticked = time.clock()
        should_update = True
    if should_update:
        should_update = False
        #Call update
        active_state.update()
        #Render
        active_state.render()
#while True:
#    event()
#    if time.clock() - time_ticked >= 0.05:
#        time_ticked = time.clock()
#        should_update = True
#    if should_update:
#        should_update = False
#        #draw
#        screen.fill(BACKGROUND)
#
#        trail_sprite_group.empty()
#
#        #Collision
#        for player in players:
#            player.update()
#            for i in player.trail:
#                trail_sprite_group.add(i)
#        for player in players:
#            for hit in pygame.sprite.spritecollide(player, food_sprite_group, True):
#                player.score += 1
#                food_sprite = Food.Food(RESOLUTION, CHUNK_SIZE, FOOD)
#                for sprite in trail_sprite_group.sprites():
#                    if sprite.rect.x == food_sprite.rect.x and sprite.rect.y == food_sprite.rect.y:
#                        food_sprite = Food.Food(RESOLUTION, CHUNK_SIZE, FOOD)
#                food_sprite_group.add(food_sprite)
#            for hit in pygame.sprite.spritecollide(player, trail_sprite_group, False):
#                if player == player_sprite:
#                    print('Player 2 wins!')
#                elif player == player_sprite2:
#                    print('Player 1 wins!')
#                sys.exit()
#
#        #draw text
#        score_label = score_font.render(('{}'.format(player_sprite.score)), 8, WHITE)
#        screen.blit(score_label, (RESOLUTION[0] / 4 - score_label.get_rect().width / 2, 10))
#        if TRON:
#            score_label = score_font.render(('{}'.format(player_sprite2.score)), 8, WHITE)
#            screen.blit(score_label, ((RESOLUTION[0] / 4) * 3 - score_label.get_rect().width / 2, 10))
#
#        food_sprite_group.draw(screen)
#        trail_sprite_group.draw(screen)
#        player_sprite_group.draw(screen)
#        pygame.display.flip()
