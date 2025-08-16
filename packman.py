import pygame
import sys
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 560, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Grid
TILE = 20
ROWS, COLS = HEIGHT // TILE, WIDTH // TILE

# Maze layout (1 = wall, 0 = path)
maze = [
    "11111111111111111111",
    "10000000001100000001",
    "10111111101101111101",
    "10100000100000000101",
    "10101110111110110101",
    "10100010000010100101",
    "10111110111110111101",
    "10000000100000000001",
    "11111111111111111111"
]

# Convert to grid
grid = [[int(c) for c in row] for row in maze]
ROWS = len(grid)
COLS = len(grid[0])

# Pac-Man
pac_x, pac_y = 1, 1
pac_dir = (0, 0)
next_dir = (0, 0)
score = 0

# Dots
dots = {(x, y) for y in range(ROWS) for x in range(COLS) if grid[y][x] == 0}

# Ghosts
ghosts = [{"x": 18, "y": 7, "dir": random.choice([(1,0),(-1,0),(0,1),(0,-1)])}]

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif (x, y) in dots:
                pygame.draw.circle(screen, WHITE, rect.center, 3)

def move_pacman():
    global pac_x, pac_y, pac_dir, next_dir, score
    nx, ny = pac_x + next_dir[0], pac_y + next_dir[1]
    if grid[ny][nx] == 0:
        pac_dir = next_dir
    nx, ny = pac_x + pac_dir[0], pac_y + pac_dir[1]
    if grid[ny][nx] == 0:
        pac_x, pac_y = nx, ny
        if (pac_x, pac_y) in dots:
            dots.remove((pac_x, pac_y))
            score += 10

def draw_pacman():
    rect = pygame.Rect(pac_x*TILE, pac_y*TILE, TILE, TILE)
    pygame.draw.circle(screen, YELLOW, rect.center, TILE//2 - 2)

def move_ghosts():
    for ghost in ghosts:
        gx, gy = ghost["x"], ghost["y"]
        dx, dy = ghost["dir"]
        nx, ny = gx + dx, gy + dy
        if grid[ny][nx] == 0:
            ghost["x"], ghost["y"] = nx, ny
        else:
            ghost["dir"] = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

def draw_ghosts():
    for ghost in ghosts:
        rect = pygame.Rect(ghost["x"]*TILE, ghost["y"]*TILE, TILE, TILE)
        pygame.draw.circle(screen, RED, rect.center, TILE//2 - 2)

def check_collision():
    for ghost in ghosts:
        if ghost["x"] == pac_x and ghost["y"] == pac_y:
            return True
    return False

def draw_score():
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, HEIGHT - 40))

# Game loop
while True:
    screen.fill(BLACK)
    draw_maze()
    draw_pacman()
    draw_ghosts()
    draw_score()

    move_pacman()
    move_ghosts()

    if check_collision():
        print("Game Over!")
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: next_dir = (-1, 0)
            if event.key == pygame.K_RIGHT: next_dir = (1, 0)
            if event.key == pygame.K_UP: next_dir = (0, -1)
            if event.key == pygame.K_DOWN: next_dir = (0, 1)

    pygame.display.flip()
    clock.tick(10)