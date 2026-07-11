import pygame
import sys
from pacman_ga.maze import Maze
from pacman_ga.fitness import bfs_reachability

TILE_SIZE = 20
WALL_COLOR = (0, 0, 255)
PATH_COLOR = (0, 0, 0)
DOT_COLOR = (255, 0, 0)
UNREACHABLE_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)


def draw_maze(screen, maze, reachable_cells=None, offset_x=0, offset_y=0):
    for r in range(maze.SIZE):
        for c in range(maze.SIZE):
            rect = pygame.Rect(
                offset_x + c * TILE_SIZE,
                offset_y + r * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            if maze.grid[r, c] == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)
                center = (
                    offset_x + c * TILE_SIZE + TILE_SIZE // 2,
                    offset_y + r * TILE_SIZE + TILE_SIZE // 2
                )
                if reachable_cells and (r, c) in reachable_cells:
                    color = DOT_COLOR
                else:
                    color = UNREACHABLE_COLOR
                pygame.draw.circle(screen, color, center, 2)


def visualize_maze(individual, title="Laberinto"):
    pygame.init()
    screen_w = Maze.SIZE * TILE_SIZE + 40
    screen_h = Maze.SIZE * TILE_SIZE + 80
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption(title)

    maze = Maze.from_chromosome(individual)
    _, reachable = bfs_reachability(maze.grid)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BG_COLOR)

        font = pygame.font.SysFont("monospace", 16)
        text = font.render(title, True, (255, 255, 255))
        screen.blit(text, (20, 10))

        draw_maze(screen, maze, reachable, offset_x=20, offset_y=40)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def save_maze_image(individual, filename, title="Laberinto"):
    pygame.init()
    screen_w = Maze.SIZE * TILE_SIZE + 40
    screen_h = Maze.SIZE * TILE_SIZE + 80
    screen = pygame.display.set_mode((screen_w, screen_h))

    maze = Maze.from_chromosome(individual)
    _, reachable = bfs_reachability(maze.grid)

    screen.fill(BG_COLOR)
    font = pygame.font.SysFont("monospace", 16)
    text = font.render(title, True, (255, 255, 255))
    screen.blit(text, (20, 10))
    draw_maze(screen, maze, reachable, offset_x=20, offset_y=40)

    pygame.image.save(screen, filename)
    pygame.quit()
    print(f"  Imagen guardada: {filename}")
