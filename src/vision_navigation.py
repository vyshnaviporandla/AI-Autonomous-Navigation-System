
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

from config import COLS, ROWS, START, GOAL, OBSTACLE_RECTS
from astar import astar


ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = ROOT / "images" / "test.jpg"
MODEL_PATH = ROOT / "yolo11n.pt"
OUTPUT_PATH = ROOT / "outputs" / "vision_navigation.png"

CELL_SIZE = 28
TOP_BAR = 45


def build_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    for left, top, width, height in OBSTACLE_RECTS:
        for y in range(top, top + height):
            for x in range(left, left + width):
                if 0 <= x < COLS and 0 <= y < ROWS:
                    grid[y][x] = 1

    return grid


def main():
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    model = YOLO(str(MODEL_PATH))
    results = model.predict(
        source=str(IMAGE_PATH),
        conf=0.35,
        verbose=False,
    )

    grid = build_grid()
    original_obstacles = {
        (x, y)
        for y in range(ROWS)
        for x in range(COLS)
        if grid[y][x] == 1
    }
    detected_cells = set()

    image_height, image_width = results[0].orig_shape

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            name = result.names[class_id]

            if confidence < 0.35:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Approximate mapping of the bounding-box bottom center to a cell.
            image_x = (x1 + x2) / 2
            image_y = y2

            col = min(COLS - 1, max(
                0, int(image_x / image_width * COLS)
            ))
            row = min(ROWS - 1, max(
                0, int(image_y / image_height * ROWS)
            ))

            print(
                f"{name}: confidence={confidence:.2f}, "
                f"cell=({col}, {row})"
            )

            if name in {
                "person", "bus", "car", "truck",
                "bicycle", "motorcycle"
            }:
                cell = (col, row)

                if cell not in {START, GOAL}:
                    if grid[row][col] == 0:
                        grid[row][col] = 1
                        detected_cells.add(cell)

    path = astar(grid, START, GOAL)

    print(f"\nDetected obstacle cells: {sorted(detected_cells)}")

    if path:
        print(f"A* found a path containing {len(path)} cells.")
    else:
        print("No path found.")

    # Create a visual grid image.
    width = COLS * CELL_SIZE
    height = TOP_BAR + ROWS * CELL_SIZE

    canvas = np.full((height, width, 3), 245, dtype=np.uint8)
    canvas[:TOP_BAR] = (35, 35, 35)

    cv2.putText(
        canvas,
        "AI Navigation: YOLO Obstacles + A* Path",
        (10, 29),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )

    # Draw cells and grid lines.
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_SIZE
            y1 = TOP_BAR + row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color = (245, 245, 245)

            if (col, row) in original_obstacles:
                color = (75, 75, 75)

            if path and (col, row) in path:
                color = (80, 200, 100)

            if (col, row) in detected_cells:
                color = (190, 80, 190)

            cv2.rectangle(
                canvas, (x1, y1), (x2, y2), color, -1
            )
            cv2.rectangle(
                canvas, (x1, y1), (x2, y2), (210, 210, 210), 1
            )

    # Highlight start and goal.
    for cell, color, label in [
        (START, (0, 200, 0), "S"),
        (GOAL, (0, 0, 255), "G"),
    ]:
        col, row = cell
        x = col * CELL_SIZE
        y = TOP_BAR + row * CELL_SIZE

        cv2.rectangle(
            canvas,
            (x + 2, y + 2),
            (x + CELL_SIZE - 2, y + CELL_SIZE - 2),
            color,
            -1,
        )
        cv2.putText(
            canvas,
            label,
            (x + 7, y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), canvas):
        raise RuntimeError(f"Could not save image: {OUTPUT_PATH}")

    print(f"\nNavigation map saved to: {OUTPUT_PATH}")
    print(
        "Legend: green = A* path, gray = fixed barriers, "
        "purple = newly detected obstacles, "
        "green S = start, red G = goal."
    )
    print(
        "Note: mapping objects from a single photo to grid cells "
        "is approximate; this is a simulation demonstration."
    )


if __name__ == "__main__":
    main()
