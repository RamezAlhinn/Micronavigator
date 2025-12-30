import matplotlib
matplotlib.use("Agg")

from map.grid_loader import load_grid
from planner.potential_field import compute_potential_field
from planner.path_extractor import extract_path
from planner.statistics import PlanningStatistics
from visualization.draw_map import draw_map
from visualization.draw_path import draw_path
from robot.exporter import export_path
from robot.shape_handler import inflate_obstacles
from config.settings import ROBOT_WIDTH, ROBOT_HEIGHT

def main():
    print("\n" + "="*60)
    print(" MICRO-NAVIGATOR - SINGLE SCENARIO EXECUTION")
    print("="*60)

    # Create statistics tracking object
    performance_tracker = PlanningStatistics()

    # Step 1: Load environment map
    environment_grid, start_position, goal_position = load_grid("map/example_map.txt")
    print(f"Start Position: {start_position}, Goal Position: {goal_position}")
    print(f"Robot Dimensions: {ROBOT_HEIGHT} x {ROBOT_WIDTH} cells")

    # Configure statistics with map parameters
    performance_tracker.set_map_info(environment_grid, ROBOT_WIDTH, ROBOT_HEIGHT)

    # Step 2: Render occupancy grid
    draw_map(environment_grid)

    # Step 3: Apply obstacle expansion for robot geometry
    print("\nExpanding obstacles to account for robot footprint...")
    expanded_grid = inflate_obstacles(environment_grid, ROBOT_WIDTH, ROBOT_HEIGHT)

    # Step 4: Generate navigation potential field
    print("Generating navigation potential field...")
    performance_tracker.start_timer()
    navigation_potential = compute_potential_field(expanded_grid, goal_position)

    # Step 5: Compute trajectory
    print("Computing optimal trajectory...")
    trajectory = extract_path(navigation_potential, start_position, goal_position, statistics=performance_tracker)
    performance_tracker.stop_timer()

    # Step 6: Validate path completion
    if trajectory and trajectory[-1] == goal_position:
        performance_tracker.set_success(True)
        performance_tracker.set_path_info(trajectory)
        print(f"Trajectory successfully computed! Length: {len(trajectory)} waypoints")
    else:
        performance_tracker.set_success(False, "Goal position not reached")
        print("Warning: Trajectory terminated before reaching goal")

    # Step 7: Generate path visualization
    draw_path(environment_grid, trajectory)
    print("Trajectory visualization saved to path_output.png")

    # Step 8: Export waypoints for robot controller
    export_path(trajectory, "robot/path_output.csv")
    print("Waypoint data exported to robot/path_output.csv")

    # Step 9: Display performance metrics
    print("\n" + performance_tracker.get_summary())

if __name__ == "__main__":
    main()
