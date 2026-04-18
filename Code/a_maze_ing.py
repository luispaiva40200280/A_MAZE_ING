import time
import sys
import os
from Maze_Generation.menu_controller import Controller
from Maze_Generation.helper_maze_classes import MazeConfig
from Maze_Generation.maze_generator import MazeGenerator
from Maze_Generation.maze_sotore import MazeDataBase
from pydantic import ValidationError

FOLDER = 'Configs'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage: a-maze-ing <config.txt>\033[0m")
        sys.exit(1)

    FILE_NAME = sys.argv[1]
    if os.path.exists(FILE_NAME):
        FINAL_PATH = FILE_NAME
    elif os.path.exists(os.path.join(FOLDER, FILE_NAME)):
        FINAL_PATH = os.path.join(FOLDER, FILE_NAME)
    else:
        print(f"\033[93mFile '{FILE_NAME}' was not found in the root \
directory or the {FOLDER}/ folder!\033[0m")
        sys.exit(1)
    try:
        print("Initializing Maze Generator...")
        time.sleep(0.01)
        # Difining the variables of my maze and the menu
        maze_config = MazeConfig.parser_file(FINAL_PATH)
        maze = MazeGenerator(maze_config)
        menu = Controller(maze)
        # START OF STORING THE MAZE GENERATED IN maze.txt
        # runing the maze itself
        maze.generate_maze()
        datbase = MazeDataBase(maze=maze)
        datbase.export_maze_txt(maze.grid)
        menu.run()
    except ValidationError as e:
        print("\n\033[91m[Configuration Error] Your config.txt file has \
invalid data:\033[0m")
        for error in e.errors():
            failed_field = (error.get("loc", ())[0] if error.get("loc")
                            else "General")
            reason = error.get("msg")
            print(f"\033[93m ╰─▶ '{failed_field}': {reason}\033[0m")
        time.sleep(2)
    except KeyboardInterrupt:
        # If they press Ctrl+C ANYWHERE, Python jumps straight here!
        menu.clean_screen()
        time.sleep(2)
        sys.exit(0)
    except ValueError as e:
        print(f"\033[93m Error': {e}\033[0m")
        time.sleep(2)
