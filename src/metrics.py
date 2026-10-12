import csv
from pathlib import Path


def save_run(path, status, path_nodes, steps, elapsed_seconds):
    """Write a small, reproducible run summary to CSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["status", "path_nodes", "movement_steps", "elapsed_seconds"])
        writer.writerow([status, path_nodes, steps, f"{elapsed_seconds:.3f}"])
