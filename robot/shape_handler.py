from config.settings import OBSTACLE, ROBOT_WIDTH, ROBOT_HEIGHT

def inflate_obstacles(grid, robot_width=None, robot_height=None):
    """
    Expands obstacle boundaries to accommodate robot footprint.
    Allows point-mass planning for rectangular robots.

    Args:
        grid: 2D occupancy grid representation
        robot_width: horizontal robot dimension (grid cells)
        robot_height: vertical robot dimension (grid cells)

    Returns:
        modified grid with expanded obstacles
    """
    if robot_width is None:
        robot_width = ROBOT_WIDTH
    if robot_height is None:
        robot_height = ROBOT_HEIGHT

    num_rows = len(grid)
    num_cols = len(grid[0])

    # Deep copy grid to avoid modifying original
    expanded_grid = [row[:] for row in grid]

    # Compute expansion margins based on robot dimensions
    vertical_margin = (robot_height - 1) // 2
    horizontal_margin = (robot_width - 1) // 2

    # Locate all obstacle positions
    obstacle_positions = []
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            if grid[row_idx][col_idx] == OBSTACLE:
                obstacle_positions.append((row_idx, col_idx))

    # Apply inflation around each obstacle
    for obs_row, obs_col in obstacle_positions:
        for row_offset in range(-vertical_margin, vertical_margin + 1):
            for col_offset in range(-horizontal_margin, horizontal_margin + 1):
                target_row, target_col = obs_row + row_offset, obs_col + col_offset

                # Boundary check
                if 0 <= target_row < num_rows and 0 <= target_col < num_cols:
                    # Mark free space as obstacle
                    if expanded_grid[target_row][target_col] == 0:
                        expanded_grid[target_row][target_col] = OBSTACLE

    return expanded_grid


def check_robot_collision(grid, position, robot_width=None, robot_height=None):
    """
    Verifies whether robot placement at given position results in collision.

    Args:
        grid: 2D occupancy grid
        position: (row, col) robot center coordinates
        robot_width: horizontal footprint dimension
        robot_height: vertical footprint dimension

    Returns:
        True if collision exists, False if position is valid
    """
    if robot_width is None:
        robot_width = ROBOT_WIDTH
    if robot_height is None:
        robot_height = ROBOT_HEIGHT

    center_row, center_col = position
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Determine robot footprint extents
    half_height = robot_height // 2
    half_width = robot_width // 2

    # Verify all cells within robot footprint
    for row_offset in range(-half_height, half_height + 1):
        for col_offset in range(-half_width, half_width + 1):
            check_row, check_col = center_row + row_offset, center_col + col_offset

            # Boundary collision
            if not (0 <= check_row < num_rows and 0 <= check_col < num_cols):
                return True

            # Obstacle collision
            if grid[check_row][check_col] == OBSTACLE:
                return True

    return False
