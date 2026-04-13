import sys
from .maze_generator import MazeGenerator
from .pallete import Themes
from .maze_sotore import MazeDataBase
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
        import tty
        import termios
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
        """
        Just gets a new random theme of my themes list
        and changes the curr theme of the maze,
        to genarate the same maze whith diferent colors
        """
        import random
        chosing_themes = [t for t in LIST_THEMES
                          if t != self.maze.active_theme]
        random_theme = random.choice(chosing_themes)
        self.maze.active_theme = random_theme
        self.maze.draw_ascii_grid()
        self.maze.draw_stats_hud()

    def clean_screen(self) -> None:
        from os import system, name
        import time
        """
        # 1. ANSI Cleanup Sequence
        \033[0m       -> Reset all text colors to terminal default
        \033[?25h     -> Un-hide the cursor
        \033[?1049l   -> Close the "Alternate Screen" buffer
        """
        print("\033[0m\033[?25h\033[?1049l", end="", flush=True)
        system('cls' if name == 'nt' else 'clear')
        msg = "Exit successfully..."
        # 2. Use your Viewport's math to find the center!
        # Add half the viewport's height to its starting Y position
        center_y = (self.maze.viewport.offset_y
                    + (self.maze.viewport.height // 2))
        # Add half the viewport's width to its starting X, minus half the
        # message length
        center_x = (self.maze.viewport.offset_x
                    + (self.maze.viewport.width // 2) - (len(msg) // 2))
        # 3. Print exactly in the center using \033[{y};{x}H
        print(f"\033[{center_y};{center_x}H\033[92m{msg}\033[0m\n\n")
        time.sleep(0.70)

    def generate_new_maze(self) -> None:
        self.maze.reset_grid()
        self.maze.generate_maze(self.maze.entry)
        MazeDataBase(maze=self.maze).export_maze_txt(self.maze.grid)

    def run(self) -> None:
        self.maze.carve_42_pattern()
        self.maze.draw_ascii_grid()
        self.maze.draw_stats_hud()
        menu_options = [
            {
                'txt': "1: Generate New Maze",
                'func': lambda: self.generate_new_maze()
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
                'func': lambda: self.clean_screen()
            }
        ]
        select_indx = 0
        while True:
            menu_y = (self.maze.viewport.offset_y
                      + self.maze.viewport.height + 1)
            print(f"\033[{menu_y};{self.maze.offset_x}H\033[K", end="")

            for i, opt in enumerate(menu_options):
                if i == select_indx:
                    print(f"{self.maze.active_theme.get_color('logo')}\
\033[1;30m > {opt['txt']} \033[0m  ", end="")
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
                    if callable(action):
                        action()
                    if select_indx == 3:
                        break
