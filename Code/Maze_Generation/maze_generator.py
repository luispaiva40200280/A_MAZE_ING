"""The core Maze Generator Engine.
Combines configuration, UI scaling, matrix construction,
and rendering animation into a single responsive terminal
application.
"""
from Algor.prims import prims_algorithm
from .viewport import Viewport
from .helper_maze_classes import Cell, MazeConfig
from typing import Tuple, List, Set
import os
import sys
import time

"""bitmap for 42"""
PATTERN = ["101 111",
           "101 001",
           "111 111",
           "001 100",
           "001 111"]


class MazeGenerator:
    """
    Orchestrates the creation, logic, and rendering of the maze.
    Attributes:
        config (MazeConfig): The verified configuration settings.
        width (int): The finalized, safely clamped width of the maze.
        height (int): The finalized, safely clamped height of the maze.
        entry (Tuple[int, int]): Safe (x, y) coordinates for the start of the
        maze.
        exit (Tuple[int, int]): Safe (x, y) coordinates for the end of the
        maze.
        viewport (Viewport): The bounding box UI and terminal math handler.
        grid (List[list[Cell]]): A 2D matrix containing the maze Cell objects.
        protected_cells (Set[Tuple[int, int]]): Coordinates of cells that
        generation algorithms cannot alter.
    """
    def __init__(self, maze_config: MazeConfig) -> None:
        from .pallete import Themes
        """
        Initializes the generator pipeline. Calculates dynamic sizing, builds
        the grid data structure, and prepares for algorithm execution.
        Args:
            maze_config (MazeConfig): Validated configuration parameters.
        """
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        self.entry = maze_config.entry
        self.exit = maze_config.exit
        self.viewport = Viewport(self.width, self.height)
        self.calculate_offsets()
        self.grid: List[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()
        self.active_theme: Themes = maze_config.theme
        self.grid[self.entry[1]][self.entry[0]].is_entry = True
        self.grid[self.exit[1]][self.exit[0]].is_exit = True

    def calculate_offsets(self) -> None:
        """
        Calculates the exact terminal cursor coordinates required to perfectly
        center the physical maze structure inside of the dynamically drawn
        Viewport UI.
        """
        maze_pixel_w = (self.width * 4) + 2
        maze_pixel_h = (self.height * 2) + 1

        self.viewport.width = maze_pixel_w + 4
        self.viewport.height = maze_pixel_h + 2

        self.offset_x = self.viewport.offset_x + 2
        self.offset_y = self.viewport.offset_y + 1

    def carve_42_pattern(self) -> None:
        """
        Injects the hardcoded '42' pattern into the center of the maze grid.
        Flags affected cells as 'protected' so pathfinding algorithms route
        around them instead of destroying the pattern.
        """
        width_patt = len(PATTERN[0])
        height_patt = len(PATTERN)
        x_start = (self.width // 2) - (width_patt // 2)
        y_start = (self.height // 2) - (height_patt // 2)
        # Add a small buffer (e.g., +4) so the pattern isn't
        # touching the outer walls
        if self.width < (width_patt + 4) or self.height < (height_patt + 4):
            # The maze is too small! Gracefully exit without carving anything.
            return
        for dy, row in enumerate(PATTERN):
            for dx, char in enumerate(row):
                if char == "1":
                    coord_x = x_start + dx
                    coord_y = y_start + dy
                    self.protected_cells.add((coord_x, coord_y))
                    self.grid[coord_y][coord_x].is_fortytwo = True

    def draw_ascii_grid(self) -> None:
        """
        Renders the initial closed-grid state of the maze to the terminal.
        Prepares the alternate screen buffer, hides the cursor, draws the
        bounding Viewport, and paints every closed cell block-by-block
        using the active Theme colors.
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("\033[?1049h\033[2J\033[?25l", end="")
        self.viewport.draw()

        # 1. Extract the active theme colors
        wall_color = self.active_theme.get_color("walls")
        logo_color = self.active_theme.get_color("logo")
        path_color = self.active_theme.get_color("path")
        ansi_reset = "\033[0m"

        output = ""
        for y in range(self.height):
            top_row, mid_row = "", ""
            for x in range(self.width):
                cell = self.grid[y][x]
                # The cell already knows how to use the theme!
                top, mid = cell.get_render_strings(self.active_theme)
                top_row += top
                mid_row += mid
                # 2. Refactor the East wall (right-most edge)
                if x == self.width - 1:
                    wall_bg = logo_color if cell.is_fortytwo else wall_color
                    # Use the theme's path color instead of empty spaces
                    east = (f"{wall_bg}  {ansi_reset}" if (cell.value & 2)
                            else f"{path_color}  {ansi_reset}")
                    top_row += f"{wall_bg}  {ansi_reset}"
                    mid_row += east

            output += f"\033[{self.offset_y + (y * 2)};{self.offset_x}\
H{top_row}"
            output += f"\033[{self.offset_y + (y * 2) + 1};{self.offset_x}\
H{mid_row}"

        boot_row = ""
        # 3. Refactor the South wall (bottom-most edge)
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            wall_bg = logo_color if cell.is_fortytwo else wall_color
            south = (f"{wall_bg}  {ansi_reset}" if (cell.value & 4)
                     else f"{path_color}  {ansi_reset}")
            boot_row += f"{wall_bg}  {ansi_reset}{south}"
        # 4. Refactor the final bottom-right corner block
        last_cell = self.grid[self.height - 1][self.width - 1]
        last_wall_bg = logo_color if last_cell.is_fortytwo else wall_color

        output += f"\033[{self.offset_y + (self.height * 2)};{self.offset_x}\
H{boot_row}{last_wall_bg}  {ansi_reset}"

        print(output, end="", flush=True)

    def animated_frame(self, cell1: Cell, cell2: Cell) -> None:
        """
        A callback function triggered by Prim's Algorithm to draw walls
        breaking in real-time. Applies a 'tweening' animation sequence
        to simulate walls dissolving into dust.
        Args:
            cell1 (Cell): The parent cell being extended from.
            cell2 (Cell): The newly carved neighbor cell.
        """
        dust_stages = ["▓▓", "▒▒", "░░", "  "]

        for dust in dust_stages:
            for cell in [cell1, cell2]:
                top, middle = cell.get_render_strings(self.active_theme, dust)
                cx = self.offset_x + (cell.x_value * 4)
                cy = self.offset_y + (cell.y_value * 2)
                print(f"\033[{cy};{cx}H{top}", end="")
                print(f"\033[{cy + 1};{cx}H{middle}", end="")
            sys.stdout.flush()
            time.sleep(0.002)

    def generate_maze(self, starr_coord: Tuple[int, int]) -> None:
        """
        The main execution pipeline for the maze generator.
        Carves the pattern, renders the UI, and initiates the
        pathfinding algorithm. Locks the terminal process until
        the user acknowledges completion.
        Args:
            starr_coord (Tuple[int, int]): The (x, y) coordinate
            indicating where the generation algorithm should begin digging.
        """
        self.carve_42_pattern()
        self.draw_ascii_grid()
        prims_algorithm(
            grid=self.grid,
            width=self.width,
            height=self.height,
            start_coord=starr_coord,
            protected=self.protected_cells,
            on_step=self.animated_frame,
        )
        end_y = self.viewport.offset_y + self.viewport.height
        msg = ("\033[92m ╰─▶ Generation Complete! Press \
[ENTER] to exit...\033[0m")
        print(f"\033[{end_y};{self.viewport.offset_x}H{msg}",
              end="", flush=True)
        input()
        print("\033[?1049l\033[?25h", end="")
