import time
# Import your newly separated classes!
from Maze_Generation.helper_maze_classes import MazeConfig
from Maze_Generation.maze_generator import MazeGenerator

if __name__ == "__main__":
    """quik test for mazegenerator"""
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)

        # 1. Setup the Configuration
        try:
            maze_config = MazeConfig.parser_file("Configs/config.txt")
            maze = MazeGenerator(maze_config)
            maze.generate_maze(starr_coord=maze.entry)
        except Exception as e:
            print(e)
    except KeyboardInterrupt: 
        print("\033[?1049l\033[7h\033[?25h\n\nAnimation stopped by user. \
               Exiting gracefully.")
