import math
from config.settings import (
    ATTRACTIVE_GAIN,
    REPULSIVE_GAIN,
    OBSTACLE_INFLUENCE,
    OBSTACLE
)

def compute_potential_field(grid, goal):
    """
    Generates navigation potential field combining attractive and repulsive forces.

    Args:
        grid: 2D occupancy grid
        goal: target position (row, col)

    Returns:
        2D array of potential values
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    potential_field = [[0.0 for _ in range(num_cols)] for _ in range(num_rows)]

    for row_idx in range(num_rows):
        for col_idx in range(num_cols):

            if grid[row_idx][col_idx] == OBSTACLE:
                potential_field[row_idx][col_idx] = float("inf")
                continue

            # Attractive component: pulls robot toward goal
            # Larger distance → higher potential
            goal_distance = math.dist((row_idx, col_idx), goal)
            attractive_potential = ATTRACTIVE_GAIN * goal_distance

            # Repulsive component: pushes robot away from obstacles
            obstacle_distance = compute_nearest_obstacle_distance(grid, row_idx, col_idx)

            if obstacle_distance <= OBSTACLE_INFLUENCE:
                repulsive_potential = REPULSIVE_GAIN * (1.0 / obstacle_distance - 1.0 / OBSTACLE_INFLUENCE) ** 2
            else:
                repulsive_potential = 0

            # Superposition of potential fields
            potential_field[row_idx][col_idx] = attractive_potential + repulsive_potential

    return potential_field


def compute_nearest_obstacle_distance(grid, row, col):
    """
    Calculates Euclidean distance from given position to closest obstacle.

    Args:
        grid: 2D occupancy grid
        row: query row index
        col: query column index

    Returns:
        minimum distance to any obstacle cell
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    minimum_distance = float("inf")

    for obstacle_row in range(num_rows):
        for obstacle_col in range(num_cols):
            if grid[obstacle_row][obstacle_col] == OBSTACLE:
                distance = math.dist((row, col), (obstacle_row, obstacle_col))
                if distance < minimum_distance:
                    minimum_distance = distance

    return minimum_distance
