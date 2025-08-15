import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame Window")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button
            running = False

    # Fill the screen
    screen.fill(WHITE)

    # Draw a red circle
    pygame.draw.circle(screen, RED, (400, 300), 50)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
