# Configuration Parameters for Path Planning System
# Modify these values to tune system behavior

# Grid Cell Type Identifiers
FREE = 0        # Navigable free space
OBSTACLE = 1    # Impassable obstacle
START = 2       # Initial robot position
GOAL = 3        # Target destination

# Potential Field Tuning Parameters
ATTRACTIVE_GAIN = 1.0       # Goal attraction coefficient
REPULSIVE_GAIN = 50.0       # Obstacle repulsion coefficient
OBSTACLE_INFLUENCE = 3      # Repulsive field radius (grid cells)

# Robot Geometric Configuration
ROBOT_WIDTH = 2             # Horizontal dimension (grid cells)
ROBOT_HEIGHT = 2            # Vertical dimension (grid cells)

# Visualization Control
SHOW_POTENTIAL = True       # Enable potential field visualization