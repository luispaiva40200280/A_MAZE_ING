import time
import sys
import os
import tty
import termios
from Maze_Generation.helper_maze_classes import MazeConfig
from Maze_Generation.maze_generator import MazeGenerator
from pydantic import ValidationError

FOLDER = 'Configs'


def get_keypress() -> str:
    """Reads a single keypress from the 
    terminal without requiring Enter.
    """
    fd = sys.stdin.fileno()
    sett = termios.tcgetattr(fd)
    try:
        # setcbreak allows us to read keys instantly,
        # but still lets Ctrl+C kill the program if
        # it gets stuck
        tty.setcbreak(fd)
        charcter = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, sett)
    return charcter


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
        maze_config = MazeConfig.parser_file(FINAL_PATH)
        maze = MazeGenerator(maze_config)
        maze.generate_maze(starr_coord=maze_config.entry)
    except ValidationError as e:
        print("\n\033[91m[Configuration Error] Your config.txt file has \
invalid data:\033[0m")
        for error in e.errors():
            failed_field = (error.get("loc")[0] if error.get("loc")
                            else "General")
            reason = error.get("msg")
            print(f"\033[93m ╰─▶ '{failed_field}': {reason}\033[0m")
