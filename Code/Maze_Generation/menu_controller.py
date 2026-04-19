"""
Interactive Terminal UI and Menu Controller for the Maze Generator.

This module provides the `Controller` class, which acts as the primary user
interface manager for the application. It establishes an unbuffered,
interactive terminal loop that listens for raw keystrokes to navigate
and execute menu options in real-time.

Responsibilities:
    - Managing the application's main execution loop.
    - Capturing silent keyboard inputs (without requiring the 'Enter' key).
    - Routing user commands to the core `MazeGenerator` engine (e.g.,
      regenerating mazes, toggling solution paths, cycling themes, and
      swapping generation algorithms).
    - Managing graceful application exits and terminal cleanup.
"""
import sys
from .maze_generator import MazeGenerator
from .pallete import Themes
from .maze_sotore import MazeDataBase
from .import supress_terminal_echos

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
        import tty
        import termios
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

    @supress_terminal_echos
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
        if self.maze.solved:
            self.maze.show_solve_path()

    def clean_screen(self) -> None:
        """
        Cleans the screen using Anscii codes
        # 1. ANSI Cleanup Sequence
        \033[0m       -> Reset all text colors to terminal default
        \033[?25h     -> Un-hide the cursor
        \033[?1049l   -> Close the "Alternate Screen" buffer
        """
        from os import system, name
        import time
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
        time.sleep(0.7)

    @supress_terminal_echos
    def generate_new_maze(self) -> None:
        """
        Generates a new maze reseting the grid to make it
        a solid brick and call the same algorithm to genarate
        it whith differnt seed
        """
        self.maze.reset_grid()
        self.maze.generate_maze()
        MazeDataBase(maze=self.maze).export_maze_txt(self.maze.grid)

    def change_alorithm(self) -> None:
        """
        Choose a new algorithm to create a new maze with
        it
        """
        from Algor.all_algo import ALGORITHM_REGISTRY
        available_algos = [
            key for key, meta in ALGORITHM_REGISTRY.items()
            if key != self.maze.algo_name and meta.job == "construct"
        ]
        if available_algos:
            self.maze.algo_name = available_algos[0]
        self.generate_new_maze()

    @supress_terminal_echos
    def run(self) -> None:
        """
        Executes the main interactive terminal menu loop for the application.
        Initializes the visual state by carving the protected pattern, drawing
        the ASCII grid, and rendering the HUD. It then enters an infinite loop
        that displays a dynamically centered, interactive horizontal menu
        directly beneath the maze's Viewport.
        The loop captures raw, unbuffered keystrokes ('1'-'5' to change the
        active selection, 'Enter' to execute) to allow real-time UI navigation.
        Terminal echoing is suppressed to ensure keystrokes do not corrupt the
        ASCII rendering. The loop continuously re-renders the menu state and
        breaks only when the 'Exit' action is executed.
        """
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
                'func': lambda: self.maze.toogle_solve_path()
            },
            {
                'txt': "3: Change Theme",
                'func': lambda: self.get_random_theme()
            },
            {
                'txt': "4: Change Algorithm",
                'func': lambda: self.change_alorithm()
            },
            {
                'txt': "5: Exit",
                'func': lambda: self.clean_screen()
            }
        ]
        select_indx = 0
        while True:
            menu_y = (self.maze.viewport.offset_y
                      + self.maze.viewport.height + 1)
            # 1. Prepare empty strings to build the menu
            clean_menu_text = ""
            colored_menu_text = ""
            # 2. Build the full strings piece-by-piece
            for i, opt in enumerate(menu_options):
                # (This also checks if you used the lambda trick for
                # dynamic text!)
                display_text = (opt['txt']() if callable(opt['txt'])
                                else opt['txt'])
                if i == select_indx:
                    color = self.maze.active_theme.get_color('logo')
                    clean_menu_text += f" > {display_text}   "
                    colored_menu_text += f"{color}\033[1;30m > \
{display_text} \033[0m  "
                else:
                    clean_menu_text += f"   {display_text}    "
                    colored_menu_text += f"   {display_text}    "
            # 3. Calculate the perfect center using the Viewport math
            visible_length = len(clean_menu_text)
            center_x = (self.maze.viewport.offset_x +
                        (self.maze.viewport.width // 2) -
                        (visible_length // 2))
            # 4. Safety boundary: Don't fall off the left side of the terminal
            center_x = max(1, center_x)
            # 5. Clear the entire row (\033[2K), jump to the center, and print!
            print(f"\033[{menu_y};1H\033[2K\033[{menu_y};{center_x}H\
{colored_menu_text}", end="")
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
                case '5':
                    select_indx = 4
                case ('\r' | '\n'):
                    action = menu_options[select_indx]['func']
                    if callable(action):
                        action()
                    if menu_options[select_indx]['txt'] == '5: Exit':
                        break
