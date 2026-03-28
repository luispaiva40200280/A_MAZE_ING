import time
# Import your newly separated classes!
from Maze_Generation.helper_maze_classes import MazeConfig
from Maze_Generation.maze_generator import MazeGenerator

if __name__ == "__main__":
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)

        # 1. Setup the Configuration
        maze_config = MazeConfig(
            width=50,
            height=50,
            entry=(20, 20),
            exit=(49, 0),
            perfect=True
        )
        maze = MazeGenerator(maze_config)
        maze.generate_maze(starr_coord=maze.entry)
    except KeyboardInterrupt:
        print("\033[?1049l\033[7h\033[?25h\n\nAnimation stopped by user. \
               Exiting gracefully.")
