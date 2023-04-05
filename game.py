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

screen = pygame.display.set_mode((895, 600))
weapon = None
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
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ''' configurating menu window '''
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
    weapon.x += weapon.velocity_x
    weapon.y += weapon.velocity_y
    weapon.velocity_y += 0.2
    time.sleep(0.01)
    if weapon.y > 500:
        for i in range(30):
            pygame.draw.circle(screen, (200, 130, 0), (weapon.x, weapon.y), i)
            pygame.draw.circle(screen, (255, 130, 0), (weapon.x, weapon.y), 0.5 * i)
            time.sleep(0.001)
        weapon = None

    ''' creating game menu '''
    for button_key in buttons.keys():
        buttons[button_key].draw()
    game = None
    if buttons['new game button'].clicked():
        for button_key in buttons.keys():
            buttons[button_key].active = True
        buttons['new game button'].active = False
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
    if buttons['create game button'].clicked():
        game = models.Game(screen, num_of_players, num_of_rounds)


    ''' game loop '''
    if game:
        exit_game_loop = False
        for round in range(game.num_of_rounds):
            if exit_game_loop:
                break
            ranking = sorted(game.players, key=lambda player: player.score, reverse=True)
            ''' round pre configuration '''
            for player in game.players:
                tank_spawn_point = random.randint(100, 800)
                player.tank = models.Tank(tank_spawn_point, game.ground_function(tank_spawn_point), player.color)
            wind = random.randint(-10, 10)
            weapon = None
            for column in game.board:
                for pixel in column:
                    if game.ground_function(pixel.x) < pixel.y:
                        pixel.ground = True
            power_slider = models.Slider(screen, (20, 100), 'SHOT POWER')
            gun_direction_slider = models.Slider(screen, (200, 100), 'GUN DIRECTION')
            shot_button = models.Button(screen, (380, 100), (60, 25), 'SHOT', True)
            exit_button = models.Button(screen, (30, 30), (60, 25), 'EXIT', True)

            ''' displaying round start screen '''
            screen.blit(background, (0, 0))
            run_round = True
            round_num_text_down = pygame.font.Font('freesansbold.ttf', 50).render(f"ROUND {round+1}", False, YELLOW)
            round_num_text_rect_down = round_num_text_down.get_rect()
            round_num_text_rect_down.center = (450, 50)
            screen.blit(round_num_text_down, round_num_text_rect_down)
            round_num_text_up = pygame.font.Font('freesansbold.ttf', 50).render(f"ROUND {round+1}", False, ORANGE)
            round_num_text_rect_up = round_num_text_up.get_rect()
            round_num_text_rect_up.center = (447, 47)
            screen.blit(round_num_text_up, round_num_text_rect_up)
            for c, player in enumerate(ranking):
                player_text = pygame.font.Font('freesansbold.ttf', 30).render(f'{player}    score: {player.score}', False, player.color)
                player_text_rect = player_text.get_rect()
                player_text_rect.center = (450, 100 + c*40)
                screen.blit(player_text, player_text_rect)

            pygame.display.update()
            time.sleep(3)
            player_turn = 0
            game.dying_order.clear()

            ''' round loop '''
            while run_round:
                players_alive = sum((1 if player.tank != None else 0 for player in game.players))
                screen.blit(background, (0, 0))
                for column in game.board:
                    for pixel in column:
                        if pixel.ground:
                            pygame.draw.rect(screen, (130, 190, 60), (pixel.x, pixel.y, 3, 3))

                ''' options window '''
                options_position = (20, 20)
                options_top_rect = pygame.Rect(options_position[0], options_position[1], 418, 50)
                options_bottom_rect = pygame.Rect(options_position[0] + 2, options_position[1] + 5, 418, 50)
                pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.bottomleft, 10)
                pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.bottomright, 10)
                pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.topright, 10)
                pygame.draw.rect(screen, (205, 102, 0), (
                (options_bottom_rect.topleft[0] - 10, options_bottom_rect.topleft[1]),
                (options_bottom_rect.size[0] + 20, options_bottom_rect.size[1])))
                pygame.draw.rect(screen, (205, 102, 0), (
                (options_bottom_rect.topleft[0], options_bottom_rect.topleft[1] - 10),
                (options_bottom_rect.size[0], options_bottom_rect.size[1] + 20)))
                pygame.draw.circle(screen, (180, 150, 0), options_top_rect.bottomleft, 10)
                pygame.draw.circle(screen, (180, 150, 0), options_top_rect.bottomright, 10)
                pygame.draw.circle(screen, (180, 150, 0), options_top_rect.topleft, 10)
                pygame.draw.circle(screen, (180, 150, 0), options_top_rect.topright, 10)
                pygame.draw.rect(screen, (180, 150, 0), ((options_top_rect.topleft[0] - 10, options_top_rect.topleft[1]),(options_top_rect.size[0] + 20, options_top_rect.size[1])))
                pygame.draw.rect(screen, (180, 150, 0), ((options_top_rect.topleft[0], options_top_rect.topleft[1] - 10),(options_top_rect.size[0], options_top_rect.size[1] + 20)))
                pygame.draw.polygon(screen, (255, 140, 0), ((515, 47 + 30 * player_turn), (515, 67 + 30 * player_turn), (535, 57 + 30 * player_turn)))

                ''' players stats '''
                stats_position = (470, 20)
                stats_top_rect = pygame.Rect(stats_position[0], stats_position[1], 390, len(game.players)*30)
                stats_bottom_rect = pygame.Rect(stats_position[0] + 2, stats_position[1] + 5, 390, len(game.players*30))
                pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.bottomleft, 10)
                pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.bottomright, 10)
                pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.topright, 10)
                pygame.draw.rect(screen, (205, 102, 0), ((stats_bottom_rect.topleft[0] - 10, stats_bottom_rect.topleft[1]),(stats_bottom_rect.size[0] + 20, stats_bottom_rect.size[1])))
                pygame.draw.rect(screen, (205, 102, 0), ((stats_bottom_rect.topleft[0], stats_bottom_rect.topleft[1] - 10), (stats_bottom_rect.size[0], stats_bottom_rect.size[1] + 20)))
                pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.bottomleft, 10)
                pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.bottomright, 10)
                pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.topleft, 10)
                pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.topright, 10)
                pygame.draw.rect(screen, (205, 205, 0), ((stats_top_rect.topleft[0] - 10, stats_top_rect.topleft[1]),(stats_top_rect.size[0] + 20, stats_top_rect.size[1])))
                pygame.draw.rect(screen, (205, 205, 0), ((stats_top_rect.topleft[0], stats_top_rect.topleft[1] - 10),(stats_top_rect.size[0], stats_top_rect.size[1] + 20)))
                pygame.draw.polygon(screen, (255, 140, 0), ((465, 22+30*player_turn), (465, 42+30*player_turn), (485, 32+30*player_turn)))

                stats = []
                for player in game.players:
                    if player.tank:
                        tank_health = player.tank.health
                    else:
                        tank_health = 0
                    stats.append(pygame.font.Font('freesansbold.ttf', 20).render(
                        f'{player}     score {player.score}     hp {tank_health}', True, player.color))
                for c, player_data in enumerate(stats):
                    text_rect = player_data.get_rect()
                    text_rect.x += 500
                    text_rect.y += 25 + 30*c
                    screen.blit(player_data, text_rect)

                for player in game.players:
                    tank = player.tank
                    if tank:
                        tank.draw(screen)
                        try:
                            if game.board[int(tank.y / 3) + 1][int(tank.x / 3)].ground == False:
                                tank.y += 1
                            if game.board[int(tank.y / 3) - 1][int(tank.x / 3)].ground == True:
                                tank.y -= 1
                            if game.board[int(tank.y / 3) - 5][int(tank.x / 3 + 3)].ground == True:
                                tank.x -= 1
                            if game.board[int(tank.y / 3) - 5][int(tank.x / 3 - 3)].ground == True:
                                tank.x += 1
                        except IndexError:
                            player.tank = None
                            game.explosion(tank.x, tank.y, 30)
                            game.dying_order.append(player)

                if game.players[player_turn].tank == None:
                    player_turn = game.next_turn(player_turn)

                if weapon != None:
                    if 0 < weapon.x < 900 and 0 < weapon.y < 600:
                        if game.board[int(weapon.y/3)][int(weapon.x/3)].ground == True:
                            game.explosion(weapon.x, weapon.y, 20)
                            weapon = None
                            wind = random.randint(-10, 10)
                            player_turn = game.next_turn(player_turn)
                        else:
                            weapon.draw(screen)
                            weapon.move(wind)
                    else:
                        weapon = None
                        wind = random.randint(-10, 10)
                        player_turn = game.next_turn(player_turn)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                try:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        game.players[player_turn].tank.move(-1)
                    if keys[pygame.K_RIGHT]:
                        game.players[player_turn].tank.move(1)
                    if keys[pygame.K_UP]:
                        game.players[player_turn].tank.move_gun(1)
                    if keys[pygame.K_DOWN]:
                        game.players[player_turn].tank.move_gun(-1)
                    if keys[pygame.K_SPACE] and weapon == None:
                        weapon = game.players[player_turn].tank.shot()
                    if shot_button.clicked() and weapon == None:
                        weapon = game.players[player_turn].tank.shot()
                    if exit_button.clicked():
                        exit_game_loop = True
                        break
                    power_slider.draw(game.players[player_turn].tank.max_shot_power)
                    game.players[player_turn].tank.shot_power = power_slider.clicked()
                    gun_direction_slider.draw(100)
                    game.players[player_turn].tank.gun_direction = 180 - 1.8 * gun_direction_slider.clicked()
                    shot_button.draw()
                    exit_button.draw()
                except AttributeError:
                    pass
                pygame.display.update()

                if players_alive == 1:
                    for c, player in enumerate(game.dying_order):
                        player.score += 500*c
                    [player for player in game.players if player not in game.dying_order][0].score += 800 * len(game.players)
                    break

        ranking = sorted(game.players, key=lambda player : player.score, reverse=True)

        screen.blit(background, (0, 0))
        run_round = True
        winner_text_down = pygame.font.Font('freesansbold.ttf', 30).render("WINNER", False, YELLOW)
        winner_text_rect_down = winner_text_down.get_rect()
        winner_text_rect_down.center = (450, 100)
        screen.blit(winner_text_down, winner_text_rect_down)
        winner_text_down = pygame.font.Font('freesansbold.ttf', 30).render("WINNER", False, ORANGE)
        winner_text_rect_down = winner_text_down.get_rect()
        winner_text_rect_down.center = (447, 97)
        screen.blit(winner_text_down, winner_text_rect_down)

        winner_text = pygame.font.Font('freesansbold.ttf', 30).render(f"{ranking[0]}", False, ranking[0].color)
        winner_text_rect = winner_text.get_rect()
        winner_text_rect.center = (450, 140)
        screen.blit(winner_text, winner_text_rect)

        second_text = pygame.font.Font('freesansbold.ttf', 15).render(f"2nd {ranking[1]}", False, ranking[1].color)
        second_text_rect = second_text.get_rect()
        second_text_rect.center = (450, 250)
        screen.blit(second_text, second_text_rect)

        if len(game.players) > 2:
            third_text = pygame.font.Font('freesansbold.ttf', 15).render(f"3rd {ranking[2]}", False, ranking[2].color)
            third_text_rect = third_text.get_rect()
            third_text_rect.center = (450, 280)
            screen.blit(third_text, third_text_rect)

        pygame.display.update()
        time.sleep(5)

        buttons['new game button'].active = True
        buttons['create game button'].active = False
        buttons['increase players button'].active = False
        buttons['increase num of rounds'].active = False
        buttons['decrease players button'].active = False
        buttons['decrease num of rounds'].active = False
        buttons['num of rounds'].active = False
        buttons['num of players'].active = False
        buttons['text num of rounds'].active = False
        buttons['text num of players'].active = False

    pygame.display.update()
