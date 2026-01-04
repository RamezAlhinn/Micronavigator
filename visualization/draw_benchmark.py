import matplotlib.pyplot as plt
import numpy as np

def create_benchmark_chart(results, output_file="benchmark_chart.png"):
    """
    Creates a benchmark chart comparing multiple scenario results.

    Args:
        results: list of result dictionaries with scenario data
        output_file: where to save the chart (default: "benchmark_chart.png")
    """

    if not results or len(results) == 0:
        print("No results to chart")
        return

    # Extract data
    scenario_names = [f"S{r['scenario']}: {r['name']}" for r in results]
    path_lengths = [r.get('path_length', 0) for r in results]
    planning_times = []
    nodes_explored = []
    success_status = [r.get('success', False) for r in results]

    # Extract stats if available
    for r in results:
        if 'stats' in r and r['stats']:
            stats_dict = r['stats'].get_dict()
            planning_times.append(stats_dict.get('planning_time_ms', 0))
            nodes_explored.append(stats_dict.get('nodes_explored', 0))
        else:
            planning_times.append(0)
            nodes_explored.append(0)

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Scenario Performance Benchmark', fontsize=16, fontweight='bold')

    # Color code by success/failure
    colors = ['green' if s else 'red' for s in success_status]

    # 1. Path Length Comparison
    ax1 = axes[0, 0]
    bars1 = ax1.bar(range(len(scenario_names)), path_lengths, color=colors, alpha=0.7)
    ax1.set_xlabel('Scenario', fontsize=10)
    ax1.set_ylabel('Path Length (waypoints)', fontsize=10)
    ax1.set_title('Path Length by Scenario', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(scenario_names)))
    ax1.set_xticklabels([f"S{r['scenario']}" for r in results], rotation=0)
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars1, path_lengths)):
        if val > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(path_lengths)*0.01,
                    str(val), ha='center', va='bottom', fontsize=9)

    # 2. Planning Time Comparison
    ax2 = axes[0, 1]
    bars2 = ax2.bar(range(len(scenario_names)), planning_times, color=colors, alpha=0.7)
    ax2.set_xlabel('Scenario', fontsize=10)
    ax2.set_ylabel('Planning Time (ms)', fontsize=10)
    ax2.set_title('Planning Time by Scenario', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(scenario_names)))
    ax2.set_xticklabels([f"S{r['scenario']}" for r in results], rotation=0)
    ax2.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars2, planning_times)):
        if val > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(planning_times)*0.01,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9)

    # 3. Nodes Explored Comparison
    ax3 = axes[1, 0]
    bars3 = ax3.bar(range(len(scenario_names)), nodes_explored, color=colors, alpha=0.7)
    ax3.set_xlabel('Scenario', fontsize=10)
    ax3.set_ylabel('Nodes Explored', fontsize=10)
    ax3.set_title('Exploration Efficiency by Scenario', fontsize=12, fontweight='bold')
    ax3.set_xticks(range(len(scenario_names)))
    ax3.set_xticklabels([f"S{r['scenario']}" for r in results], rotation=0)
    ax3.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars3, nodes_explored)):
        if val > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(nodes_explored)*0.01,
                    str(val), ha='center', va='bottom', fontsize=9)

    # 4. Success Rate Summary
    ax4 = axes[1, 1]
    success_count = sum(success_status)
    total_count = len(success_status)
    fail_count = total_count - success_count

    wedges, texts, autotexts = ax4.pie(
        [success_count, fail_count],
        labels=['Success', 'Failed'],
        colors=['green', 'red'],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    ax4.set_title(f'Success Rate: {success_count}/{total_count}', fontsize=12, fontweight='bold')

    # Add summary statistics as text
    summary_text = (
        f"Total Scenarios: {total_count}\n"
        f"Successful: {success_count}\n"
        f"Failed: {fail_count}\n"
        f"Avg Path Length: {np.mean([p for p in path_lengths if p > 0]):.1f}\n"
        f"Avg Planning Time: {np.mean([t for t in planning_times if t > 0]):.2f} ms"
    )

    ax4.text(0.02, 0.02, summary_text,
            transform=ax4.transAxes,
            fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Benchmark chart saved to {output_file}")


def create_single_scenario_benchmark(scenario_num, scenario_name, stats, output_file="scenario_benchmark.png"):
    """
    Creates a detailed benchmark chart for a single scenario.

    Args:
        scenario_num: scenario number
        scenario_name: scenario name
        stats: PlanningStatistics object
        output_file: where to save the chart
    """

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Scenario {scenario_num}: {scenario_name} - Performance Metrics',
                fontsize=14, fontweight='bold')

    # Extract metrics from stats dict
    stats_dict = stats.get_dict()
    planning_time_ms = stats_dict.get('planning_time_ms', 0)
    nodes_explored = stats_dict.get('nodes_explored', 0)
    path_length = stats_dict.get('path_length', 0)
    path_cost = stats_dict.get('path_cost', 0)
    map_rows = stats_dict.get('map_rows', 0)
    map_cols = stats_dict.get('map_cols', 0)
    num_obstacles = stats_dict.get('num_obstacles', 0)
    robot_width = stats_dict.get('robot_width', 0)
    robot_height = stats_dict.get('robot_height', 0)
    success = stats_dict.get('success', False)

    # 1. Key Metrics Bar Chart
    ax1 = axes[0, 0]
    metrics = ['Planning\nTime (ms)', 'Nodes\nExplored', 'Path\nLength', 'Path\nCost']
    values = [planning_time_ms, nodes_explored, path_length, path_cost]
    normalized_values = [v / max(values) * 100 for v in values]

    bars = ax1.barh(metrics, normalized_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax1.set_xlabel('Normalized Value (%)', fontsize=10)
    ax1.set_title('Performance Metrics Overview', fontsize=11, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)

    # Add actual values as labels
    for i, (bar, val, norm_val) in enumerate(zip(bars, values, normalized_values)):
        ax1.text(norm_val + 2, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontsize=9)

    # 2. Map Statistics
    ax2 = axes[0, 1]
    ax2.axis('off')

    map_stats = f"""
    MAP INFORMATION
    {'='*30}
    Map Size: {map_rows} × {map_cols} cells
    Total Cells: {map_rows * map_cols}
    Obstacles: {num_obstacles}
    Free Space: {map_rows * map_cols - num_obstacles}

    ROBOT CONFIGURATION
    {'='*30}
    Robot Size: {robot_height} × {robot_width} cells
    Footprint: {robot_height * robot_width} cells

    PLANNING RESULTS
    {'='*30}
    Status: {'✓ SUCCESS' if success else '✗ FAILED'}
    Planning Time: {planning_time_ms:.2f} ms
    Nodes Explored: {nodes_explored}
    """

    ax2.text(0.1, 0.9, map_stats, transform=ax2.transAxes,
            fontsize=9, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

    # 3. Path Quality Metrics
    ax3 = axes[1, 0]
    if path_length > 0:
        avg_step_cost = path_cost / path_length
        quality_metrics = ['Path Length', 'Total Cost', 'Avg Step Cost']
        quality_values = [path_length, path_cost, avg_step_cost]

        bars3 = ax3.bar(quality_metrics, quality_values, color=['#2ca02c', '#d62728', '#9467bd'])
        ax3.set_ylabel('Value', fontsize=10)
        ax3.set_title('Path Quality Metrics', fontsize=11, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar, val in zip(bars3, quality_values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(quality_values)*0.01,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    else:
        ax3.text(0.5, 0.5, 'No Path Found', ha='center', va='center',
                transform=ax3.transAxes, fontsize=14, color='red')
        ax3.set_title('Path Quality Metrics', fontsize=11, fontweight='bold')

    # 4. Efficiency Ratio
    ax4 = axes[1, 1]
    if nodes_explored > 0 and path_length > 0:
        exploration_ratio = nodes_explored / path_length
        efficiency = path_length / nodes_explored * 100

        ax4.bar(['Exploration\nRatio', 'Efficiency\n(%)'],
               [exploration_ratio, efficiency],
               color=['#ff7f0e', '#1f77b4'])
        ax4.set_ylabel('Value', fontsize=10)
        ax4.set_title('Exploration Efficiency', fontsize=11, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        # Add interpretation text
        if efficiency > 80:
            interpretation = "Excellent"
            color = 'green'
        elif efficiency > 50:
            interpretation = "Good"
            color = 'orange'
        else:
            interpretation = "Could be improved"
            color = 'red'

        ax4.text(0.5, 0.02, f'Overall: {interpretation}',
                transform=ax4.transAxes, ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=color,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    else:
        ax4.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center',
                transform=ax4.transAxes, fontsize=14, color='gray')
        ax4.set_title('Exploration Efficiency', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Scenario benchmark chart saved to {output_file}")
