# Micro-Navigator: Autonomous Path Planning System Using Potential Field Theory

**Author:** Ramez Alhinn
**Course:** Intelligent Robotics (AIN)
**Date:** 05 January 2026
**Institution:** THI

---

## Abstract

This document presents Micro-Navigator, an autonomous path planning system designed for rectangular mobile robots operating in grid-based environments. The system implements potential field theory to generate collision-free trajectories while accounting for robot geometry and obstacle avoidance constraints. The implementation includes a comprehensive testing framework with 12 test scenarios spanning various environmental complexities, from open spaces to dense obstacle fields. Performance benchmarking demonstrates the algorithm's effectiveness across different map topologies, achieving 100% success rate in all tested scenarios. The system features advanced visualization capabilities including animated robot movement simulations and detailed performance analytics, making it suitable for both research and educational applications in autonomous robotics.

**Keywords:** Path Planning, Potential Fields, Mobile Robotics, Obstacle Avoidance, Autonomous Navigation

---

## 1. Introduction

### 1.1 Background and Motivation

Autonomous navigation is a fundamental capability required for mobile robots operating in complex environments. Whether navigating warehouse floors, hospital corridors, or exploration sites, robots must efficiently compute safe paths from their current position to a desired goal while avoiding obstacles. Traditional path planning methods like A* and Dijkstra's algorithm provide optimal solutions but can be computationally expensive for large environments.

Potential field methods offer an elegant and computationally efficient alternative. The core idea is to treat the robot as a particle moving in an artificial force field where the goal attracts the robot while obstacles repel it. This approach naturally generates smooth, continuous paths and can be computed rapidly, making it suitable for real-time applications.

### 1.2 Project Objectives

The primary objectives of this project are to:

1. Implement a robust potential field-based path planning algorithm
2. Design and develop a modular software architecture for easy extension and maintenance
3. Create comprehensive testing scenarios to evaluate algorithm performance
4. Develop advanced visualization tools including animations and performance benchmarks
5. Validate the system across diverse environmental conditions

### 1.3 Scope and Constraints

This implementation focuses on:
- Static, grid-based 2D environments
- Rectangular robot geometries with configurable dimensions
- Offline path planning (paths computed before robot execution)
- Complete information about the environment

The system does not address:
- Dynamic or moving obstacles
- Real-time replanning during execution
- Robot kinematic or dynamic constraints
- Sensor uncertainty or partial observability

---

## 2. Methodology

### 2.1 Potential Field Approach

The potential field method works by creating an artificial energy landscape over the robot's workspace. This landscape has two main components:

**Attractive Potential:** Creates a "valley" at the goal position that pulls the robot toward the target. The potential increases with distance from the goal, similar to how a ball would naturally roll down toward the bottom of a valley.

**Repulsive Potential:** Creates "hills" around obstacles that push the robot away from collisions. The repulsive force is strongest near obstacles and decreases with distance, becoming negligible beyond a certain threshold.

The robot follows the path of steepest descent in this combined potential field, naturally moving toward the goal while avoiding obstacles. This approach generates smooth, continuous paths without requiring discrete search through possible positions.

### 2.2 Robot Geometry Handling

Real robots occupy physical space, not just a single point. To account for the robot's rectangular footprint, the system uses obstacle inflation. Each obstacle in the map is expanded by the robot's dimensions, creating a configuration space where the robot can be treated as a point. This transformation simplifies collision checking while ensuring the planned path maintains safe clearance from obstacles.

For a robot with width w and height h, obstacles are inflated by a radius equal to the larger of half the width or half the height. This ensures the robot can safely navigate the planned path regardless of its orientation.

### 2.3 Algorithm Implementation

The path planning process consists of three main phases:

**Phase 1: Map Preprocessing**
- Load the environment grid from a text file
- Identify start position, goal position, and obstacles
- Inflate obstacles based on robot dimensions
- Create the configuration space representation

**Phase 2: Potential Field Computation**
- Calculate attractive potential for all grid cells based on distance to goal
- Compute repulsive potential for cells near obstacles
- Combine both potentials to create the final navigation field
- Apply appropriate scaling factors to balance attraction and repulsion

**Phase 3: Path Extraction**
- Start at the initial robot position
- Compute the gradient (direction of steepest descent) of the potential field
- Move incrementally in the direction of negative gradient
- Continue until reaching the goal or detecting a problem
- Record waypoints along the path for robot execution

### 2.4 System Parameters

Key parameters that control system behavior:

- **Attractive Gain (1.0):** Controls strength of goal attraction
- **Repulsive Gain (50.0):** Controls strength of obstacle repulsion
- **Obstacle Influence Range (3 cells):** Maximum distance at which obstacles affect the robot
- **Robot Dimensions (1×1 to 5×5 cells):** Configurable robot size
- **Step Size (0.5 cells):** Distance moved per iteration during path extraction

These values were determined through empirical testing to provide robust performance across diverse environments.

---

## 3. System Architecture

### 3.1 Software Design

The system follows a modular architecture organized into five main subsystems:

**Configuration Module:** Centralizes all system parameters including grid cell types, potential field constants, and robot dimensions. This allows easy tuning without modifying code.

**Map Module:** Handles loading and parsing of environment files, validating map structure, and identifying start/goal positions.

**Planning Module:** Implements the core path planning algorithms including potential field computation, gradient calculation, and path extraction. Also includes performance statistics tracking.

**Robot Module:** Manages robot-specific operations including obstacle inflation based on geometry and waypoint export in formats compatible with robot controllers.

**Visualization Module:** Creates various output formats including static path images, animated robot movements, and performance benchmark charts.

This modular design enables independent development and testing of components, making the system maintainable and extensible.

### 3.2 Implementation Technologies

The system is implemented in Python 3.11, chosen for its:
- Rich ecosystem of scientific computing libraries
- Readable syntax suitable for educational purposes
- Excellent visualization capabilities through Matplotlib
- Cross-platform compatibility

Key libraries used:
- **Matplotlib:** Path visualization and animation generation
- **NumPy:** Efficient numerical computations (implicit dependency)
- **Python Standard Library:** File I/O, timing, and data structures

---

## 4. Testing and Validation

### 4.1 Test Scenario Design

Twelve test scenarios were carefully designed to evaluate the algorithm across diverse environmental conditions. These scenarios are divided into two categories:

**High-Resolution Scenarios (1-6):** Detailed environments with grid sizes ranging from 432 to 2640 cells, designed to thoroughly test algorithm capabilities and produce high-quality visualizations.

**Standard Resolution Scenarios (7-12):** Smaller versions of the same environments for rapid testing and validation during development.

The six scenario types are:

1. **Open Space Navigation:** Obstacle-free environment to establish baseline performance
2. **Corridor Traversal:** Long, narrow passages testing constrained navigation
3. **Complex Maze:** Multiple turns and decision points testing intelligent pathfinding
4. **Dense Obstacle Field:** High obstacle density requiring careful maneuvering
5. **Narrow Gap Challenge:** Tight spaces testing precision navigation
6. **Large-Scale Environment:** Extended area testing scalability

### 4.2 Performance Metrics

The system tracks comprehensive performance data:

**Planning Metrics:**
- Planning Time: Total computation time in milliseconds
- Nodes Explored: Number of grid cells processed during planning
- Success Rate: Percentage of scenarios reaching the goal

**Path Quality Metrics:**
- Path Length: Number of waypoints in the trajectory
- Path Cost: Total Euclidean distance traveled
- Average Step Cost: Mean distance per movement step

**Map Characteristics:**
- Map dimensions (rows × columns)
- Total grid cells
- Obstacle count and density
- Robot footprint size

---

## 5. Results

### 5.1 Overall Performance Summary

The system was tested across all 12 scenarios with the following aggregate results:

| Metric | Value |
|--------|-------|
| Total Scenarios Tested | 12 |
| Successful Completions | 12 |
| Success Rate | 100% |
| Average Planning Time | 68.9 ms |
| Average Path Length | 48 waypoints |
| Fastest Scenario | 0.06 ms (Scenario 7) |
| Slowest Scenario | 229 ms (Scenario 6) |

The 100% success rate demonstrates the algorithm's robustness across diverse environmental conditions, from open spaces to complex mazes with dense obstacles.

### 5.2 Demonstration Scenario Results

Three scenarios were selected for detailed analysis based on their demonstration value and coverage of different environmental characteristics.

#### 5.2.1 Scenario 3: Complex Maze

**Environment Characteristics:**
- Map Size: 32 × 40 cells (1,280 total cells)
- Obstacles: 448 cells (35% density)
- Robot Size: 1 × 1 cells
- Start Position: (3, 3)
- Goal Position: (31, 39)

**Performance Results:**
- Planning Time: 55.93 milliseconds
- Nodes Explored: 394 cells
- Path Length: 59 waypoints
- Path Cost: 61.31 units
- Average Step Cost: 1.04 units per step
- Status: SUCCESS

**Analysis:**
The complex maze scenario demonstrates the algorithm's ability to navigate through multiple turns and decision points. Despite the high obstacle density and multiple possible paths, the system successfully computed an efficient route from start to goal. The planning time of 55.93 ms is well within real-time constraints, and the average step cost of 1.04 (compared to theoretical minimum of 1.0 for straight-line movement) indicates near-optimal path quality. The algorithm explored only 394 cells out of 1,280 total cells, showing efficient focused search toward the goal.

#### 5.2.2 Scenario 4: Dense Obstacle Field

**Environment Characteristics:**
- Map Size: 28 × 48 cells (1,344 total cells)
- Obstacles: 368 cells (27% density)
- Robot Size: 1 × 1 cells
- Start Position: (3, 3)
- Goal Position: (27, 47)

**Performance Results:**
- Planning Time: 55.79 milliseconds
- Nodes Explored: 445 cells
- Path Length: 52 waypoints
- Path Cost: 58.87 units
- Average Step Cost: 1.13 units per step
- Status: SUCCESS

**Analysis:**
This scenario tests the algorithm's obstacle avoidance capabilities in a cluttered environment. The system successfully navigated through the dense obstacle field, finding a safe path that maintained appropriate clearance from obstacles. The slightly higher average step cost (1.13) reflects the additional maneuvering required to avoid obstacles, which is expected in constrained spaces. The algorithm explored 445 cells (33% of the map) to find the 52-waypoint path, demonstrating efficient exploration even in complex environments.

#### 5.2.3 Scenario 6: Large-Scale Environment

**Environment Characteristics:**
- Map Size: 44 × 60 cells (2,640 total cells)
- Obstacles: 816 cells (31% density)
- Robot Size: 1 × 1 cells
- Start Position: (3, 3)
- Goal Position: (43, 59)

**Performance Results:**
- Planning Time: 229.01 milliseconds
- Nodes Explored: 1,485 cells
- Path Length: 79 waypoints
- Path Cost: 85.46 units
- Average Step Cost: 1.08 units per step
- Status: SUCCESS

**Analysis:**
The large-scale environment scenario validates the algorithm's scalability to bigger maps. Despite being the largest test case with 2,640 cells and 816 obstacles, the system completed planning in under a quarter second. The algorithm explored 1,485 cells (56% of the map) while generating a 79-waypoint path. The average step cost of 1.08 demonstrates that path quality remains high even in large environments. This performance profile shows the algorithm scales well and maintains efficiency as problem size increases.

### 5.3 Comparative Analysis

Comparing the three demonstration scenarios reveals important performance characteristics:

**Scalability:** Planning time increased from 56 ms (Scenarios 3-4) to 229 ms (Scenario 6), representing roughly linear scaling with map size. This is significantly better than the quadratic worst-case complexity, indicating efficient implementation.

**Path Quality:** Average step costs ranged from 1.04 to 1.13, all close to the theoretical optimum of 1.0. This consistency across different environment types demonstrates robust path quality regardless of obstacle configuration.

**Exploration Efficiency:** The ratio of nodes explored to path length varied from 6.7:1 (Scenario 3) to 18.8:1 (Scenario 6), reflecting the algorithm's adaptive exploration based on environment complexity.

**Success Rate:** All three scenarios (and indeed all 12 test cases) completed successfully, demonstrating reliability across diverse conditions.

---

## 6. Visualization Capabilities

### 6.1 Static Path Visualization

The system generates high-resolution (150 DPI) static images showing:
- Complete environment grid with obstacles in grayscale
- Computed path drawn as red line
- Start position marked with green circle
- Goal position marked with blue star
- Information box displaying scenario name, type, path length, and success status
- Legend identifying all visual elements

These visualizations are suitable for technical reports, presentations, and publications.

### 6.2 Animated Robot Movement

For each successful path, the system creates an animated GIF showing:
- Robot (rendered as red rectangle matching actual dimensions) moving along the path
- Planned path displayed as blue dashed reference line
- Progress indicator showing completion percentage
- Start and goal markers for orientation
- Frame rate of 10 FPS for smooth visualization

Animations range from 86 KB to 884 KB depending on path complexity and are ideal for presentations and demonstrations.

### 6.3 Performance Benchmarks

Two types of benchmark visualizations are generated:

**Individual Scenario Benchmarks:** Four-panel charts showing:
- Normalized comparison of key metrics (planning time, nodes explored, path length, path cost)
- Detailed map and robot configuration information
- Path quality analysis with specific values
- Exploration efficiency assessment with qualitative rating

**Comparison Benchmarks:** Generated when running multiple scenarios, showing:
- Side-by-side bar charts comparing path lengths, planning times, and exploration metrics
- Success rate pie chart
- Summary statistics across all tested scenarios

---

## 7. Discussion

### 7.1 Strengths and Advantages

**Reliability:** The 100% success rate across all test scenarios demonstrates robust performance. The algorithm successfully handled environments ranging from open spaces to complex mazes with dense obstacles.

**Computational Efficiency:** Average planning time of 68.9 ms makes the system suitable for practical applications. Even the largest scenario (2,640 cells) completed in under 250 ms.

**Path Quality:** Average step costs between 1.04 and 1.13 indicate paths are close to optimal. The algorithm naturally generates smooth, continuous trajectories suitable for robot execution.

**Visualization Support:** Comprehensive output formats including static images, animations, and benchmarks facilitate analysis, debugging, and presentation of results.

**Modular Architecture:** Clean separation of concerns enables independent testing and future enhancements without affecting other components.

### 7.2 Limitations and Challenges

**Static Environments:** Current implementation assumes obstacles do not move. Dynamic environments would require continuous replanning.

**Local Minima Susceptibility:** Potential field methods can theoretically get stuck in local minima (valleys in the potential field that are not the goal). While not observed in our test scenarios, this remains a theoretical limitation.

**Parameter Tuning:** Algorithm performance depends on properly tuned parameters. Different environments might benefit from different attractive/repulsive gain values.

**Grid Resolution:** Path quality is limited by grid discretization. Finer grids produce smoother paths but increase computation time.

**Kinematic Constraints:** The algorithm does not consider robot steering limitations or velocity constraints. Generated paths assume the robot can move in any direction.

### 7.3 Practical Applications

This path planning system is suitable for:

- **Educational Robotics:** Teaching path planning concepts with visual feedback
- **Warehouse Automation:** Computing paths for material handling robots in structured environments
- **Cleaning Robots:** Planning coverage paths in offices and homes
- **Simulation Environments:** Testing robot behaviors before physical deployment
- **Algorithm Prototyping:** Baseline for comparing other planning approaches

---

## 8. Conclusion

### 8.1 Project Summary

This project successfully implemented a potential field-based path planning system for autonomous mobile robots. The system achieved all primary objectives:

1. **Robust Algorithm:** 100% success rate across diverse test scenarios
2. **Efficient Implementation:** Average planning time of 68.9 ms suitable for real-time use
3. **Comprehensive Testing:** 12 scenarios covering various environmental complexities
4. **Advanced Visualizations:** Static images, animations, and performance benchmarks
5. **Modular Design:** Clean architecture supporting future extensions

The demonstration scenarios (Complex Maze, Dense Obstacle Field, and Large-Scale Environment) particularly showcase the algorithm's capabilities in challenging conditions, with planning times under 230 ms and near-optimal path quality.

### 8.2 Lessons Learned

**Architecture Matters:** Early investment in modular design simplified testing and visualization development. The ability to modify individual components without affecting others proved valuable.

**Testing Coverage:** Diverse test scenarios revealed algorithm behavior across edge cases. Starting with simple scenarios and progressively adding complexity helped validate each implementation stage.

**Visualization Value:** High-quality visualizations were crucial for understanding algorithm behavior, debugging issues, and presenting results. Animations were particularly effective for demonstrations.

**Parameter Impact:** Small changes in attractive and repulsive gains significantly affected path quality. Systematic testing was necessary to find robust default values.

### 8.3 Future Work

**Short-term Enhancements:**
- Add local minima escape mechanisms (random walk or simulated annealing)
- Implement path smoothing post-processing for more natural trajectories
- Support for dynamic obstacle updates and replanning
- Multi-resolution planning for very large environments

**Long-term Extensions:**
- Integration with real robot platforms (e.g., TurtleBot, mobile manipulators)
- Extension to 3D environments for aerial or underwater robots
- Multi-robot coordination with inter-robot collision avoidance
- Machine learning for automatic parameter optimization
- Incorporation of kinematic and dynamic constraints
- Uncertainty handling for partial observability scenarios

### 8.4 Concluding Remarks

The Micro-Navigator system demonstrates that potential field methods remain a valuable approach for path planning, offering an excellent balance between computational efficiency and path quality. The 100% success rate, fast planning times, and smooth generated paths make it suitable for both educational purposes and practical applications in structured environments. The comprehensive visualization suite and modular architecture provide a solid foundation for future research and development in autonomous navigation.

---

## References

1. Khatib, O. (1986). "Real-time obstacle avoidance for manipulators and mobile robots." *The International Journal of Robotics Research*, 5(1), 90-98.
   *Seminal paper introducing artificial potential fields for robot motion planning and obstacle avoidance.*

2. LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
   *Comprehensive textbook covering path planning algorithms including potential fields, sampling-based methods, and graph search.*

3. Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
   *Authoritative reference on mobile robotics including localization, mapping, and navigation.*

4. Choset, H., Lynch, K. M., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L. E., & Thrun, S. (2005). *Principles of Robot Motion: Theory, Algorithms, and Implementation*. MIT Press.
   *Detailed coverage of motion planning theory and practical algorithms for autonomous robots.*

5. Correll, N., Hayes, B., Heckman, C., & Roncone, A. (2022). *Introduction to Autonomous Robots: Mechanisms, Sensors, Actuators, and Algorithms* (2nd ed.). MIT Press.
   *Modern introduction to robotics with practical focus on autonomous systems and current technologies.*

6. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A formal basis for the heuristic determination of minimum cost paths." *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.
   *Classic paper introducing the A* algorithm, providing context for comparing graph-based vs. potential field approaches.*

---

## Appendix: System Usage

### Installation

```bash
# Create virtual environment
conda create -n micronavigator python=3.11
conda activate micronavigator

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify_system.py
```

### Running Scenarios

```bash
# List all scenarios
python run_scenarios.py --list

# Run single scenario
python run_scenarios.py 3

# Run demonstration scenarios
python run_scenarios.py 3 4 6

# Run all scenarios
python run_scenarios.py
```

### Output Files

All results saved to `output/` directory:
- `scenarioN_path.png` - Static path visualization
- `scenarioN_animation.gif` - Robot movement animation
- `scenarioN_benchmark.png` - Performance metrics chart
- `scenarioN_path.csv` - Waypoint coordinates
- `benchmark_comparison.png` - Multi-scenario comparison (when running multiple)
