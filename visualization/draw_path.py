import matplotlib.pyplot as plt
from config.settings import FREE, OBSTACLE, START, GOAL

def draw_path(grid, path, output_file="path_output.png", title=None, scenario_info=None):
    """
    Draws the grid and overlays the path.

    Args:
        grid: 2D occupancy grid
        path: list of (row, col) tuples
        output_file: where to save the image (default: "path_output.png")
        title: custom title for the plot (optional)
        scenario_info: dict with scenario metadata for enhanced visualization (optional)
    """

    color_map = {
        FREE: 1.0,
        OBSTACLE: 0.0,
        START: 0.5,
        GOAL: 0.7
    }

    image = [[color_map[cell] for cell in row] for row in grid]

    # Create figure with better size
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(image, cmap="gray")

    # Extract x and y coordinates of the path
    y_coords = [p[1] for p in path]  # column = x axis
    x_coords = [p[0] for p in path]  # row = y axis

    # Plot path with start and end markers
    if path:
        ax.plot(y_coords, x_coords, color="red", linewidth=2, label="Path", zorder=5)
        ax.plot(y_coords[0], x_coords[0], 'go', markersize=12, label="Start", zorder=6)
        ax.plot(y_coords[-1], x_coords[-1], 'b*', markersize=15, label="Goal", zorder=6)
        ax.legend(loc='upper right')

    # Set title
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    elif scenario_info:
        title_text = f"Scenario: {scenario_info.get('name', 'Unknown')}"
        ax.set_title(title_text, fontsize=14, fontweight='bold')
    else:
        ax.set_title("Path on Grid", fontsize=14)

    # Add scenario info as text annotation
    if scenario_info:
        info_lines = []
        if 'description' in scenario_info:
            info_lines.append(f"Type: {scenario_info['description']}")
        if 'path_length' in scenario_info:
            info_lines.append(f"Path Length: {scenario_info['path_length']} waypoints")
        if 'success' in scenario_info:
            status = "Success" if scenario_info['success'] else "Failed"
            info_lines.append(f"Status: {status}")

        if info_lines:
            info_text = '\n'.join(info_lines)
            ax.text(0.02, 0.98, info_text,
                   transform=ax.transAxes,
                   fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

