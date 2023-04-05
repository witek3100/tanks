import math
import random
import time
import pygame
import models
import sys

pygame.init()

BLUE = (20, 60, 160)
GREEN = (20, 160, 60)
GREY = (150, 150, 150)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)

screen = pygame.display.set_mode((900, 600))
board = [[models.Pixel(3*x, 3*y) for x in range(300)] for y in range(200)]

ground_function = lambda x : 2*math.sqrt(x) + 500
for column in board:
    for pixel in column:
        if ground_function(pixel.x) < pixel.y:
            pixel.ground = True

def explosion(x, y, strength):
    for i in range(strength):
        pygame.draw.circle(screen, GREY, (x, y), i)
        pygame.draw.circle(screen, RED, (x, y), 0.5*i)
        time.sleep(0.002)
    for column in board:
        for pixel in column:
            if (pixel.x - x)**2 + (pixel.y - y)**2 < strength**2:
                pixel.ground = False
    for tank in tanks:
        if x-strength < tank.x < x+strength and y-strength < tank.y < y+strength:
            tank.health -= strength
        if tank.health <= 0:
            explosion(tank.x, tank.y, 20)
            tanks.remove(tank)


weapon = None
colors = [BLUE, GREEN, GREY, RED, YELLOW]
tanks = [models.Tank(i*200+100, ground_function(i*200+100), colors.pop()) for i in range(len(colors))]
next_turn = lambda player : player + 1 if player < len(tanks)-1 else 0

wind = random.randint(-10, 10)
player = 0

num_of_players = 2
num_of_rounds = 5
buttons = {'new game button' : models.Button(screen, (390, 150), (120, 30), 'NEW GAME', True),
           'text num of players' : models.Button(screen, (380, 120), (140, 20), '     players', False),
           'decrease players button' : models.Button(screen, (370, 170), (20, 20), '-', False),
           'increase players button' : models.Button(screen, (510, 170), (20, 20), '+', False),
           'num of players' : models.Button(screen, (440, 170), (20, 20), '{}'.format(num_of_players), False),
           'text num of rounds': models.Button(screen, (380, 240), (140, 20), '     rounds', False),
           'decrease num of rounds': models.Button(screen, (370, 290), (20, 20), '-', False),
           'increase num of rounds': models.Button(screen, (510, 290), (20, 20), '+', False),
           'num of rounds': models.Button(screen, (440, 290), (20, 20), '{}'.format(num_of_rounds), False),
           'create game button': models.Button(screen, (370, 360), (160, 30), 'CREATE GAME', False),
           }

''' menu loop '''
run_menu = True
run_round = False
while run_menu:
    background = pygame.image.load("static/mountains.jpg").convert()
    screen.blit(background, (0, 0))

    title_text_down = pygame.font.Font('freesansbold.ttf', 50).render("TANKS", False, YELLOW)
    title_text_rect_down = title_text_down.get_rect()
    title_text_rect_down.center = (450, 50)
    screen.blit(title_text_down, title_text_rect_down)
    title_text_up = pygame.font.Font('freesansbold.ttf', 50).render("TANKS", False, ORANGE)
    title_text_rect_up = title_text_up.get_rect()
    title_text_rect_up.center = (447, 47)
    screen.blit(title_text_up, title_text_rect_up)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ''' shoting tanks animation '''
    tank1 = models.Tank(100, 500, RED)
    tank1.gun_direction = 40
    tank2 = models.Tank(800, 500, BLUE)
    tank2.gun_direction = 130
    tank1.draw(screen)
    tank2.draw(screen)
    if not weapon:
        shoting_tank = random.choice([tank1, tank2])
        weapon = shoting_tank.shot()
    weapon.draw(screen)
    time.sleep(0.01)
    weapon.x += weapon.velocity_x
    weapon.y += weapon.velocity_y
    weapon.velocity_y += 0.2
    if weapon.y > 500:
        explosion(weapon.x, weapon.y, 30)
        weapon = None

    for button_key in buttons.keys():
        buttons[button_key].draw()

    game = None
    if buttons['new game button'].clicked():
        for button_key in buttons.keys():
            buttons[button_key].active = True
        buttons['new game button'].active = False

    if buttons['create game button'].clicked():
        game = models.Game(num_of_players, num_of_rounds)
    if buttons['increase players button'].clicked():
        if num_of_players < 6:
            num_of_players += 1
        buttons['num of players'].update_text(str(num_of_players))
    if buttons['decrease players button'].clicked():
        if 2 < num_of_players:
            num_of_players -= 1
        buttons['num of players'].update_text(str(num_of_players))
    if buttons['increase num of rounds'].clicked():
        if num_of_rounds < 10:
            num_of_rounds += 1
        buttons['num of rounds'].update_text(str(num_of_rounds))
    if buttons['decrease num of rounds'].clicked():
        if 1 < num_of_rounds:
            num_of_rounds -= 1
        buttons['num of rounds'].update_text(str(num_of_rounds))

    ''' round loop '''
    while game:
        background = pygame.image.load("static/mountains.jpg").convert()
        screen.blit(background, (0, 0))
        for column in board:
            for pixel in column:
                if pixel.ground:
                    pygame.draw.rect(screen, GREEN, (pixel.x, pixel.y, 3, 3))

        ''' players info text boxes '''
        text_boxes = []
        for tank in tanks:
            text_boxes.append(pygame.font.Font('freesansbold.ttf', 20).render(
                'PLAYER 1     score {}     hp {}'.format(100, tank.health), True, tank.color))

        for c, player_data in enumerate(text_boxes):
            text_rect = player_data.get_rect()
            text_rect.x += 500
            text_rect.y += 10 + 30*c
            screen.blit(player_data, text_rect)

        for tank in tanks:
            tank.draw(screen)
            try:
                if board[int(tank.y / 3) + 1][int(tank.x / 3)].ground == False:
                    tank.y += 1
                if board[int(tank.y / 3) - 1][int(tank.x / 3)].ground == True:
                    tank.y -= 1
                if board[int(tank.y / 3) - 5][int(tank.x / 3 + 3)].ground == True:
                    tank.x -= 1
                if board[int(tank.y / 3) - 5][int(tank.x / 3 - 3)].ground == True:
                    tank.x += 1
            except IndexError:
                tanks.remove(tank)

        if weapon != None:
            weapon.draw(screen)
            weapon.move(wind)
            try:
                if board[int(weapon.y/3)][int(weapon.x/3)].ground == True:
                    explosion(weapon.x, weapon.y, 20)
                    weapon = None
                    wind = random.randint(-10, 10)
                    player = next_turn(player)
            except IndexError:
                weapon = None
                wind = random.randint(-10, 10)
                player = next_turn(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tanks[player].move(-1)
        if keys[pygame.K_RIGHT]:
            tanks[player].move(1)
        if keys[pygame.K_UP]:
            tanks[player].move_gun(1)
        if keys[pygame.K_DOWN]:
            tanks[player].move_gun(-1)
        if keys[pygame.K_SPACE] and weapon == None:
            weapon = tanks[player].shot()

        pygame.display.update()

    pygame.display.update()

pygame.quit()
