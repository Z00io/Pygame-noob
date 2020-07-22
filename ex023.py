import pygame
import random
import sys

pygame.init()

WIDTH: int = 900
HEIGHT: int = 700
BACKGROUND_COLOR: int = (0, 0, 0)

YELLOW =  (255, 255, 0)
RED: int = (255, 0, 0)
BLUE: int = (0, 0, 255)
player_size: int = 50
player_pos: int = [WIDTH / 2, HEIGHT - 2 * player_size]

enemy_size: int = 50
enemy_pos: int = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

font = pygame.font.SysFont('monospace', 35)

def set_level(score, SPEED):
    if score < 20:
        SPEED = 12
    elif score < 40:
        SPEED = 14
    elif score < 60:
        SPEED = 16
    elif score < 80:
        SPEED = 18
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 12 and delay < 0.3:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def drawn_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size * 1
            elif event.key == pygame.K_RIGHT:
                x += player_size * 1

            player_pos = [x, y]
    screen.fill(BACKGROUND_COLOR)

    #

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score:" + str(score)
    label = font.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 300, HEIGHT - 100))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    drawn_enemies(enemy_list)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(50)
    pygame.display.update()
