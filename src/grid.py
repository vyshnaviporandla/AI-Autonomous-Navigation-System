from src.config import COLS, ROWS, OBSTACLE_RECTS, START, GOAL


def build_grid():
    """Return a 2D grid: 0 means free, 1 means blocked."""
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for left, top, width, height in OBSTACLE_RECTS:
        for y in range(top, min(top + height, ROWS)):
            for x in range(left, min(left + width, COLS)):
                grid[y][x] = 1

    # Keep endpoints open even if the map is later edited.
    sx, sy = START
    gx, gy = GOAL
    grid[sy][sx] = 0
    grid[gy][gx] = 0
    return grid


def in_bounds(grid, node):
    x, y = node
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def is_walkable(grid, node):
    x, y = node
    return in_bounds(grid, node) and grid[y][x] == 0
