import math
import random
import time
import pygame
import models

pygame.init()

BLUE = (20, 60, 160)
GREEN = (20, 160, 60)
YELLOW = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((900, 600))
board = [[models.Pixel(3*x, 3*y) for x in range(300)] for y in range(200)]

ground_function = lambda x : 2*math.sqrt(x) + 400
for column in board:
    for pixel in column:
        if ground_function(pixel.x) < pixel.y:
            pixel.ground = True

def explosion(x, y, strength):
    for i in range(strength):
        pygame.draw.circle(screen, YELLOW, (x, y), i)
        pygame.draw.circle(screen, RED, (x, y), 0.5*i)
        time.sleep(0.002)
    for column in board:
        for pixel in column:
            if (pixel.x - x)**2 + (pixel.y - y)**2 < strength**2:
                pixel.ground = False
    if x-strength < tank.x < x+strength and y-strength < tank.y < y+strength:
        tank.health -= strength

weapon = None
colors = [BLUE, GREEN, YELLOW, RED]
tanks = [models.Tank(i*100, ground_function(i*100), colors.pop()) for i in range(len(colors))]
tank = models.Tank(100, ground_function(100), RED)

run = True
wind = random.randint(-10, 10)
player = 0
while run:
    for column in board:
        for pixel in column:
            if pixel.ground:
                pygame.draw.rect(screen, GREEN, (pixel.x, pixel.y, 3, 3))
            else:
                pygame.draw.rect(screen, BLUE, (pixel.x, pixel.y, 3, 3))

    for tank in tanks:
        pygame.draw.rect(screen, tank.color, (tank.x, tank.y-7, 13, 10))
        pygame.draw.rect(screen, tank.color, (tank.x-6.5, tank.y-2, 26, 10))
        pygame.draw.rect(screen, BLACK, (tank.x - 6, tank.y + 5, 24, 4))
        pygame.draw.line(screen, BLACK, (tank.x+5, tank.y-7), (tank.x+(20*math.cos((tank.gun_direction/360)*2*math.pi)), tank.y-7-(20*math.sin((tank.gun_direction/360)*2*math.pi))), 5)
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
        pygame.draw.circle(screen, BLACK, (weapon.x, weapon.y), 2)
        weapon.x += weapon.velocity_x
        weapon.y += weapon.velocity_y
        weapon.velocity_y += 0.2
        weapon.velocity_x += wind*0.005
        try:
            if board[int(weapon.y/3)][int(weapon.x/3)].ground == True:
                explosion(weapon.x, weapon.y, 20)
                weapon = None
                wind = random.randint(-10, 10)
                if player < len(tanks)-1:
                    player += 1
                else:
                    player = 0
        except IndexError:
            weapon = None
            wind = random.randint(-10, 10)
            if player < len(tanks):
                player += 1
            else:
                player = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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

pygame.quit()
