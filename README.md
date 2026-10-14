# AI-Based Autonomous Navigation System

An AI-assisted navigation simulation that combines **A\* path planning, dynamic obstacle replanning, YOLO object detection, OpenCV image processing, and Pygame visualization** in a virtual environment.

The project demonstrates how a virtual agent can plan a route around obstacles, react to a simulated obstacle appearing during movement, and use object detections from an image to create an approximate grid-based navigation plan.

> **Scope and limitations:** This is a software-only simulation and learning project. It does not control a physical robot or vehicle. YOLO detections mapped from a single image to grid cells are approximate and do not provide reliable real-world depth, localization, or obstacle distances.

## Problem Statement

A virtual agent must travel from a defined start position to a goal while avoiding blocked grid cells. The system uses A\* search to calculate a path, visualizes the agent's movement, and demonstrates replanning when a temporary obstacle blocks the planned route.

A separate vision-navigation module uses YOLO to detect objects in an image, approximates their positions on the simulation grid, and calculates a route around the resulting obstacle cells.

## Objectives

- Implement grid-based path planning using A\*.
- Visualize autonomous agent movement in a 2D environment.
- Demonstrate dynamic obstacle insertion and route replanning.
- Detect objects in images using a pretrained YOLO model.
- Process images with OpenCV.
- Map selected object detections to approximate grid cells.
- Record simulation results and maintain automated tests.

## Features

- **A\* path planning:** Finds a shortest path on a four-direction grid using Manhattan distance.
- **Dynamic replanning:** Recalculates a route when a temporary obstacle is added during simulation.
- **Pygame visualization:** Displays the grid, obstacles, route, agent, start, and goal.
- **YOLO object detection:** Detects objects in an input image using a pretrained model.
- **Vision-based navigation demo:** Maps selected detections to grid cells and runs A\* on the updated map.
- **OpenCV image processing:** Demonstrates color-based detection and image output.
- **Simulation metrics:** Saves run summaries to CSV.
- **Automated tests:** Checks the path-planning functionality.

## Technology Stack

- Python
- Pygame
- NumPy
- OpenCV
- Ultralytics YOLO
- pytest
- Python standard library

## System Architecture

### Navigation simulation

```text
Grid configuration
       |
       v
Grid construction
       |
       v
A* path planner
       |
       v
Initial route
       |
       v
Pygame agent simulation
       |
       v
Temporary obstacle appears
       |
       v
A* replanning
       |
       v
Updated route and run metrics
```

### Vision-based navigation demonstration

```text
Input image
     |
     v
YOLO object detection
     |
     v
Selected object detections
     |
     v
Approximate image-to-grid mapping
     |
     v
Updated obstacle grid
     |
     v
A* route planning
     |
     v
Console results and visual navigation map
```

The vision-navigation script calculates a path from detections in an image. It is a separate demonstration and does not automatically feed live camera detections into the animated Pygame simulator.

## Project Structure

```text
AI-Autonomous-Navigation-System/
├── images/
│   └── test.jpg
├── outputs/
│   ├── navigation_demo.png
│   ├── vision_navigation.png
│   └── yolo_detection/
│       └── test.jpg
├── src/
│   ├── astar.py
│   ├── config.py
│   ├── grid.py
│   ├── metrics.py
│   ├── simulator.py
│   ├── detect_objects.py
│   ├── vision.py
│   └── vision_navigation.py
├── tests/
│   └── test_astar.py
├── requirements.txt
├── main.py
└── README.md
```

Generated output files may not all be tracked by Git. The actual files in your local checkout determine which outputs are available.

## Installation

### Requirements

- Python installed on your computer
- Internet access for installing dependencies and obtaining model weights when needed
- A desktop environment capable of opening a Pygame window

The project has been run successfully in a Windows virtual environment using Python 3.13.15. Compatibility may vary with other Python and dependency versions.

### Windows Command Prompt

Open a terminal in the project root.

Create a virtual environment if you do not already have one:

```bat
python -m venv .venv
```

Activate it:

```bat
.venv\Scripts\activate
```

Install dependencies:

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
```

If pytest is already listed in `requirements.txt`, the additional pytest installation is unnecessary.

## Running the Project

Run the commands below from the **project root directory**, with the virtual environment activated.

### 1. Start the animated navigation simulator

```bat
python -m src.simulator
```

The virtual agent follows an A\*-planned route. During the simulation, a temporary obstacle is introduced, and the planner attempts to calculate a new route.

**Controls**

| Key | Action |
|---|---|
| `SPACE` | Pause or resume |
| `R` | Restart the simulation |
| `S` | Save a screenshot |
| `ESC` | Quit |

The simulator saves its screenshot to `outputs/navigation_demo.png` when you press `S`. Run metrics are recorded in `outputs/run_metrics.csv` when a run finishes or is stopped.

### 2. Run YOLO object detection

```bat
python src\detect_objects.py
```

This script runs the pretrained YOLO model on the sample image and reports detected classes, confidence scores, and bounding boxes.

The annotated detection image is saved under:

```text
outputs/yolo_detection/test.jpg
```

The model weights may be downloaded automatically by Ultralytics when the model is first loaded. An internet connection may be required on the first run.

### 3. Run the vision-navigation demonstration

```bat
python src\vision_navigation.py
```

This script:

1. Loads the sample image.
2. Detects objects using YOLO.
3. Maps selected detections to approximate grid cells.
4. Adds eligible detected cells as simulated obstacles.
5. Runs A\* to find a path.
6. Prints detection and route information.

The resulting map is saved to:

```text
outputs/vision_navigation.png
```

This mapping is an illustrative approximation. It is not a calibrated conversion from image coordinates to physical positions.

### 4. Run the OpenCV vision demonstration

```bat
python src\vision.py
```

This script demonstrates image processing and color-based detection and generates a visual output under the `outputs` directory.

### 5. Run automated tests

```bat
python -m pytest -v
```

The path-planning tests check the implemented A\* behavior.

## Testing and Results

The project has completed **four automated tests successfully** in the development environment.

The Pygame simulator has also been launched successfully, and the temporary-obstacle replanning behavior has been observed during a manual run.

The YOLO detection script has detected objects in the sample image, and the vision-navigation script has produced a path using the approximate obstacle grid.

These results demonstrate the implemented software features. They do not establish real-world navigation accuracy, safety, or performance.

## Outputs

| File | Purpose |
|---|---|
| `outputs/navigation_demo.png` | Screenshot of the Pygame simulator |
| `outputs/vision_navigation.png` | Grid visualization of obstacles and the planned route |
| `outputs/yolo_detection/test.jpg` | Annotated object-detection image |
| `outputs/run_metrics.csv` | Simulation run summaries |

Output files are generated when the relevant scripts run. If a file is missing, run its corresponding script to regenerate it.

## Limitations

- The environment is a 2D grid rather than a physical world.
- The dynamic obstacle in the Pygame simulator is simulated, not detected by a live camera.
- The vision-navigation module uses a single image and approximate image-to-grid mapping.
- A single image does not provide reliable metric depth or full 3D object positions.
- The project does not currently implement live camera navigation, robot localization, motor control, or physical collision avoidance.
- The system has not been validated for use in real vehicles or safety-critical environments.

## Future Improvements

- Integrate a live camera feed into the simulation.
- Improve object-to-grid mapping using camera calibration and depth information.
- Connect vision detections directly to a continuously running navigation loop.
- Add randomized obstacle maps and more automated replanning tests.
- Compare A\* with other path-planning algorithms.
- Explore ROS 2 integration.
- Explore robotics simulators such as Gazebo or CARLA.
- Add more detailed performance measurements and evaluation scenarios.

## Learning Outcomes

- Grid representation and graph search
- A\* pathfinding and heuristic functions
- Dynamic obstacle replanning
- Object detection using a pretrained model
- Image processing with OpenCV
- Python modular design and testing
- Simulation visualization and CSV metrics
- Version control using Git and GitHub

## Author

**Vyshnavi Porandla**

GitHub repository: https://github.com/vyshnaviporandla/AI-Autonomous-Navigation-System

Branch: `feature/dynamic-replanning`
