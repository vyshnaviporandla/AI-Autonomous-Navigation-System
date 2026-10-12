# Window and grid configuration
CELL_SIZE = 28
COLS = 30
ROWS = 20
TOP_BAR = 70
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE + TOP_BAR
FPS = 60
AGENT_STEP_FRAMES = 8

# Grid coordinates are (column, row)
START = (1, 1)
GOAL = (28, 18)

# Rectangular obstacles: (left, top, width, height), in grid cells.
OBSTACLE_RECTS = [
    (5, 0, 2, 12),
    (10, 7, 2, 13),
    (15, 0, 2, 11),
    (20, 8, 2, 12),
    (25, 0, 2, 11),
]
