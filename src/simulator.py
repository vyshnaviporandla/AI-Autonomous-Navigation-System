import time
from pathlib import Path

import pygame

from src.astar import astar
from src.config import (
    CELL_SIZE, COLS, ROWS, TOP_BAR, WINDOW_WIDTH, WINDOW_HEIGHT,
    FPS, AGENT_STEP_FRAMES, START, GOAL
)
from src.grid import build_grid
from src.metrics import save_run


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI-Based Autonomous Navigation System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18)
    small_font = pygame.font.SysFont("arial", 14)

    grid = build_grid()
    path = astar(grid, START, GOAL)
    if not path:
        print("No valid path found. Check the map and start/goal positions.")
        pygame.quit()
        return

    print(f"Path found: {len(path)} nodes")
    print("Controls: SPACE = pause/resume | R = restart | S = save screenshot | ESC = quit")

    agent_index = 0
    frame_counter = 0
    paused = False
    finished = False
    start_time = time.perf_counter()
    end_time = None
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not finished:
                    paused = not paused
                elif event.key == pygame.K_r:
                    agent_index = 0
                    frame_counter = 0
                    paused = False
                    finished = False
                    start_time = time.perf_counter()
                    end_time = None
                elif event.key == pygame.K_s:
                    screenshot_path = output_dir / "navigation_demo.png"
                    pygame.image.save(screen, screenshot_path)
                    print(f"Screenshot saved to {screenshot_path}")

        if not paused and not finished:
            frame_counter += 1
            if frame_counter >= AGENT_STEP_FRAMES:
                frame_counter = 0
                if agent_index < len(path) - 1:
                    agent_index += 1
                if agent_index >= len(path) - 1:
                    finished = True
                    end_time = time.perf_counter()
                    elapsed = end_time - start_time
                    save_run(output_dir / "run_metrics.csv", "success", len(path),
                             len(path) - 1, elapsed)
                    print(f"Goal reached! Movement steps: {len(path)-1}; time: {elapsed:.2f}s")
                    print(f"Metrics saved to {output_dir / 'run_metrics.csv'}")

        screen.fill((245, 247, 250))
        header = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR)
        pygame.draw.rect(screen, (28, 39, 56), header)
        title = font.render("AI-Based Autonomous Navigation System", True, (255, 255, 255))
        screen.blit(title, (12, 8))
        status = "GOAL REACHED" if finished else ("PAUSED" if paused else "NAVIGATING")
        info = small_font.render(
            f"Status: {status}   |   Path nodes: {len(path)}   |   SPACE pause  R restart  S screenshot",
            True, (220, 230, 240))
        screen.blit(info, (12, 38))

        # Draw grid cells.
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(x * CELL_SIZE, TOP_BAR + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, (65, 73, 86), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (218, 224, 231), rect, 1)

        # Draw planned path.
        for x, y in path:
            rect = pygame.Rect(x * CELL_SIZE + 5, TOP_BAR + y * CELL_SIZE + 5,
                               CELL_SIZE - 10, CELL_SIZE - 10)
            pygame.draw.rect(screen, (94, 190, 143), rect, border_radius=4)

        # Start and goal markers.
        sx, sy = START
        gx, gy = GOAL
        pygame.draw.rect(screen, (55, 130, 230),
                         (sx * CELL_SIZE + 2, TOP_BAR + sy * CELL_SIZE + 2,
                          CELL_SIZE - 4, CELL_SIZE - 4), border_radius=6)
        pygame.draw.rect(screen, (230, 90, 80),
                         (gx * CELL_SIZE + 2, TOP_BAR + gy * CELL_SIZE + 2,
                          CELL_SIZE - 4, CELL_SIZE - 4), border_radius=6)

        # Draw the moving virtual agent.
        ax, ay = path[agent_index]
        center = (ax * CELL_SIZE + CELL_SIZE // 2,
                  TOP_BAR + ay * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, (255, 196, 61), center, CELL_SIZE // 3)
        pygame.draw.circle(screen, (35, 43, 55), center, CELL_SIZE // 3, 2)

        pygame.display.flip()
        clock.tick(FPS)

    # Save a final metrics row if the user closes early.
    if not finished:
        save_run(output_dir / "run_metrics.csv", "stopped_early", len(path),
                 agent_index, time.perf_counter() - start_time)
    pygame.quit()
