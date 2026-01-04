# Micro-Navigator: Potential Field Path Planning System

## Overview

Micro-Navigator is an autonomous path planning system designed for rectangular robots operating in grid-based environments. The system employs potential field theory to generate collision-free trajectories while accounting for robot geometry and obstacle avoidance constraints.

## Key Features

- **Potential Field Algorithm**: Implements attractive and repulsive potential fields for smooth path generation
- **Configurable Robot Dimensions**: Supports variable robot sizes with automatic obstacle inflation
- **Performance Analytics**: Comprehensive statistics tracking including path length, computation time, and success metrics
- **Advanced Visualization**:
  - Static path visualizations with detailed scenario information
  - Animated GIF showing robot movement along the planned path
  - Performance benchmark charts with detailed metrics analysis
  - Comparison charts for multiple scenarios
- **Flexible Scenario Runner**: Run individual scenarios or multiple scenarios with a single command
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

**Quick Start:** See [QUICKSTART.md](QUICKSTART.md) for a quick reference guide.

### Run Individual or Multiple Scenarios

The scenario runner allows flexible execution of test scenarios:

```bash
# List all available scenarios
python run_scenarios.py --list

# Run all scenarios
python run_scenarios.py

# Run a specific scenario (e.g., scenario 1)
python run_scenarios.py 1

# Run multiple specific scenarios (e.g., 1, 3, and 5)
python run_scenarios.py 1 3 5
```

**Available Scenarios:**

High-Resolution (Best for Demonstrations):
1. Open Space Navigation - Obstacle-free pathfinding
2. Corridor Traversal - Constrained passage navigation
3. Complex Maze - Multi-turn maze solving
4. Dense Obstacle Field - High-density obstacle avoidance
5. Narrow Gap Challenge - Precision maneuvering
6. Large-Scale Environment - Extended range planning

Standard Resolution (Fast Testing):
7-12. Same scenarios in standard resolution for rapid iteration

**Outputs:**
- `output/scenarioN_path.png` - Static visualization with scenario info, path, and markers
- `output/scenarioN_animation.gif` - Animated GIF showing robot movement along the path
- `output/scenarioN_benchmark.png` - Performance metrics and analysis chart
- `output/scenarioN_path.csv` - Waypoint coordinates for robot execution
- `output/benchmark_comparison.png` - Comparison chart (when running multiple scenarios)
- Terminal output with detailed statistics and summary

### System Verification

Verify all modules and scenarios are properly configured:

```bash
python verify_system.py
```

This checks:
- Required Python packages (matplotlib, numpy)
- Project file structure
- All 12 scenario map files
- Scenario runner configuration

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
