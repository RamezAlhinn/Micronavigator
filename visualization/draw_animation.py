import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from config.settings import FREE, OBSTACLE, START, GOAL

def create_animation(grid, path, robot_width, robot_height, output_file="robot_animation.gif", scenario_info=None):
    """
    Creates an animated GIF showing the robot moving along the path.

    Args:
        grid: 2D occupancy grid
        path: list of (row, col) tuples representing the path
        robot_width: robot width in grid cells
        robot_height: robot height in grid cells
        output_file: where to save the animation (default: "robot_animation.gif")
        scenario_info: dict with scenario metadata (optional)
    """

    if not path or len(path) == 0:
        print("No path to animate")
        return

    color_map = {
        FREE: 1.0,
        OBSTACLE: 0.0,
        START: 0.5,
        GOAL: 0.7
    }

    image = [[color_map[cell] for cell in row] for row in grid]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Display the grid
    ax.imshow(image, cmap="gray", alpha=0.8)

    # Plot the planned path
    y_coords = [p[1] for p in path]
    x_coords = [p[0] for p in path]
    ax.plot(y_coords, x_coords, 'b--', linewidth=1, alpha=0.5, label="Planned Path")

    # Mark start and goal
    ax.plot(y_coords[0], x_coords[0], 'go', markersize=10, label="Start")
    ax.plot(y_coords[-1], x_coords[-1], 'b*', markersize=12, label="Goal")

    # Create robot rectangle (will be updated in animation)
    robot_patch = Rectangle((0, 0), robot_width, robot_height,
                            linewidth=2, edgecolor='red', facecolor='red', alpha=0.6)
    ax.add_patch(robot_patch)

    # Add progress text
    progress_text = ax.text(0.02, 0.02, '', transform=ax.transAxes,
                          fontsize=10, verticalalignment='bottom',
                          bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    # Set title
    if scenario_info:
        title_text = f"Scenario: {scenario_info.get('name', 'Unknown')} - Robot Navigation"
        ax.set_title(title_text, fontsize=14, fontweight='bold')
    else:
        ax.set_title("Robot Navigation Animation", fontsize=14)

    ax.legend(loc='upper right')
    plt.tight_layout()

    def init():
        """Initialize animation"""
        robot_patch.set_xy((path[0][1] - robot_width/2, path[0][0] - robot_height/2))
        progress_text.set_text('Progress: 0%')
        return robot_patch, progress_text

    def animate(frame):
        """Update function for each frame"""
        if frame < len(path):
            pos = path[frame]
            # Center the robot on the path point
            robot_patch.set_xy((pos[1] - robot_width/2, pos[0] - robot_height/2))

            # Update progress
            progress = (frame + 1) / len(path) * 100
            progress_text.set_text(f'Progress: {progress:.1f}% ({frame + 1}/{len(path)})')

        return robot_patch, progress_text

    # Create animation
    # Use fewer frames for smoother animation
    frames = min(len(path), 100)  # Cap at 100 frames
    frame_indices = [int(i * len(path) / frames) for i in range(frames)]

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=frame_indices, interval=100,
                                  blit=True, repeat=True)

    # Save animation
    print(f"Creating animation with {len(frame_indices)} frames...")
    anim.save(output_file, writer='pillow', fps=10, dpi=100)
    plt.close()
    print(f"Animation saved to {output_file}")
