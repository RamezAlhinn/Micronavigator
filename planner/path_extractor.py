import math
from collections import deque

# Direction vectors for 8-connected grid navigation
DIRECTION_OFFSETS = [
    (-1, 0),   # north
    (1, 0),    # south
    (0, -1),   # west
    (0, 1),    # east
    (-1, -1),  # northwest
    (-1, 1),   # northeast
    (1, -1),   # southwest
    (1, 1),    # southeast
]

def extract_path(potential, start, goal, statistics=None):
    """
    Extracts a path from start to goal using the potential field.
    Primary method: A* with potential field heuristic.
    Fallback method: Steepest descent on potential gradient.

    Args:
        potential: 2D array of potential values
        start: tuple (row, col) for starting location
        goal: tuple (row, col) for target location
        statistics: optional PlanningStatistics tracker

    Returns:
        list of (row, col) waypoints from start to goal
    """
    # Attempt A* pathfinding with potential field guidance
    trajectory, explored_count = compute_astar_path(potential, start, goal)

    if statistics:
        statistics.nodes_explored += explored_count

    if trajectory and trajectory[-1] == goal:
        return trajectory

    # A* unsuccessful - no feasible path found
    if not trajectory:
        print("A* pathfinding failed: start and goal may be disconnected.")
        print("Obstacle configuration may prevent valid path.")
        # Attempt steepest descent as backup
        return compute_gradient_path(potential, start, goal)

    # Backup strategy: steepest descent with loop prevention
    print("A* returned incomplete path, applying gradient descent...")
    return compute_gradient_path(potential, start, goal)


def compute_astar_path(potential, start, goal):
    """
    Implements A* algorithm with potential field as heuristic function.

    Returns:
        tuple: (waypoint_list, explored_node_count)
    """
    from heapq import heappush, heappop

    grid_rows = len(potential)
    grid_cols = len(potential[0])

    # Min-heap priority queue: (total_cost, accumulated_cost, position, trajectory)
    frontier = []
    heappush(frontier, (potential[start[0]][start[1]], 0, start, [start]))

    # Maintain optimal cost to reach each position
    cost_map = {start: 0}

    # Iteration limit for computational safety
    iteration_limit = grid_rows * grid_cols * 4
    iteration_count = 0
    explored_nodes = 0

    while frontier and iteration_count < iteration_limit:
        iteration_count += 1
        total_cost, accumulated_cost, current_pos, trajectory = heappop(frontier)
        explored_nodes += 1

        if current_pos == goal:
            return trajectory, explored_nodes

        row, col = current_pos

        for delta_row, delta_col in DIRECTION_OFFSETS:
            next_row, next_col = row + delta_row, col + delta_col

            # Boundary validation
            if not (0 <= next_row < grid_rows and 0 <= next_col < grid_cols):
                continue

            next_pos = (next_row, next_col)

            # Obstacle check
            if potential[next_row][next_col] == float("inf"):
                continue

            # Edge cost (diagonal movements are longer)
            edge_cost = math.sqrt(2) if (delta_row != 0 and delta_col != 0) else 1.0
            new_accumulated_cost = accumulated_cost + edge_cost

            # Update if better path found
            if next_pos not in cost_map or new_accumulated_cost < cost_map[next_pos]:
                cost_map[next_pos] = new_accumulated_cost
                estimated_total = new_accumulated_cost + potential[next_row][next_col]
                updated_trajectory = trajectory + [next_pos]
                heappush(frontier, (estimated_total, new_accumulated_cost, next_pos, updated_trajectory))

    return [], explored_nodes


def compute_gradient_path(potential, start, goal):
    """
    Performs steepest gradient descent on the potential field.
    Includes cycle detection to prevent infinite loops.
    """
    waypoints = [start]
    current_pos = start
    position_history = deque(maxlen=20)  # Circular buffer for cycle detection
    position_history.append(start)

    step_limit = len(potential) * len(potential[0]) * 2

    for step_num in range(step_limit):
        if current_pos == goal:
            return waypoints

        row, col = current_pos
        lowest_neighbor = None
        lowest_potential = float("inf")

        # Identify neighbor with minimum potential value
        for delta_row, delta_col in DIRECTION_OFFSETS:
            next_row, next_col = row + delta_row, col + delta_col

            if 0 <= next_row < len(potential) and 0 <= next_col < len(potential[0]):
                neighbor_pos = (next_row, next_col)
                neighbor_potential = potential[next_row][next_col]

                if neighbor_potential < lowest_potential:
                    lowest_potential = neighbor_potential
                    lowest_neighbor = neighbor_pos

        if lowest_neighbor is None or lowest_potential == float("inf"):
            print("Gradient descent halted: no reachable neighbors.")
            return waypoints

        # Cycle detection logic
        if step_num > 10 and lowest_neighbor in position_history:
            repetition_count = list(position_history).count(lowest_neighbor)
            if repetition_count > 2:
                print("Gradient descent halted: cyclic trajectory detected.")
                return waypoints

        waypoints.append(lowest_neighbor)
        position_history.append(lowest_neighbor)
        current_pos = lowest_neighbor

    print("Gradient descent halted: maximum step limit reached.")
    return waypoints
