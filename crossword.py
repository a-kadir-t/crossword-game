# Hell yeah! The first lines of the code of the most fun crossword puzzle ever!

import pygame
import sys

# Constants
GRID_SIZE = 10
CELL_SIZE = 50
MARGIN = 2
SCREEN_SIZE = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)

def draw_grid(screen):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(
                col * (CELL_SIZE + MARGIN) + MARGIN,
                row * (CELL_SIZE + MARGIN) + MARGIN,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, LINE_COLOR, rect, width=1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Crossword Grid")
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_grid(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
