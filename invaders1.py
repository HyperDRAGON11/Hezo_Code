import pygame
import random
import math
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player_img = pygame.Surface((50, 30))
player_img.fill((0, 255, 0))
player_x = 370
player_y = 480 
player_speed = 0

enemy_img = pygame.Surface((40, 30))
enemy_img.fill((255, 0, 0))
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6
for _ in range(num_enemies):
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(40)

bullet_img = pygame.Surface((5, 15))
bullet_img.fill((255, 255, 0))
bullet_x = 0
bullet_y = 480
bullet_y_change = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font(None, 36)
over_font = pygame.font.Font(None, 64)

def show_score():
    score = font.render(f"Score: {score_value}", True, WHITE)
    screen.blit(score, (10, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (300, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 22, y - 15))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = -4
            if event.key == pygame.K_RIGHT:
                player_speed = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_speed = 0

    player_x += player_speed
    if player_x <= 0:
        player_x = 0
    elif player_x >= 750:
        player_x = 750

    for i in range(num_enemies):
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 250 
            game_over_text()
            running = False
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 760:
            enemy_x_change[i] = -2
            enemy_y[i] += enemy_y_change[i]
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    player(player_x, player_y)
    show_score()
    pygame.display.update()

pygame.quit()
sys.exit()
