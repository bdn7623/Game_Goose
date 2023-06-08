import pygame
import random
from os import listdir
from pygame import Surface
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
YELLOW = 255, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface: Surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

# player = pygame.Surface((20, 20))
# player.fill(WHITE)
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect() #первоначальное расположение
player_speed = 10

def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy = pygame.image.load('img/enemy.png').convert_alpha()
    #enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_rect = pygame.Rect(width, random.randint(0, heigth - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(2,5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(YELLOW)
    bonus = pygame.image.load("img/bonus.png").convert_alpha()
    #bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_width()), 0, *bonus.get_size())
    bonus_speed = random.randint(2,5)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('img/background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_spped = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

scores = 0

enemies =[]
bonuses = []

is_working = True
is_game_over = False

while True:
    FPS.tick(60) #синхронизация
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False  #pygame.quit()
            exit()

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

    #main_surface.fill((BLACK))

    #main_surface.blit(bg, (0, 0))

    bgX -= bg_spped
    bgX2 -= bg_spped

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX,0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            main_surface.blit(font.render(f"GAME OVER, SCORE: {scores}", True, BLACK), (width - 500, 300))
            pygame.display.flip()
            pygame.time.wait(3000)  # ждем 3 секунды
            scores = 0  # сбрасываем очки
            enemies.clear()  # удаляем всех врагов
            bonuses.clear()  # удаляем все бонусы
            player_rect.center = (width // 2, heigth // 2)  # перемещаем персонажа в центр экрана
            is_game_over = False  # перезапускаем игру

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > heigth:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    pygame.display.flip()
