import pygame
import sys
import random

from GameFactory import GFScreen, GFCharacter, GFBasic_Monster, GFSpriteSheet, GFFollowAI

screen_width = 800
screen_height = 600
sprite_size = 16
movement_speed = 5

pygame.mixer.init()
pygame.mixer.music.load('music/castle.wav')
pygame.mixer.music.play()

class FoxSprite(GFCharacter):
    hp = 10
        
class SnakeSprite(GFBasic_Monster):
    hp = 10

# Setup Pygame
pygame.init()
clock = pygame.time.Clock()

mainGame = GFScreen(screen_width, screen_height)
pygame.display.set_caption("Forest Critters")

players = pygame.sprite.Group()
snakes = pygame.sprite.Group()

the_player = FoxSprite("sprites/racoon.png",
                        init_pos_x = random.randrange(screen_width-sprite_size),
                        init_pos_y = random.randrange(screen_height-sprite_size))
the_player.set_screen(mainGame)

players.add(the_player)

for idx in range(0, 5):
    a_snake = SnakeSprite('sprites/snake_green.png',
                                  init_pos_x = random.randrange(screen_width-sprite_size),
                                  init_pos_y = random.randrange(screen_height-sprite_size))
    a_snake.set_screen(mainGame)
    if (idx < 4):
        myAI = GFFollowAI(a_snake, the_player)
        a_snake.ai = myAI
    
    snakes.add(a_snake)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                the_player.change_y = -movement_speed
            elif event.key == pygame.K_DOWN:
                the_player.change_y = movement_speed
            elif event.key == pygame.K_LEFT:
                the_player.change_x = -movement_speed
            elif event.key == pygame.K_RIGHT:
                the_player.change_x = movement_speed
        if event.type == pygame.KEYUP:
            the_player.change_y = 0
            the_player.change_x = 0
                

    mainGame.fill((53, 81, 92))
    snakes.draw(mainGame.screen)
    snakes.update(0.1)
    players.draw(mainGame.screen)
    players.update(0.1)
    
    pygame.display.flip()
    clock.tick(60)
