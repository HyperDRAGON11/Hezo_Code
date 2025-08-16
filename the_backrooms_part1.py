import pygame
import math
import sys
import random

# Settings
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 6
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
SCALE = WIDTH // NUM_RAYS
TILE = 80

# Maze generation
MAP_WIDTH, MAP_HEIGHT = 10, 8
MAP = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def generate_maze():
    stack = [(1, 1)]
    visited = set(stack)
    while stack:
        x, y = stack[-1]
        MAP[y][x] = 0
        neighbors = []
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx < MAP_WIDTH-1 and 1 <= ny < MAP_HEIGHT-1 and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        if neighbors:
            nx, ny = random.choice(neighbors)
            MAP[(y+ny)//2][(x+nx)//2] = 0
            stack.append((nx, ny))
            visited.add((nx, ny))
        else:
            stack.pop()

generate_maze()

# Player
player_x, player_y = TILE + TILE // 2, TILE + TILE // 2
player_angle = 0

# Monster
monster_x, monster_y = TILE * (MAP_WIDTH - 2), TILE * (MAP_HEIGHT - 2)
monster_speed = 1.2

# Audio
pygame.mixer.init()
try:
    hum = pygame.mixer.Sound("ambient_hum.wav")
    hum.play(-1)
    whisper = pygame.mixer.Sound("creepy_whisper.wav")
    heartbeat = pygame.mixer.Sound("heartbeat.wav")
    scream = pygame.mixer.Sound("scream.wav")
except:
    hum = whisper = heartbeat = scream = None

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

def mapping(x, y):
    return int(x // TILE), int(y // TILE)

def ray_casting(px, py, pa):
    rays = []
    wall_hits = []
    start_angle = pa - HALF_FOV
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        for depth in range(0, MAX_DEPTH, 4):
            target_x = px + depth * cos_a
            target_y = py + depth * sin_a
            map_x, map_y = mapping(target_x, target_y)
            if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                if MAP[map_y][map_x]:
                    depth *= math.cos(pa - angle)
                    rays.append((ray, depth))
                    wall_hits.append(depth)
                    break
    return rays, wall_hits

def draw_walls(rays):
    for ray, depth in rays:
        wall_height = min(HEIGHT, (TILE * 300) // (depth + 0.0001))
        brightness = 220 - min(180, depth // 4)
        color = (brightness, brightness, 170)
        pygame.draw.rect(
            screen, color,
            (ray * SCALE, HEIGHT // 2 - wall_height // 2, SCALE, wall_height)
        )

def move_player(keys):
    global player_x, player_y
    speed = 3
    dx = dy = 0
    if keys[pygame.K_w]:
        dx += math.cos(player_angle) * speed
        dy += math.sin(player_angle) * speed
    if keys[pygame.K_s]:
        dx -= math.cos(player_angle) * speed
        dy -= math.sin(player_angle) * speed
    nx, ny = player_x + dx, player_y + dy
    if MAP[int(ny // TILE)][int(nx // TILE)] == 0:
        player_x, player_y = nx, ny

def move_monster():
    global monster_x, monster_y
    dx = player_x - monster_x
    dy = player_y - monster_y
    distance = math.hypot(dx, dy)
    if distance > 10:
        mx = monster_x + monster_speed * dx / distance
        my = monster_y + monster_speed * dy / distance
        if MAP[int(my // TILE)][int(mx // TILE)] == 0:
            monster_x, monster_y = mx, my
    return distance

def draw_monster(wall_hits):
    dx = monster_x - player_x
    dy = monster_y - player_y
    angle_to_player = math.atan2(dy, dx)
    rel_angle = angle_to_player - player_angle
    while rel_angle < -math.pi:
        rel_angle += 2 * math.pi
    while rel_angle > math.pi:
        rel_angle -= 2 * math.pi
    if abs(rel_angle) < HALF_FOV:
        dist = math.hypot(dx, dy)
        ray_index = int((rel_angle + HALF_FOV) / DELTA_ANGLE)
        if ray_index < len(wall_hits) and dist < wall_hits[ray_index]:
            proj_height = max(20, min(HEIGHT, (TILE * 300) // (dist + 0.0001)))
            x = WIDTH // 2 + int((rel_angle / FOV) * WIDTH)
            pygame.draw.rect(
                screen, (255, 0, 0),
                (x - SCALE // 2, HEIGHT // 2 - proj_height // 2, SCALE, proj_height)
            )

def sanity_effect(distance):
    if distance < 150:
        if heartbeat:
            heartbeat.play()
        flicker = random.randint(0, 10) < 3
        if flicker:
            screen.fill((random.randint(100,255), random.randint(100,255), random.randint(100,255)))
    if random.randint(0, 300) == 1 and whisper:
        whisper.play()

def monster_death_animation():
    if scream:
        scream.play()
    for frame in range(60):
        screen.fill((random.randint(100, 255), 0, 0))
        size = int(HEIGHT * (frame / 60))
        pygame.draw.circle(screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), size)
        pygame.display.flip()
        clock.tick(60)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    keys = pygame.key.get_pressed()
    move_player(keys)

    # Mouse-based rotation
    mouse_dx = pygame.mouse.get_rel()[0]
    player_angle += mouse_dx * 0.002
    player_angle %= 2 * math.pi

    dist_to_monster = move_monster()
    rays, wall_hits = ray_casting(player_x, player_y, player_angle)
    draw_walls(rays)
    draw_monster(wall_hits)
    sanity_effect(dist_to_monster)

    if dist_to_monster < 30:
        monster_death_animation()
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)