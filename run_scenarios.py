#!/usr/bin/env python3
"""
Scenario Runner - Execute individual or all scenarios with enhanced visualization

Usage:
    python run_scenarios.py                    # Run all scenarios
    python run_scenarios.py 1                  # Run scenario 1
    python run_scenarios.py 1 3 5              # Run scenarios 1, 3, and 5
    python run_scenarios.py --list             # List all available scenarios
"""

import sys
import matplotlib
matplotlib.use("Agg")

from map.grid_loader import load_grid
from planner.potential_field import compute_potential_field
from planner.path_extractor import extract_path
from planner.statistics import PlanningStatistics
from visualization.draw_path import draw_path
from visualization.draw_animation import create_animation
from visualization.draw_benchmark import create_single_scenario_benchmark, create_benchmark_chart
from robot.exporter import export_path
from robot.shape_handler import inflate_obstacles


# Define all available scenarios
SCENARIOS = {
    # High-resolution scenarios (recommended for demonstrations)
    1: {
        "name": "Open Space Navigation",
        "map_file": "map/scenario1_simple_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Obstacle-free pathfinding"
    },
    2: {
        "name": "Corridor Traversal",
        "map_file": "map/scenario2_corridor_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Constrained passage navigation"
    },
    3: {
        "name": "Complex Maze",
        "map_file": "map/scenario3_maze_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Multi-turn maze solving"
    },
    4: {
        "name": "Dense Obstacle Field",
        "map_file": "map/scenario4_cluttered_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "High-density obstacle avoidance"
    },
    5: {
        "name": "Narrow Gap Challenge",
        "map_file": "map/scenario5_narrow_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Precision maneuvering"
    },
    6: {
        "name": "Large-Scale Environment",
        "map_file": "map/scenario6_large_highres.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Extended range planning"
    },
    # Standard resolution scenarios (faster execution)
    7: {
        "name": "Open Space (Fast)",
        "map_file": "map/scenario1_simple.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Quick baseline test"
    },
    8: {
        "name": "Corridor (Fast)",
        "map_file": "map/scenario2_corridor.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Rapid corridor test"
    },
    9: {
        "name": "Maze (Fast)",
        "map_file": "map/scenario3_maze.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Quick maze validation"
    },
    10: {
        "name": "Obstacles (Fast)",
        "map_file": "map/scenario4_cluttered.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Fast obstacle testing"
    },
    11: {
        "name": "Narrow Gap (Fast)",
        "map_file": "map/scenario5_narrow.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Quick precision test"
    },
    12: {
        "name": "Large Map (Fast)",
        "map_file": "map/scenario6_large.txt",
        "robot_width": 1,
        "robot_height": 1,
        "description": "Rapid scalability test"
    },
}


def run_scenario(scenario_num, scenario_config):
    """Execute a single scenario and return results"""

    print("\n" + "="*70)
    print(f" SCENARIO {scenario_num}: {scenario_config['name'].upper()}")
    print("="*70)
    print(f"Description: {scenario_config['description']}")
    print(f"Map File: {scenario_config['map_file']}")
    print(f"Robot Size: {scenario_config['robot_height']}x{scenario_config['robot_width']} cells")

    # Create statistics tracker
    stats = PlanningStatistics()

    try:
        # Load map
        grid, start, goal = load_grid(scenario_config['map_file'])
        print(f"Start: {start}, Goal: {goal}")
        print(f"Grid Size: {len(grid)}x{len(grid[0])} cells")

        # Set up statistics
        stats.set_map_info(grid, scenario_config['robot_width'], scenario_config['robot_height'])

        # Inflate obstacles
        print("\nInflating obstacles for robot footprint...")
        inflated_grid = inflate_obstacles(grid, scenario_config['robot_width'], scenario_config['robot_height'])

        # Compute potential field
        print("Computing potential field...")
        stats.start_timer()
        potential = compute_potential_field(inflated_grid, goal)

        # Extract path
        print("Extracting path...")
        path = extract_path(potential, start, goal, statistics=stats)
        stats.stop_timer()

        # Validate results
        success = path and path[-1] == goal
        if success:
            stats.set_success(True)
            stats.set_path_info(path)
            print(f"✓ Path found! Length: {len(path)} waypoints")
        else:
            stats.set_success(False, "Goal not reached")
            print("✗ Failed to reach goal")

        # Generate visualization with scenario info
        output_path = f"output/scenario{scenario_num}_path.png"
        viz_info = {
            'name': scenario_config['name'],
            'description': scenario_config['description'],
            'path_length': len(path) if path else 0,
            'success': success
        }
        draw_path(grid, path, output_file=output_path, scenario_info=viz_info)
        print(f"Visualization saved: {output_path}")

        # Export path
        csv_path = f"output/scenario{scenario_num}_path.csv"
        export_path(path, csv_path)
        print(f"Path data exported: {csv_path}")

        # Create animation
        if success:
            animation_path = f"output/scenario{scenario_num}_animation.gif"
            print(f"\nGenerating robot animation...")
            create_animation(grid, path, scenario_config['robot_width'],
                           scenario_config['robot_height'],
                           output_file=animation_path,
                           scenario_info=viz_info)

        # Create benchmark chart for single scenario
        benchmark_path = f"output/scenario{scenario_num}_benchmark.png"
        print(f"Generating benchmark chart...")
        create_single_scenario_benchmark(scenario_num, scenario_config['name'],
                                        stats, output_file=benchmark_path)

        # Print statistics
        print("\n" + stats.get_summary())

        return {
            "scenario": scenario_num,
            "name": scenario_config['name'],
            "success": path and path[-1] == goal,
            "path_length": len(path) if path else 0,
            "stats": stats
        }

    except Exception as e:
        print(f"✗ Error running scenario: {e}")
        return {
            "scenario": scenario_num,
            "name": scenario_config['name'],
            "success": False,
            "error": str(e)
        }


def list_scenarios():
    """Display all available scenarios"""
    print("\n" + "="*70)
    print(" AVAILABLE SCENARIOS")
    print("="*70)
    for num, config in SCENARIOS.items():
        print(f"  {num}. {config['name']:<25} - {config['description']}")
    print("="*70)


def print_summary(results):
    """Print summary of all executed scenarios"""
    print("\n" + "="*70)
    print(" EXECUTION SUMMARY")
    print("="*70)

    successful = sum(1 for r in results if r['success'])
    total = len(results)

    print(f"\nScenarios Run: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {successful/total*100:.1f}%")

    print("\nDetailed Results:")
    print("-" * 70)
    for r in results:
        status = "✓" if r['success'] else "✗"
        path_info = f"({r['path_length']} waypoints)" if r['success'] else "(failed)"
        print(f"  {status} Scenario {r['scenario']}: {r['name']:<25} {path_info}")
    print("="*70)


def main():
    """Main entry point"""

    # Parse command line arguments
    if "--list" in sys.argv or "-l" in sys.argv:
        list_scenarios()
        return

    # Determine which scenarios to run
    scenario_nums = []

    if len(sys.argv) > 1:
        # Run specific scenarios
        for arg in sys.argv[1:]:
            try:
                num = int(arg)
                if num in SCENARIOS:
                    scenario_nums.append(num)
                else:
                    print(f"Warning: Scenario {num} does not exist")
            except ValueError:
                print(f"Warning: '{arg}' is not a valid scenario number")
    else:
        # Run all scenarios
        scenario_nums = sorted(SCENARIOS.keys())

    if not scenario_nums:
        print("No scenarios to run. Use --list to see available scenarios.")
        return

    print("\n" + "="*70)
    print(" MICRO-NAVIGATOR SCENARIO RUNNER")
    print("="*70)
    print(f"Running {len(scenario_nums)} scenario(s): {', '.join(map(str, scenario_nums))}")

    # Create output directory if needed
    import os
    os.makedirs("output", exist_ok=True)

    # Run scenarios
    results = []
    for num in scenario_nums:
        result = run_scenario(num, SCENARIOS[num])
        results.append(result)

    # Print summary if multiple scenarios
    if len(results) > 1:
        print_summary(results)

        # Generate comparison benchmark chart
        print("\nGenerating comparison benchmark chart...")
        create_benchmark_chart(results, output_file="output/benchmark_comparison.png")

    print("\n" + "="*70)
    print(" COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
