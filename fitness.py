from collections import deque

import numpy as np

from .maze import Maze


def bfs_reachability(grid):
    free_cells = [
        (r, c)
        for r in range(grid.shape[0])
        for c in range(grid.shape[1])
        if grid[r, c] == 0
    ]
    if not free_cells:
        return 0.0, set()

    start = free_cells[0]
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < grid.shape[0]
                and 0 <= nc < grid.shape[1]
                and grid[nr, nc] == 0
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(visited) / len(free_cells), visited


def is_finishable(grid):
    reachability, _ = bfs_reachability(grid)
    return 1.0 if reachability >= 0.95 else 0.0


def intersected_block_ratio(grid):
    rows, cols = grid.shape
    total_walls = 0
    intersected_walls = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                total_walls += 1
                has_wall_neighbor = False
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                        has_wall_neighbor = True
                        break
                if has_wall_neighbor:
                    intersected_walls += 1
    if total_walls == 0:
        return 0.0
    return intersected_walls / total_walls


def homogeneity_factor(grid):
    size = grid.shape[0]
    half = size // 2
    quadrants = [
        grid[:half, :half],
        grid[:half, half:],
        grid[half:, :half],
        grid[half:, half:],
    ]
    wall_counts = [np.sum(q == 1) for q in quadrants]
    total = sum(wall_counts)
    if total == 0:
        return 0.0
    mean = total / 4
    variance = sum((w - mean) ** 2 for w in wall_counts) / 4
    max_variance = mean**2
    if max_variance == 0:
        return 1.0
    return max(0.0, 1.0 - (variance / max_variance))


def horizontal_vertical_ratio(grid):
    h_walls = 0
    v_walls = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 1:
                if c + 1 < grid.shape[1] and grid[r, c + 1] == 1:
                    h_walls += 1
                if r + 1 < grid.shape[0] and grid[r + 1, c] == 1:
                    v_walls += 1
    if v_walls == 0:
        return float(h_walls) if h_walls > 0 else 0.0
    return h_walls / v_walls


def block_size_ratio(grid):
    size = grid.shape[0]
    interior_walls = int(np.sum(grid[1:size - 1, 1:size - 1] == 1))
    return (interior_walls - 48) / 48


def room_structure_ratio(grid):
    rows, cols = grid.shape
    corners = 0
    total_walls = int(np.sum(grid == 1))
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                wall_dirs = []
                for dr, dc, name in [
                    (-1, 0, "N"),
                    (1, 0, "S"),
                    (0, -1, "W"),
                    (0, 1, "E"),
                ]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 1:
                        wall_dirs.append(name)
                if len(wall_dirs) == 2:
                    if not (
                        ("N" in wall_dirs and "S" in wall_dirs)
                        or ("E" in wall_dirs and "W" in wall_dirs)
                    ):
                        corners += 1
    if total_walls == 0:
        return 0.0
    return corners / total_walls


def density_target_ratio(grid):
    size = grid.shape[0]
    interior_walls = int(np.sum(grid[1:size - 1, 1:size - 1] == 1))
    density = interior_walls / (size * size)
    target = 0.3
    return max(0.0, 1.0 - abs(density - target) * 2)


def symmetry_ratio(grid):
    size = grid.shape[0]
    half = size // 2
    n_UL = int(np.sum(grid[:half, :half] == 1))
    n_UR = int(np.sum(grid[:half, half:] == 1))
    n_LL = int(np.sum(grid[half:, :half] == 1))
    n_LR = int(np.sum(grid[half:, half:] == 1))
    S = abs(n_UL - n_UR + n_LL - n_LR)
    return max(0.0, 1.0 - S / (size * size))


def balance_ratio(grid):
    size = grid.shape[0]
    half = size // 2
    O_TR = int(np.sum(grid[:half, :] == 1))
    O_BR = int(np.sum(grid[half:, :] == 1))
    B = abs(O_TR - O_BR)
    return max(0.0, 1.0 - B / (size * size))


def fitness_improved(individual):
    maze = Maze.from_chromosome(individual)
    grid = maze.grid

    finish = is_finishable(grid)
    ibr = intersected_block_ratio(grid)
    hvr = horizontal_vertical_ratio(grid)
    rs = room_structure_ratio(grid)
    dr = density_target_ratio(grid)
    sr = symmetry_ratio(grid)
    br = balance_ratio(grid)

    fit = 0.25 * finish - 0.10 * ibr + 0.10 * hvr + 0.20 * rs + 0.15 * dr + 0.15 * sr + 0.10 * br
    return (fit,)


def fitness_base(individual):
    maze = Maze.from_chromosome(individual)
    grid = maze.grid

    finish = is_finishable(grid)
    ibr = intersected_block_ratio(grid)
    hf = homogeneity_factor(grid)
    hvr = horizontal_vertical_ratio(grid)
    bsr = block_size_ratio(grid)

    fit = 0.4 * finish - 0.1 * ibr + 0.2 * hf + 0.2 * hvr + 0.2 * bsr
    return (fit,)
