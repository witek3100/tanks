import pygame
import math

class Pixel:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ground = False

class Weapon:

    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.strength = 15
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.gun_direction = 90
        self.health = 100
        self.shot_power = 50
        self.max_shot_power = 100

    def move(self, change):
        if 0 <= self.x <= 900:
            self.x += change

    def move_gun(self, change):
        if 0 < self.gun_direction < 180:
            self.gun_direction += change

    def edit_shot_power(self, change):
        if 0 < self.shot_power < self.max_shot_power:
            self.shot_power += change

    def shot(self):
        return Weapon(self.x+(20*math.cos((self.gun_direction/360)*2*math.pi)), self.y-(20*math.sin((self.gun_direction/360)*2*math.pi)),
                      self.shot_power*0.2*math.cos((self.gun_direction/360)*2*math.pi), -self.shot_power*0.2*math.sin((self.gun_direction/360)*2*math.pi))