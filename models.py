import time
import pygame
import math

class Button:
    def __init__(self, screen, pos, size, text, active):
        #main vars
        self.screen = screen
        self.position = pos
        self.size = size
        self.top_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.bottom_rect = pygame.Rect(self.position[0] + 2, self.position[1] + 5, self.size[0], self.size[1])
        self.pressed = False
        self.active = active

        #colors
        self.__top_rect_normal_color = (205,205,0)
        self.__top_rect_hovered_color = (250,250,150)
        self.__bottom_rect_normal_color = (205,102,0)
        self.__bottom_rect_hovered_color = (205,142,40)
        self.__not_active_color = (131,139,139)

        self.__top_rect_color = self.__top_rect_normal_color
        self.__bottom_rect_color = self.__bottom_rect_normal_color

        #text
        self.__text_font = pygame.font.SysFont(str(text) + "font", 30)
        self.__text = self.__text_font.render(text, False, (0, 0, 0))

    def draw(self):
        if self.active:
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.bottomleft, 10)
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.bottomright, 10)
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.topright, 10)
            pygame.draw.rect(self.screen, self.__bottom_rect_color, ((self.bottom_rect.topleft[0] - 10, self.bottom_rect.topleft[1]), (self.bottom_rect.size[0] + 20, self.bottom_rect.size[1])))
            pygame.draw.rect(self.screen, self.__bottom_rect_color, ((self.bottom_rect.topleft[0], self.bottom_rect.topleft[1] - 10), (self.bottom_rect.size[0], self.bottom_rect.size[1] + 20)))
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.bottomleft, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.bottomright, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.topleft, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.topright, 10)
            pygame.draw.rect(self.screen, self.__top_rect_color, ((self.top_rect.topleft[0] - 10, self.top_rect.topleft[1]), (self.top_rect.size[0] + 20, self.top_rect.size[1])))
            pygame.draw.rect(self.screen, self.__top_rect_color, ((self.top_rect.topleft[0], self.top_rect.topleft[1] - 10), (self.top_rect.size[0], self.top_rect.size[1] + 20)))
            self.screen.blit(self.__text, (self.position[0]+2, self.position[1]+5))

    def clicked(self):
        if self.active:
            pos = pygame.mouse.get_pos()
            if self.top_rect.collidepoint(pos):
                self.__top_rect_color = self.__top_rect_hovered_color
                self.__bottom_rect_color = self.__bottom_rect_hovered_color
                if pygame.mouse.get_pressed()[0] and self.pressed == False:
                    self.top_rect.center = self.bottom_rect.center
                    self.draw()
                    pygame.display.update()
                    time.sleep(0.05)
                    return True
                self.top_rect.x = self.position[0]
                self.top_rect.y = self.position[1]
            else:
                self.__top_rect_color = self.__top_rect_normal_color
                self.__bottom_rect_color = self.__bottom_rect_normal_color
            return False

    def update_text(self, text):
        self.__text_font = pygame.font.SysFont(str(text) + "font", 30)
        self.__text = self.__text_font.render(text, False, (0, 0, 0))

class Game:
    def __init__(self, players, num_of_rounds):
        self.board = [[Pixel(3*x, 3*y) for x in range(300)] for y in range(200)]
        self.players = [Player(i, (255,255,255)) for i in range(players)]
        self.next_turn = lambda player : player + 1 if player < len(self.players)-1 else 0
        self.ground_function = lambda x : 2*math.sqrt(x) + 400
        self.num_of_rounds = num_of_rounds

class Player:
    def __init__(self, id, color):
        self.player_id = id
        self.score = 0
        self.color = color
        self.tank = None

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

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), 2)

    def move(self, wind):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.2
        self.velocity_x += wind * 0.005

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
        elif self.gun_direction <= 0:
            self.gun_direction = 1
        elif self.gun_direction >= 180:
            self.gun_direction = 179
    def edit_shot_power(self, change):
        if 0 < self.shot_power < self.max_shot_power:
            self.shot_power += change

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y - 7, 13, 10))
        pygame.draw.rect(screen, self.color, (self.x - 6.5, self.y - 2, 26, 10))
        pygame.draw.rect(screen, (0,0,0), (self.x - 6, self.y + 5, 24, 4))
        pygame.draw.line(screen, (0,0,0), (self.x + 5, self.y - 7), (self.x + (20 * math.cos((self.gun_direction / 360) * 2 * math.pi)), self.y - 7 - (20 * math.sin((self.gun_direction / 360) * 2 * math.pi))), 5)

    def shot(self):
        return Weapon(self.x+(20*math.cos((self.gun_direction/360)*2*math.pi)), self.y-(20*math.sin((self.gun_direction/360)*2*math.pi)),
                      self.shot_power*0.2*math.cos((self.gun_direction/360)*2*math.pi), -self.shot_power*0.2*math.sin((self.gun_direction/360)*2*math.pi))