import pygame
import random
from os import listdir
from random import randint as rcolor
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1366, 768

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
YELLOW = 255, 255, 0
PURPLE = 125, 18, 255

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'
bonSfx = pygame.mixer.Sound(IMGS_PATH + 'bonus.wav')
bon1Sfx = pygame.mixer.Sound(IMGS_PATH + 'boom.wav')
# player = pygame.Surface((20, 20))
# player.fill((WHITE))
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]

player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5

def create_bonus():
    bonus = pygame.Surface((20, 20))
    # bonus.fill(YELLOW)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (80, 130))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 5)
    return [bonus, bonus_rect, bonus_speed]

def create_enemy():
    enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (140, 55))
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(1, 5)
    return [enemy, enemy_rect, enemy_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

score = 0

enemies = []

bonuses = []

is_working = True
while is_working:
    
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
            
    
    
    
    pressed_keys = pygame.key.get_pressed()
    
    #if player_rect.bottom >= height or player_rect.top <= 0:
    #    player_speed[1] = -player_speed[1]
    #    player.fill((rcolor(0, 255), rcolor(0, 255), rcolor(0,255)))
    #if player_rect.left <= 0 or player_rect.right >= width:
    #    player.fill((rcolor(0, 255), rcolor(0, 255), rcolor(0,255)))
    #    player_speed[0] = -player_speed[0]
    
    # main_surface.fill((BLACK))
    # main_surface.blit(bg, (0, 0))
    bgX -= bg_speed
    bgX2 -= bg_speed
    
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    
    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    
    main_surface.blit(player, (player_rect))
    main_surface.blit(font.render(str(score), True, PURPLE), (width - 30, 0))
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))
        
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
            pygame.mixer.Sound.play(bonSfx)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            pygame.mixer.Sound.play(bon1Sfx)
            is_working = False
    
    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)
    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    
    
    # main_surface.fill((155, 145, 155))
    pygame.display.flip()


