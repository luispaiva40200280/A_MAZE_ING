import time
from Maze_Generation.helper_maze_classes import MazeConfig
from Maze_Generation.maze_generator import MazeGenerator
from pydantic import ValidationError

if __name__ == "__main__":
    """quik test for mazegenerator"""
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)
        try:
            maze_config = MazeConfig.parser_file("Configs/config.txt")
            maze = MazeGenerator(maze_config)
            maze.generate_maze(starr_coord=maze.entry)
        except ValidationError as e:
            print("\n\033[91m[Configuration Error] Your config.txt file has \
invalid data:\033[0m")
            for error in e.errors():
                failed_field = (error.get("loc")[0] if error.get("loc")
                                else "General")
                reason = error.get("msg")
                print(f"\033[93m ╰─▶ '{failed_field}': {reason}\033[0m")
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        print("\033[?1049l\033[7h\033[?25h\n\nAnimation stopped by user. \
               Exiting gracefully.")
