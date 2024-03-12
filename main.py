import random
import sys
import pygame
from pygame.locals import *

# Customized Constants
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT * 0.8
CUSTOM_GAME_SPRITES = {}
CUSTOM_GAME_SOUNDS = {}
PLAYER_IMAGE = 'images/bird.png'
BACKGROUND_IMAGE = 'images/background.png'
PIPE_IMAGE = 'images/pipe.png'


def welcome_screen():
    """
    Displays welcome images on the screen
    """
    player_x = int(SCREEN_WIDTH / 5)
    player_y = int((SCREEN_HEIGHT - CUSTOM_GAME_SPRITES['player'].get_height()) / 2)
    message_x = int((SCREEN_WIDTH - CUSTOM_GAME_SPRITES['message'].get_width()) / 2)
    message_y = int(SCREEN_HEIGHT * 0.13)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
        SCREEN.blit(CUSTOM_GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(CUSTOM_GAME_SPRITES['player'], (player_x, player_y))
        SCREEN.blit(CUSTOM_GAME_SPRITES['message'], (message_x, message_y))
        SCREEN.blit(CUSTOM_GAME_SPRITES['base'], (base_x, GROUND_Y))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main_game():
    score = 0
    player_x = int(SCREEN_WIDTH / 5)
    player_y = int(SCREEN_WIDTH / 2)
    base_x = 0

    new_pipe_1 = get_random_pipe()
    new_pipe_2 = get_random_pipe()

    upper_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': new_pipe_1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': new_pipe_2[0]['y']},
    ]

    lower_pipes = [
        {'x': SCREEN_WIDTH + 200, 'y': new_pipe_1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': new_pipe_2[1]['y']},
    ]

    pipe_velocity_x = -4

    player_velocity_y = -9
    player_max_velocity_y = 10
    player_min_velocity_y = -8
    player_acceleration_y = 1

    player_flap_acceleration = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_velocity_y = player_flap_acceleration
                    player_flapped = True
                    CUSTOM_GAME_SOUNDS['wing'].play()

        crash_test = is_collide(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            return

        player_mid_position = player_x + CUSTOM_GAME_SPRITES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_position = pipe['x'] + CUSTOM_GAME_SPRITES['pipe'][0].get_width() / 2
            if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                score += 1
                print(f"Your score is {score}")
                CUSTOM_GAME_SOUNDS['point'].play()

        if player_velocity_y < player_max_velocity_y and not player_flapped:
            player_velocity_y += player_acceleration_y

        if player_flapped:
            player_flapped = False

        player_height = CUSTOM_GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_velocity_y, GROUND_Y - player_y - player_height)

        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_velocity_x
            lower_pipe['x'] += pipe_velocity_x

        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        if upper_pipes[0]['x'] < -CUSTOM_GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        SCREEN.blit(CUSTOM_GAME_SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(CUSTOM_GAME_SPRITES['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(CUSTOM_GAME_SPRITES['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        SCREEN.blit(CUSTOM_GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(CUSTOM_GAME_SPRITES['player'], (player_x, player_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += CUSTOM_GAME_SPRITES['numbers'][digit].get_width()
        X_offset = (SCREEN_WIDTH - width) / 2

        for digit in my_digits:
            SCREEN.blit(CUSTOM_GAME_SPRITES['numbers'][digit], (X_offset, SCREEN_HEIGHT * 0.12))
            X_offset += CUSTOM_GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > GROUND_Y - 25 or player_y < 0:
        CUSTOM_GAME_SOUNDS['hit'].play()
        return True

    for pipe in upper_pipes:
        pipe_height = CUSTOM_GAME_SPRITES['pipe'][0].get_height()
        if player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < CUSTOM_GAME_SPRITES['pipe'][0].get_width():
            CUSTOM_GAME_SOUNDS['hit'].play()
            return True

    for pipe in lower_pipes:
        if (player_y + CUSTOM_GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < \
                CUSTOM_GAME_SPRITES['pipe'][0].get_width():
            CUSTOM_GAME_SOUNDS['hit'].play()
            return True

    return False


def get_random_pipe():
    pipe_height = CUSTOM_GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - CUSTOM_GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREEN_WIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},  # upper Pipe
        {'x': pipe_x, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('My Flappy Bird')
    CUSTOM_GAME_SPRITES['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

    CUSTOM_GAME_SPRITES['message'] = pygame.image.load('images/message.png').convert_alpha()
    CUSTOM_GAME_SPRITES['base'] = pygame.image.load('images/base.png').convert_alpha()
    CUSTOM_GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE_IMAGE).convert_alpha(), 180),
        pygame.image.load(PIPE_IMAGE).convert_alpha()
    )

    CUSTOM_GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    CUSTOM_GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    CUSTOM_GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    CUSTOM_GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    CUSTOM_GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

    CUSTOM_GAME_SPRITES['background'] = pygame.image.load(BACKGROUND_IMAGE).convert()
    CUSTOM_GAME_SPRITES['player'] = pygame.image.load(PLAYER_IMAGE).convert_alpha()

    while True:
        welcome_screen()
        main_game()
