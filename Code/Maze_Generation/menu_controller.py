import sys
import tty
import termios
from .maze_generator import MazeGenerator
from .pallete import Themes

LIST_THEMES = list(Themes)


class Controller:
    """This class controls the menu of choices in
    maze genarator, wiht keypresses, just as:
     » change theme
     » change algorithm for the construct of the maze
     » show shorts path or hide it
     »» make it playble ???
     """
    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze
        self.is_generate: bool = False

    def _get_key_press(self) -> str:
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

    def get_random_theme(self) -> None:
        import random
        random_theme = random.choice(LIST_THEMES)
        self.maze.active_theme = random_theme
        self.maze.draw_ascii_grid()
        self.maze.draw_stats_hdu()

    def run(self) -> None:
        self.maze.carve_42_pattern()
        self.maze.draw_ascii_grid()
        self.maze.draw_stats_hdu()
        menu_options = [
            {
                'txt': "1: Generate New Maze",
                'func': lambda: (
                    self.maze.reset_grid(),
                    self.maze.generate_maze(self.maze.entry)
                )
            },
            {
                'txt': "2: Toggle Path",
                'func': lambda: print('show the shortes path')
            },
            {
                'txt': "3: Change Theme",
                'func': lambda: self.get_random_theme()
            },
            {
                'txt': "4: Exit",
                'func': "Quit"
            }
        ]
        select_indx = 0
        while True:
            menu_y = (self.maze.viewport.offset_y
                      + self.maze.viewport.height + 1)
            print(f"\033[{menu_y};{self.maze.offset_x}H\033[K", end="")

            for i, opt in enumerate(menu_options):
                if i == select_indx:
                    print(f"{self.maze.active_theme.get_color('walls')} > \
{opt['txt']} \033[0m  ", end="")
                else:
                    print(f"   {opt['txt']}    ", end="")
            sys.stdout.flush()
            key = self._get_key_press().lower()
            match key:
                case '1':
                    select_indx = 0
                case '2':
                    select_indx = 1
                case '3':
                    select_indx = 2
                case '4':
                    select_indx = 3
                case ('\r' | '\n'):
                    action = menu_options[select_indx]['func']
                    if action == "Quit":
                        break
                    else:
                        action()
