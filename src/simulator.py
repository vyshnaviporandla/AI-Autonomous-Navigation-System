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


DYNAMIC_OBSTACLE_TRIGGER = 16
OBSTACLE_AHEAD = 4


def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI-Based Autonomous Navigation System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 18)
    small_font = pygame.font.SysFont("arial", 14)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    def reset_simulation():
        grid = build_grid()
        path = astar(grid, START, GOAL)
        if not path:
            return None

        return {
            "grid": grid,
            "path": path,
            "initial_path_nodes": len(path),
            "agent_index": 0,
            "frame_counter": 0,
            "paused": False,
            "finished": False,
            "no_route": False,
            "obstacle_added": False,
            "dynamic_obstacle": None,
            "replanned": False,
            "start_time": time.perf_counter(),
            "total_steps": 0,
        }

    state = reset_simulation()
    if state is None:
        print("No valid initial path found. Check the map.")
        pygame.quit()
        return

    print(f"Initial path found: {len(state['path'])} nodes")
    print(
        "Controls: SPACE = pause/resume | R = restart | "
        "S = save screenshot | ESC = quit"
    )
    print("A temporary obstacle will appear automatically during the run.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE and not state["finished"]:
                    state["paused"] = not state["paused"]

                elif event.key == pygame.K_r:
                    state = reset_simulation()
                    if state is None:
                        print("Unable to restart: no initial path found.")
                        running = False
                    else:
                        print("Simulation restarted.")

                elif event.key == pygame.K_s:
                    screenshot_path = output_dir / "navigation_demo.png"
                    pygame.image.save(screen, screenshot_path)
                    print(f"Screenshot saved to {screenshot_path}")

        if not running:
            break

        if not state["paused"] and not state["finished"]:
            state["frame_counter"] += 1

            if state["frame_counter"] >= AGENT_STEP_FRAMES:
                state["frame_counter"] = 0

                if state["agent_index"] < len(state["path"]) - 1:
                    state["agent_index"] += 1
                    state["total_steps"] += 1

                # Add one temporary obstacle ahead of the moving agent.
                if (
                    not state["obstacle_added"]
                    and state["agent_index"] >= DYNAMIC_OBSTACLE_TRIGGER
                ):
                    obstacle_index = state["agent_index"] + OBSTACLE_AHEAD
                    current_position = state["path"][state["agent_index"]]

                    if obstacle_index < len(state["path"]) - 1:
                        obstacle = state["path"][obstacle_index]
                        ox, oy = obstacle

                        # Never block the agent's current cell or the goal.
                        if obstacle != current_position and obstacle != GOAL:
                            state["grid"][oy][ox] = 1
                            state["dynamic_obstacle"] = obstacle
                            state["obstacle_added"] = True

                            print(f"Dynamic obstacle appeared at {obstacle}.")
                            print("Checking the remaining route with A*...")

                            new_path = astar(
                                state["grid"], current_position, GOAL
                            )

                            if new_path:
                                state["path"] = new_path
                                state["agent_index"] = 0
                                state["replanned"] = True
                                print(
                                    "Route replanned successfully: "
                                    f"{len(new_path)} nodes remaining."
                                )
                            else:
                                state["no_route"] = True
                                state["finished"] = True
                                elapsed = (
                                    time.perf_counter() - state["start_time"]
                                )
                                save_run(
                                    output_dir / "run_metrics.csv",
                                    "no_path",
                                    state["initial_path_nodes"],
                                    state["total_steps"],
                                    elapsed,
                                )
                                print("No safe route remains. Agent stopped.")

                # Check whether the agent reached the goal.
                if not state["finished"] and state["path"][
                    state["agent_index"]
                ] == GOAL:
                    state["finished"] = True
                    elapsed = time.perf_counter() - state["start_time"]
                    save_run(
                        output_dir / "run_metrics.csv",
                        "success",
                        state["initial_path_nodes"],
                        state["total_steps"],
                        elapsed,
                    )
                    print(
                        f"Goal reached! Total movement steps: "
                        f"{state['total_steps']}; time: {elapsed:.2f}s"
                    )
                    print(f"Metrics saved to {output_dir / 'run_metrics.csv'}")

        # Draw the scene.
        screen.fill((245, 247, 250))
        header = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR)
        pygame.draw.rect(screen, (28, 39, 56), header)

        title = font.render(
            "AI-Based Autonomous Navigation System",
            True,
            (255, 255, 255),
        )
        screen.blit(title, (12, 8))

        if state["no_route"]:
            status = "NO ROUTE - AGENT STOPPED"
        elif state["finished"]:
            status = "GOAL REACHED"
        elif state["paused"]:
            status = "PAUSED"
        elif state["replanned"]:
            status = "ROUTE REPLANNED"
        else:
            status = "NAVIGATING"

        info = small_font.render(
            f"Status: {status} | Route nodes: {len(state['path'])} | "
            "SPACE pause  R restart  S screenshot",
            True,
            (220, 230, 240),
        )
        screen.blit(info, (12, 38))

        # Draw free cells and the original obstacles.
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    TOP_BAR + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                if state["grid"][y][x] == 1:
                    pygame.draw.rect(screen, (65, 73, 86), rect)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (218, 224, 231), rect, 1)

        # Draw the currently planned route.
        for x, y in state["path"]:
            rect = pygame.Rect(
                x * CELL_SIZE + 5,
                TOP_BAR + y * CELL_SIZE + 5,
                CELL_SIZE - 10,
                CELL_SIZE - 10,
            )
            pygame.draw.rect(
                screen, (94, 190, 143), rect, border_radius=4
            )

        # Highlight the temporary obstacle in purple.
        if state["dynamic_obstacle"] is not None:
            ox, oy = state["dynamic_obstacle"]
            rect = pygame.Rect(
                ox * CELL_SIZE + 2,
                TOP_BAR + oy * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            )
            pygame.draw.rect(
                screen, (160, 70, 190), rect, border_radius=4
            )

        # Start and goal markers.
        sx, sy = START
        gx, gy = GOAL
        pygame.draw.rect(
            screen,
            (55, 130, 230),
            (
                sx * CELL_SIZE + 2,
                TOP_BAR + sy * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            ),
            border_radius=6,
        )
        pygame.draw.rect(
            screen,
            (230, 90, 80),
            (
                gx * CELL_SIZE + 2,
                TOP_BAR + gy * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4,
            ),
            border_radius=6,
        )

        # Draw the virtual agent at its current position.
        ax, ay = state["path"][state["agent_index"]]
        center = (
            ax * CELL_SIZE + CELL_SIZE // 2,
            TOP_BAR + ay * CELL_SIZE + CELL_SIZE // 2,
        )
        pygame.draw.circle(
            screen, (255, 196, 61), center, CELL_SIZE // 3
        )
        pygame.draw.circle(
            screen, (35, 43, 55), center, CELL_SIZE // 3, 2
        )

        pygame.display.flip()
        clock.tick(FPS)

    # Record an early stop, but don't duplicate completed-run metrics.
    if not state["finished"]:
        save_run(
            output_dir / "run_metrics.csv",
            "stopped_early",
            state["initial_path_nodes"],
            state["total_steps"],
            time.perf_counter() - state["start_time"],
        )

    pygame.quit()


if __name__ == "__main__":
    run_simulation()