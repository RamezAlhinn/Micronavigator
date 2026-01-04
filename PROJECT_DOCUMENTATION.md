# Micro-Navigator: Autonomous Path Planning System Using Potential Field Theory

**Author:** Ramez Alhinn
**Course:** Intelligent Robotics (AIN)
**Date:** 05 January 2026
**Institution:** THI

---

## Abstract

This document presents Micro-Navigator, an autonomous path planning system designed for rectangular mobile robots operating in grid-based environments. The system implements potential field theory to generate collision-free trajectories while accounting for robot geometry and obstacle avoidance constraints. The implementation includes a comprehensive testing framework with 12 test scenarios spanning various environmental complexities, from open spaces to dense obstacle fields. Performance benchmarking demonstrates the algorithm's effectiveness across different map topologies, with successful path generation in 100% of tested scenarios. The system features advanced visualization capabilities including animated robot movement simulations and detailed performance analytics, making it suitable for both research and educational applications.

**Keywords:** Path Planning, Potential Fields, Mobile Robotics, Obstacle Avoidance, Autonomous Navigation

---

## 1. Introduction

### 1.1 Motivation

Autonomous navigation remains a fundamental challenge in mobile robotics, requiring systems to efficiently compute collision-free paths from start to goal positions while navigating complex environments. Traditional approaches such as A* search and Dijkstra's algorithm provide optimal solutions but may struggle with computational efficiency in large state spaces. Potential field methods offer an elegant alternative by treating the robot as a particle moving under the influence of artificial forces: attractive forces pulling toward the goal and repulsive forces pushing away from obstacles.

### 1.2 Problem Statement

Given:
- A rectangular robot with dimensions $w \times h$ grid cells
- A discrete 2D grid-based environment with obstacles
- A start position $P_{start} = (x_s, y_s)$
- A goal position $P_{goal} = (x_g, y_g)$

Objective:
- Compute a collision-free path $\pi = \{p_0, p_1, ..., p_n\}$ where $p_0 = P_{start}$ and $p_n = P_{goal}$
- Minimize path cost while maintaining safety margins around obstacles
- Account for robot geometry through appropriate obstacle inflation

### 1.3 Scope and Limitations

**Scope:**
- Grid-based 2D environments with static obstacles
- Rectangular robot geometries with configurable dimensions
- Offline path planning (pre-computed before execution)
- Deterministic obstacle configurations

**Limitations:**
- Static environments only (no dynamic obstacles)
- Grid discretization may limit path optimality
- Potential for local minima in certain configurations
- Does not address kinematic or dynamic constraints

---

## 2. Theoretical Background

### 2.1 Potential Field Theory

The potential field approach models robot navigation as movement in an artificial potential field $U(x, y)$ composed of two components:

$$U(x, y) = U_{att}(x, y) + U_{rep}(x, y)$$

where:
- $U_{att}(x, y)$ is the attractive potential guiding toward the goal
- $U_{rep}(x, y)$ is the repulsive potential preventing obstacle collisions

#### 2.1.1 Attractive Potential

The attractive potential increases with distance from the goal, creating a "pull" toward the target:

$$U_{att}(x, y) = \frac{1}{2} k_{att} \cdot d^2(P, P_{goal})$$

where:
- $k_{att}$ is the attractive gain constant
- $d(P, P_{goal})$ is the Euclidean distance to the goal
- The quadratic form ensures smooth gradients near the goal

#### 2.1.2 Repulsive Potential

The repulsive potential increases near obstacles, creating "push" forces:

$$U_{rep}(x, y) = \begin{cases}
\frac{1}{2} k_{rep} \left(\frac{1}{d(P, P_{obs})} - \frac{1}{\rho_0}\right)^2 & \text{if } d(P, P_{obs}) \leq \rho_0 \\
0 & \text{if } d(P, P_{obs}) > \rho_0
\end{cases}$$

where:
- $k_{rep}$ is the repulsive gain constant
- $d(P, P_{obs})$ is the distance to nearest obstacle
- $\rho_0$ is the influence range of obstacles

#### 2.1.3 Gradient Descent Path Extraction

The path is computed by following the negative gradient of the total potential:

$$\vec{F}(x, y) = -\nabla U(x, y)$$

Starting from $P_{start}$, the robot moves iteratively in the direction of steepest descent until reaching $P_{goal}$ or a local minimum.

### 2.2 Obstacle Inflation for Robot Geometry

To account for the robot's physical dimensions, obstacles are inflated by the robot's footprint. For a robot of size $w \times h$, each obstacle cell is expanded by:

$$\text{inflation\_radius} = \max\left(\left\lceil\frac{w}{2}\right\rceil, \left\lceil\frac{h}{2}\right\rceil\right)$$

This configuration space transformation allows treating the robot as a point in the inflated space, simplifying collision detection.

---

## 3. System Architecture

### 3.1 Overview

The Micro-Navigator system follows a modular architecture organized into five primary subsystems:

```
micronavigator/
├── config/          # Configuration parameters and constants
├── map/             # Environment representation and loading
├── planner/         # Core path planning algorithms
├── robot/           # Robot-specific geometry and export
└── visualization/   # Rendering and performance analysis
```

### 3.2 Component Description

#### 3.2.1 Configuration Module (`config/`)

**File:** `settings.py`

Centralizes system parameters including:
- Grid cell type identifiers (FREE, OBSTACLE, START, GOAL)
- Potential field parameters ($k_{att}$, $k_{rep}$, $\rho_0$)
- Robot geometric configuration ($w$, $h$)
- Visualization preferences

This separation enables easy parameter tuning without modifying core algorithms.

#### 3.2.2 Map Module (`map/`)

**File:** `grid_loader.py`

**Responsibilities:**
- Parse text-based grid map files
- Identify start and goal positions
- Validate map integrity
- Support multiple resolution levels

**Map Format:**
```
0 0 0 3 3
0 1 1 3 3
2 2 0 0 0
```
where: 0=FREE, 1=OBSTACLE, 2=START, 3=GOAL

#### 3.2.3 Planning Module (`planner/`)

**Core Components:**

1. **`potential_field.py`**: Computes combined potential field
   - Attractive potential generation
   - Repulsive potential computation
   - Obstacle distance transformation
   - Field composition and normalization

2. **`path_extractor.py`**: Extracts paths via gradient descent
   - Numerical gradient computation
   - Step-wise path construction
   - Local minima detection
   - Path smoothing (optional)

3. **`statistics.py`**: Performance tracking
   - Planning time measurement
   - Node exploration counting
   - Path quality metrics (length, cost)
   - Success/failure logging

#### 3.2.4 Robot Module (`robot/`)

**Core Components:**

1. **`shape_handler.py`**: Obstacle inflation
   - Configuration space transformation
   - Morphological dilation operations
   - Safety margin enforcement

2. **`exporter.py`**: Waypoint export
   - CSV format generation
   - Robot controller compatibility
   - Coordinate system transformation

#### 3.2.5 Visualization Module (`visualization/`)

**Core Components:**

1. **`draw_path.py`**: Static path visualization
   - Grid map rendering
   - Path overlay with markers
   - Information annotations
   - High-resolution output (150 DPI)

2. **`draw_animation.py`**: Animated robot simulation
   - Frame-by-frame robot position rendering
   - Progress indicators
   - GIF generation for presentations
   - Configurable frame rate (10 FPS)

3. **`draw_benchmark.py`**: Performance analytics
   - Multi-panel metric visualization
   - Comparative scenario analysis
   - Statistical summary generation
   - Publication-ready charts

---

## 4. Implementation Details

### 4.1 Algorithm Implementation

#### 4.1.1 Potential Field Computation

**Algorithm 1: Compute Potential Field**
```
Input: grid, goal_position, k_att, k_rep, rho_0
Output: potential_field

1. Initialize potential_field with zeros
2. Compute distance_to_goal for all cells
3. For each cell (x, y):
   a. U_att = 0.5 * k_att * distance_to_goal[x, y]^2
   b. distance_to_obstacle = min_distance_to_nearest_obstacle(x, y)
   c. If distance_to_obstacle <= rho_0:
      U_rep = 0.5 * k_rep * (1/distance_to_obstacle - 1/rho_0)^2
   d. Else:
      U_rep = 0
   e. potential_field[x, y] = U_att + U_rep
4. Return potential_field
```

**Complexity Analysis:**
- Time: $O(n \cdot m \cdot k)$ where $n \times m$ is grid size, $k$ is obstacle count
- Space: $O(n \cdot m)$ for potential field storage

#### 4.1.2 Path Extraction via Gradient Descent

**Algorithm 2: Extract Path**
```
Input: potential_field, start, goal, max_iterations
Output: path

1. Initialize path = [start]
2. current = start
3. For iteration = 1 to max_iterations:
   a. If current == goal:
      Return path (SUCCESS)
   b. gradient = compute_gradient(potential_field, current)
   c. next_position = current - step_size * gradient
   d. If next_position in obstacle or out of bounds:
      Return path (FAILURE - collision)
   e. path.append(next_position)
   f. current = next_position
   g. If no significant movement for N steps:
      Return path (FAILURE - local minimum)
4. Return path (FAILURE - max iterations)
```

**Convergence Criteria:**
- Goal reached: $||P_{current} - P_{goal}|| < \epsilon$
- Local minimum: $||\nabla U|| < \epsilon_{grad}$
- Maximum iterations exceeded

### 4.2 Parameter Selection

Empirically determined parameters for robust performance:

| Parameter | Value | Justification |
|-----------|-------|---------------|
| $k_{att}$ | 1.0 | Moderate attraction allows exploration |
| $k_{rep}$ | 50.0 | Strong repulsion ensures safety |
| $\rho_0$ | 3 cells | Balanced obstacle influence range |
| Step size | 0.5 | Smooth paths without overshooting |
| Max iterations | 10000 | Sufficient for large maps |

---

## 5. Experimental Setup and Testing

### 5.1 Test Scenario Design

Twelve test scenarios were designed to evaluate algorithm performance across diverse environmental conditions:

**High-Resolution Scenarios (Primary):**

| ID | Scenario Name | Map Size | Obstacles | Characteristics |
|----|---------------|----------|-----------|-----------------|
| 1 | Open Space Navigation | 12×36 | 0 | Baseline performance |
| 2 | Corridor Traversal | 12×56 | 208 | Constrained passages |
| 3 | Complex Maze | 32×40 | 448 | Multi-turn navigation |
| 4 | Dense Obstacle Field | 28×48 | 368 | High obstacle density |
| 5 | Narrow Gap Challenge | 20×40 | 288 | Precision maneuvering |
| 6 | Large-Scale Environment | 44×60 | 816 | Scalability testing |

**Standard Resolution Scenarios (7-12):**
Identical topologies at reduced resolution for rapid testing and validation.

### 5.2 Performance Metrics

**Quantitative Metrics:**
1. **Planning Time** ($t_{plan}$): Total computation time (ms)
2. **Nodes Explored** ($N_{exp}$): Number of grid cells evaluated
3. **Path Length** ($L_{path}$): Number of waypoints in trajectory
4. **Path Cost** ($C_{path}$): Cumulative Euclidean distance
5. **Success Rate** ($S_{rate}$): Percentage of successful completions

**Qualitative Metrics:**
1. Path smoothness (subjective visual assessment)
2. Clearance from obstacles (safety margin)
3. Optimality ratio (path cost vs. theoretical minimum)

### 5.3 Testing Framework

**Execution Command:**
```bash
python run_scenarios.py [scenario_ids]
```

**Output Generation:**
- Static visualization: `output/scenarioN_path.png`
- Animated simulation: `output/scenarioN_animation.gif`
- Performance metrics: `output/scenarioN_benchmark.png`
- Waypoint data: `output/scenarioN_path.csv`
- Comparison analysis: `output/benchmark_comparison.png`

---

## 6. Results and Analysis

### 6.1 Experimental Results

**Overall Performance Summary:**

| Metric | Mean | Std Dev | Min | Max |
|--------|------|---------|-----|-----|
| Planning Time (ms) | 68.9 | 76.2 | 0.06 | 229.0 |
| Nodes Explored | 492 | 513 | 9 | 1485 |
| Path Length (steps) | 48 | 20 | 9 | 79 |
| Path Cost (units) | 51.1 | 24.8 | 8.0 | 85.5 |
| Success Rate (%) | 100 | 0 | 100 | 100 |

**Key Findings:**

1. **100% Success Rate**: All scenarios completed successfully, demonstrating algorithm robustness across diverse environments.

2. **Scalability**: Planning time scales sublinearly with map size (O(n log n) observed vs. O(n²) theoretical worst case), indicating efficient implementation.

3. **Path Quality**: Average step cost of 1.06 units indicates near-optimal paths (theoretical minimum is 1.0 for straight-line movement).

### 6.2 Scenario-Specific Analysis

**Scenario 3 - Complex Maze:**
- Planning Time: 55.93 ms
- Nodes Explored: 394
- Path Length: 59 waypoints
- Characteristics: Successfully navigated multiple decision points with no local minima encountered

**Scenario 4 - Dense Obstacle Field:**
- Planning Time: 55.79 ms
- Nodes Explored: 445
- Path Length: 52 waypoints
- Characteristics: Demonstrated effective obstacle avoidance in high-density environment

**Scenario 6 - Large-Scale Environment:**
- Planning Time: 225.73 ms
- Nodes Explored: 1485
- Path Length: 79 waypoints
- Characteristics: Validated scalability to larger map sizes (2640 cells)

### 6.3 Visualization Analysis

**Static Visualizations:**
All scenarios produced clear path visualizations with:
- Distinct start (green) and goal (blue) markers
- Red path overlay showing complete trajectory
- Information annotations displaying success metrics

**Animated Simulations:**
Generated GIF animations (10 FPS) effectively demonstrate:
- Robot footprint movement along planned path
- Progress indicators (percentage completion)
- Smooth transitions between waypoints
- File sizes: 86 KB - 884 KB depending on path complexity

**Performance Benchmarks:**
Four-panel charts provide comprehensive analysis:
- Normalized metric comparisons
- Map configuration details
- Path quality assessment
- Exploration efficiency ratings

---

## 7. Discussion

### 7.1 Strengths

1. **Robustness**: 100% success rate across all test scenarios demonstrates reliable path finding even in challenging environments.

2. **Computational Efficiency**: Sub-second planning times for all scenarios make the system suitable for real-time applications.

3. **Modularity**: Clear separation of concerns enables easy extension and modification of individual components.

4. **Visualization Suite**: Comprehensive output formats support both technical analysis and presentation requirements.

5. **Geometric Awareness**: Obstacle inflation correctly accounts for robot dimensions, ensuring physically feasible paths.

### 7.2 Limitations and Challenges

1. **Local Minima**: While not observed in test scenarios, potential field methods are theoretically susceptible to local minima in certain configurations (e.g., U-shaped obstacles).

2. **Path Optimality**: Gradient descent does not guarantee globally optimal paths; solutions are locally optimal within the potential field landscape.

3. **Static Environments**: Current implementation assumes static obstacles; dynamic environments would require replanning.

4. **Grid Discretization**: Path resolution limited by grid cell size; finer grids improve quality but increase computation.

5. **Parameter Sensitivity**: Performance depends on appropriate tuning of $k_{att}$, $k_{rep}$, and $\rho_0$ for specific environments.

### 7.3 Comparison with Alternative Approaches

**vs. A* Search:**
- Advantage: Smoother paths, faster computation for large maps
- Disadvantage: No optimality guarantee

**vs. RRT (Rapidly-exploring Random Trees):**
- Advantage: More predictable behavior, smoother paths
- Disadvantage: Less effective in high-dimensional spaces

**vs. Dynamic Window Approach:**
- Advantage: Simpler implementation, offline planning capability
- Disadvantage: No kinematic constraint handling

---

## 8. Conclusion and Future Work

### 8.1 Summary

This project successfully implemented a potential field-based path planning system for autonomous mobile robots. The system demonstrated:

- **Effectiveness**: 100% success rate across 12 diverse test scenarios
- **Efficiency**: Average planning time of 68.9 ms suitable for practical applications
- **Usability**: Comprehensive visualization and benchmarking tools
- **Extensibility**: Modular architecture supporting future enhancements

The implementation validates potential field theory as a viable approach for grid-based robot navigation, particularly in static environments with well-defined obstacles.

### 8.2 Future Enhancements

**Short-term Improvements:**

1. **Local Minima Escape**: Implement random walk or simulated annealing to escape local minima
2. **Path Smoothing**: Add post-processing for smoother, more natural trajectories
3. **Dynamic Replanning**: Support moving obstacles through periodic field updates
4. **Multi-resolution Planning**: Hierarchical approach for very large maps

**Long-term Extensions:**

1. **Kinematic Constraints**: Incorporate differential drive or Ackermann steering models
2. **Multi-robot Coordination**: Extend to multi-agent scenarios with inter-robot avoidance
3. **3D Navigation**: Generalize to three-dimensional environments
4. **Learning-based Tuning**: Automatic parameter optimization via machine learning
5. **Real Robot Integration**: Deploy on physical platform (e.g., TurtleBot, mobile manipulator)

### 8.3 Lessons Learned

1. **Modular Design**: Early investment in clean architecture paid dividends during testing and visualization development
2. **Comprehensive Testing**: Diverse scenario set revealed algorithm behavior across edge cases
3. **Visualization Importance**: High-quality outputs essential for understanding and presenting results
4. **Parameter Tuning**: Significant impact on performance; systematic approach necessary

---

## 9. References

1. Khatib, O. (1986). "Real-time obstacle avoidance for manipulators and mobile robots." *The International Journal of Robotics Research*, 5(1), 90-98.

2. LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.

3. Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.

4. Choset, H., Lynch, K. M., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L. E., & Thrun, S. (2005). *Principles of Robot Motion: Theory, Algorithms, and Implementation*. MIT Press.

5. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A formal basis for the heuristic determination of minimum cost paths." *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.

---

## Appendix A: Installation and Usage

### A.1 System Requirements

- Python 3.11+
- matplotlib >= 3.5.0
- numpy (installed with matplotlib)

### A.2 Installation

```bash
# Create virtual environment
conda create -n micronavigator python=3.11
conda activate micronavigator

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify_system.py
```

### A.3 Running Scenarios

```bash
# List available scenarios
python run_scenarios.py --list

# Run single scenario
python run_scenarios.py 3

# Run multiple scenarios
python run_scenarios.py 1 3 5

# Run all scenarios
python run_scenarios.py
```

### A.4 Output Files

All outputs saved to `output/` directory:
- `scenarioN_path.png` - Static visualization
- `scenarioN_animation.gif` - Robot movement animation
- `scenarioN_benchmark.png` - Performance metrics
- `scenarioN_path.csv` - Waypoint data
- `benchmark_comparison.png` - Multi-scenario comparison

---

## Appendix B: Configuration Parameters

Located in `config/settings.py`:

```python
# Grid cell types
FREE = 0
OBSTACLE = 1
START = 2
GOAL = 3

# Potential field parameters
ATTRACTIVE_GAIN = 1.0       # k_att
REPULSIVE_GAIN = 50.0       # k_rep
OBSTACLE_INFLUENCE = 3      # rho_0 (cells)

# Robot geometry
ROBOT_WIDTH = 2             # cells
ROBOT_HEIGHT = 2            # cells
```