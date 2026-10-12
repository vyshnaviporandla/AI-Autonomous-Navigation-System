# AI-Based Autonomous Navigation System

A beginner-friendly autonomous navigation demo using a 2D virtual environment, Python, Pygame, and the A* path-planning algorithm. The virtual agent finds a route around blocked grid cells and animates its movement from a start point to a goal.

> **Scope note:** This is a simulation-based learning project. It is not a road-ready self-driving system and does not yet include camera perception, trained object detection, real sensors, or hardware control.

## Problem statement
A mobile agent must travel from a start location to a destination without entering obstacle cells. The program builds a grid map, computes a path, visualizes it, and moves the agent along that route.

## Industry relevance
Grid-based planning introduces concepts used in robotics and automation: environment representation, graph search, obstacle-aware routing, simulation, testing, and run metrics. Industrial systems require additional sensing, localization, control, and safety validation.

## Features
- 2D virtual environment with fixed obstacles
- A* path planning using Manhattan distance
- Animated virtual agent
- Pause, restart, screenshot, and quit controls
- CSV run summary
- Unit tests for the path planner

## Tech stack
- Python 3.10 or 3.11
- Pygame
- Python standard library (`heapq`, `csv`, `unittest`)

## Architecture
```text
Grid map + start/goal
        |
        v
Grid representation (src/grid.py)
        |
        v
A* planner (src/astar.py)
        |
        v
Planned route
        |
        v
Pygame simulator (src/simulator.py)
        |
        +--> Animated visualization
        +--> outputs/run_metrics.csv
```

## Folder structure
```text
AI-Autonomous-Navigation-System/
├── docs/                  # Project notes and milestones
├── outputs/               # Generated metrics and screenshots
├── src/
│   ├── astar.py            # A* path-planning algorithm
│   ├── config.py           # Map and display settings
│   ├── grid.py             # Grid and obstacle map
│   ├── metrics.py          # CSV run summaries
│   └── simulator.py       # Pygame visualization and agent movement
├── tests/
│   └── test_astar.py       # Unit tests
├── main.py                 # Application entry point
├── requirements.txt
└── README.md
```

## Installation

### Windows (PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
From the project root, with the virtual environment activated:
```bash
python main.py
```

Controls:
- `SPACE`: pause/resume
- `R`: restart
- `S`: save the current screen to `outputs/navigation_demo.png`
- `ESC`: quit

When the agent reaches the goal, the terminal reports success and `outputs/run_metrics.csv` is written.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Results
The expected demonstration shows:
- Dark cells: obstacles
- Green cells: planned route
- Blue marker: start
- Red marker: goal
- Yellow circle: virtual agent

The CSV records status, number of path nodes, movement steps, and elapsed runtime. Record actual results after running the project; do not claim measurements that have not been collected.

## Screenshots and demo
Save evidence under `images/` or `outputs/`, for example:
- `images/01_environment.png`
- `images/02_planned_path.png`
- `images/03_goal_reached.png`
- `images/04_github_repo.png`

Use relative Markdown links, e.g. `![Navigation demo](images/03_goal_reached.png)`. Add only screenshots you actually captured from your run.

## Future improvements
- Randomized maps and automated test scenarios
- Replanning when obstacles change
- OpenCV-based camera perception
- Lightweight object detection model
- ROS 2 integration
- CARLA or Gazebo integration
- Localization and mapping
- More realistic motion and collision models

## Learning outcomes
- Representing a world as a grid
- Implementing A* search
- Separating code into modules
- Visualizing a navigation algorithm
- Writing unit tests and run metrics
- Documenting and version-controlling a project

## Author
Add your name, GitHub profile, and contact details here before publishing.
