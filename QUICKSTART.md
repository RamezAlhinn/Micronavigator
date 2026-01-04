# Quick Start Guide

## Getting Animations and Visualizations

**Important:** Use `python run_scenarios.py` (NOT `main.py`) to get animations and benchmarks!

Every scenario run automatically creates:
- Static visualization (PNG)
- **Animated robot movement (GIF)** ✨
- Performance benchmark chart (PNG)
- Waypoint data (CSV)

All files are saved in the `output/` directory.

## Running Scenarios

### List Available Scenarios
```bash
python run_scenarios.py --list
```

### Run All Scenarios
```bash
python run_scenarios.py
```

### Run a Single Scenario
```bash
python run_scenarios.py 1    # Run scenario 1
python run_scenarios.py 3    # Run scenario 3
```

### Run Multiple Scenarios
```bash
python run_scenarios.py 1 3 5    # Run scenarios 1, 3, and 5
python run_scenarios.py 1 2 3 4 5 6    # Run scenarios 1 through 6
```

## Available Scenarios

**High-Resolution Scenarios (Best for Demonstrations):**

| # | Name | Description |
|---|------|-------------|
| 1 | Open Space Navigation | Obstacle-free pathfinding |
| 2 | Corridor Traversal | Constrained passage navigation |
| 3 | Complex Maze | Multi-turn maze solving |
| 4 | Dense Obstacle Field | High-density obstacle avoidance |
| 5 | Narrow Gap Challenge | Precision maneuvering |
| 6 | Large-Scale Environment | Extended range planning |

**Standard Resolution Scenarios (Fast Testing):**

| # | Name | Description |
|---|------|-------------|
| 7 | Open Space (Fast) | Quick baseline test |
| 8 | Corridor (Fast) | Rapid corridor test |
| 9 | Maze (Fast) | Quick maze validation |
| 10 | Obstacles (Fast) | Fast obstacle testing |
| 11 | Narrow Gap (Fast) | Quick precision test |
| 12 | Large Map (Fast) | Rapid scalability test |

## Output Files

After running scenarios, check the `output/` directory:
- `output/scenarioN_path.png` - Static visualization with scenario info
- `output/scenarioN_animation.gif` - **Animated robot movement** (open with any GIF viewer)
- `output/scenarioN_benchmark.png` - Performance metrics chart for the scenario
- `output/scenarioN_path.csv` - Robot waypoint data (CSV format)
- `output/benchmark_comparison.png` - Comparison chart (when running multiple scenarios)

### Viewing Your Animations

```bash
# List all animations
ls -lh output/*.gif

# Open an animation (macOS)
open output/scenario3_animation.gif

# Open output folder to view all files
open output/
```

## Demonstration Workflow

### For Presentations/Demos
```bash
# Best visual scenarios (recommended order)
python run_scenarios.py 3    # Complex Maze - shows intelligent pathfinding
python run_scenarios.py 4    # Dense Obstacles - impressive maneuvering
python run_scenarios.py 6    # Large-Scale - shows scalability

# View the animations
open output/scenario3_animation.gif
open output/scenario4_animation.gif
open output/scenario6_animation.gif
```

### For Quick Testing
```bash
# 1. Verify system works
python verify_system.py

# 2. Quick baseline test
python run_scenarios.py 7

# 3. Fast validation of all types
python run_scenarios.py 7 8 9

# 4. Check results
ls -lh output/
```

### For Complete Analysis
```bash
# Run all high-res scenarios for comparison
python run_scenarios.py 1 2 3 4 5 6

# View the comparison chart
open output/benchmark_comparison.png
```

## Visualization Features

### Static Path Visualization
Each path visualization includes:
- Path drawn in red from start to goal
- Green circle marking the start position
- Blue star marking the goal position
- Scenario name and description in the title
- Information box showing:
  - Scenario type/description
  - Path length (number of waypoints)
  - Success/failure status
- Legend identifying path, start, and goal markers

### Animated Robot Movement
Each successful scenario generates an animated GIF showing:
- Robot (red rectangle) moving along the planned path
- Progress indicator showing completion percentage
- Planned path shown as blue dashed line
- Start and goal markers for reference

### Benchmark Charts
Individual scenario benchmarks show:
- Key performance metrics comparison
- Map and robot configuration details
- Path quality metrics (length, cost, efficiency)
- Exploration efficiency analysis

Comparison benchmarks (multiple scenarios) show:
- Path length comparison across scenarios
- Planning time comparison
- Nodes explored comparison
- Overall success rate pie chart
- Summary statistics

## Tips

### For Demonstrations
- **Best scenarios**: 3 (Complex Maze), 4 (Dense Obstacles), 6 (Large-Scale)
- Use high-res scenarios (1-6) for impressive visualizations
- Animations make excellent presentation materials

### For Testing
- Start with scenario 1 to verify system works
- Use fast scenarios (7-12) for rapid iteration
- Run multiple scenarios to generate comparison charts

### General
- High-res scenarios: Better quality, slower execution
- Standard scenarios: Lower quality, faster execution
- All visualizations are publication-ready (150 DPI)
- Output files numbered by scenario for easy tracking
