import numpy as np


class Maze:
    SIZE = 20

    def __init__(self, grid=None):
        if grid is None:
            self.grid = np.random.randint(0, 2, (self.SIZE, self.SIZE))
        else:
            self.grid = np.array(grid, dtype=int).reshape(self.SIZE, self.SIZE)
        self._enforce_borders()

    def _enforce_borders(self):
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1

    def to_chromosome(self):
        return self.grid.flatten().tolist()

    @staticmethod
    def from_chromosome(chromosome):
        return Maze(grid=np.array(chromosome).reshape(Maze.SIZE, Maze.SIZE))

    def get_free_cells(self):
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if self.grid[r, c] == 0]

    def get_wall_cells(self):
        return [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if self.grid[r, c] == 1]


def enforce_borders(individual):
    size = Maze.SIZE
    grid = np.array(individual).reshape(size, size)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1
    return grid.flatten().tolist()
