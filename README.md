# Micro-Navigator: Potential Field Path Planning System

## Overview

Micro-Navigator is an autonomous path planning system designed for rectangular robots operating in grid-based environments. The system employs potential field theory to generate collision-free trajectories while accounting for robot geometry and obstacle avoidance constraints.

## Key Features

- **Potential Field Algorithm**: Implements attractive and repulsive potential fields for smooth path generation
- **Configurable Robot Dimensions**: Supports variable robot sizes with automatic obstacle inflation
- **Performance Analytics**: Comprehensive statistics tracking including path length, computation time, and success metrics
- **Visualization Tools**: Automated generation of path and map visualizations
- **Export Capabilities**: CSV output format compatible with robot control systems

## System Architecture

```
micronavigator/
├── config/          Configuration parameters and constants
├── map/             Grid map loading and scenario definitions
├── planner/         Core path planning algorithms and utilities
├── robot/           Robot geometry handling and path export
├── visualization/   Rendering and visualization components
└── evaluation/      Benchmarking and performance assessment tools
```

## Installation

### Environment Setup

Create and activate a new conda environment:

```bash
conda create -n micronavigator python=3.11
conda activate micronavigator
```

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Single Scenario Execution

Run path planning on the default map configuration:

```bash
conda activate micronavigator
python main.py
```

**Outputs:**
- `map_output.png` - Visualization of the occupancy grid
- `path_output.png` - Generated path overlay on the map
- `robot/path_output.csv` - Waypoint coordinates for robot execution

### Batch Evaluation

Execute comprehensive performance benchmarking across multiple scenarios:

```bash
conda activate micronavigator
python run_evaluation.py
```

The evaluation suite tests various configurations including:
- Multiple map topologies (simple, corridor, maze, cluttered, narrow, large)
- Different robot dimensions (1x1 to 5x5 grid cells)
- Performance metrics: path optimality, planning time, exploration efficiency

**Outputs:**
- `evaluation/results.json` - Detailed results in JSON format
- `evaluation/results.csv` - Tabular results for analysis
- `evaluation/*_path.png` - Individual scenario visualizations

## Configuration

Modify system parameters in [config/settings.py](config/settings.py):

### Robot Configuration
- `ROBOT_WIDTH` - Robot width in grid cells
- `ROBOT_HEIGHT` - Robot height in grid cells

### Potential Field Parameters
- `ATTRACTIVE_GAIN` - Goal attraction strength
- `REPULSIVE_GAIN` - Obstacle repulsion strength
- `OBSTACLE_INFLUENCE` - Range of obstacle repulsive field

### Visualization Settings
- Output file paths
- Display parameters

## Algorithm Details

The planner utilizes a two-stage approach:

1. **Potential Field Computation**: Combines attractive potential (guiding toward goal) and repulsive potential (avoiding obstacles) to create a navigation function over the configuration space

2. **Path Extraction**: Performs gradient descent on the potential field to extract a minimum-cost trajectory from start to goal

Obstacle inflation ensures safe navigation by expanding obstacles based on robot footprint dimensions.

## Performance Metrics

The system tracks the following key performance indicators:

- **Planning Time**: Computational duration for path generation
- **Nodes Explored**: Number of grid cells evaluated during planning
- **Path Length**: Total number of waypoints in the trajectory
- **Path Cost**: Cumulative cost metric based on step distances
- **Success Rate**: Percentage of scenarios reaching goal position

## Requirements

- Python 3.11+
- matplotlib >= 3.5.0

## License

This software is provided for educational and research purposes.

## Author

Developed as part of autonomous systems coursework.
