"""The core Maze Generator Engine.
Combines configuration, UI scaling, matrix construction,
and rendering animation into a single responsive terminal
application.
"""
from Algor.all_algo import ALGORITHM_REGISTRY
from . import supress_terminal_echos
from .viewport import Viewport
from .helper_maze_classes import Cell, MazeConfig
from typing import Tuple, List, Set, Optional, Union
import os
import sys
import time
from datetime import datetime
import random

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
        self.seed = (maze_config.seed if maze_config.seed
                     else random.randint(0, 9999))
        self.rgn = random.Random(self.seed)
        self.date = datetime.now().strftime('%H:%M:%S')
        self.path = ""
        self.solved = False
        self.decouple = maze_config.decouple_entry
        self.perfect = maze_config.perfect
        self.algo_name = maze_config.algorithm
        self._pattern_warning_shown = False

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
            if not self._pattern_warning_shown:
                print("\033[33m[Warning] Maze is too small to carve the '42'"
                      "pattern. Skipping...\033[0m", end="", flush=True)
                time.sleep(1.5)
                self._pattern_warning_shown = True
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
        os.system("clear")
        print("\033[2J\033[?25l", end="")
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
        A callback function triggered by Algorithm's to draw walls
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
            time.sleep(0.004)

    def _handle_imperfect_mazes(self) -> None:
        """
        Converts a perfect maze into an imperfect 'braided' maze.
        If the configuration specifies an imperfect maze (PERFECT=false),
        this method scans the grid to identify "dead ends"
        (cells enclosed by exactly three walls).
        It then randomly selects a subset of these dead ends (20%)
        and smashes an adjacent solid wall to connect them to a
        neighboring cell.
        This process creates loops and alternate routes while strictly avoiding
        breaches to the absolute outer boundaries or the protected '42'.
        """
        if not self.config.perfect:
            from Algor import DIRECTIONS
            # Step A: Find all the "Dead Ends" in the maze
            # In your bitmask math, dead ends have values: 7, 11, 13, 14
            dead_ends = []
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    cell = self.grid[y][x]
                    if cell.value in (7, 11, 13, 14) and not cell.is_fortytwo:
                        dead_ends.append(cell)
            # Step B: Pick how many dead ends to connect
            # (Connecting ~50% of them creates a fantastic, loopy maze)
            loops_to_make = len(dead_ends) // 5
            self.rgn.shuffle(dead_ends)
            # Step C: Smash a wall to connect the dead end to a neighbor
            for i in range(min(loops_to_make, len(dead_ends))):
                cell1 = dead_ends[i]
                # Look at all 4 directions to find
                # which walls are currently SOLID
                solid_walls = []
                for dx, dy, bit, opp in DIRECTIONS:
                    # If this bit is still 1, the wall is solid
                    if (cell1.value & bit):
                        nx, ny = cell1.x_value + dx, cell1.y_value + dy
                        # Make sure we don't accidentally break
                        # the absolute outer border!
                        if (0 < nx < self.width - 1 and
                                0 < ny < self.height - 1):
                            cell2 = self.grid[ny][nx]
                            if not cell2.is_fortytwo:
                                solid_walls.append((cell2, bit, opp))
                # Pick a random solid wall and smash it!
                if solid_walls:
                    cell2, bit, opp = self.rgn.choice(solid_walls)
                    cell1.value &= ~bit
                    cell2.value &= ~opp
                    self.animated_frame(cell1, cell2)

    @supress_terminal_echos
    def generate_maze(self) -> None:
        """
        The main execution pipeline for the maze generator.
        Carves the pattern, renders the UI, and initiates the
        pathfinding algorithm. Locks the terminal process until
        the user acknowledges completion.
        Args:
            starr_coord (Tuple[int, int]): The (x, y) coordinate
            indicating where the generation algorithm should begin digging.
        """
        try:
            start_point = self.entry if self.decouple else (0, 0)
            algorithm = ALGORITHM_REGISTRY[self.algo_name]
            solve_maze = ALGORITHM_REGISTRY['BFS']
            self.carve_42_pattern()
            self.draw_ascii_grid()
            self.draw_stats_hud()
            algorithm.func(
                grid=self.grid,
                width=self.width,
                height=self.height,
                start_coord=start_point,
                protected=self.protected_cells,
                on_step=self.animated_frame,
                rng=self.rgn
            )
            self.path = solve_maze.func(
                grid=self.grid,
                width=self.width,
                height=self.height,
                entry=self.entry,
                exit=self.exit,
            )
            if not self.perfect:
                self._handle_imperfect_mazes()
        except Exception as e:
            print(e)

    def draw_stats_hud(self) -> None:
        """
        Renders a real-time statistics Heads-Up Display (HUD) above the maze.
        Constructs an ANSI color-coded string displaying the current maze
        dimensions, the active pathfinding algorithm (Prim's), and the
        currently selected theme. It dynamically calculates the correct
        terminal coordinates to print this information exactly one row
        above the top-left corner of the Viewport.
        Returns:
            None
        """
        hud_y = self.viewport.offset_y - 1
        theme_name = self.active_theme.name
        algo = ALGORITHM_REGISTRY[self.algo_name]
        # 1. Build a "clean" version with NO colors just to
        # measure the true visible length
        clean_text = (
            f"[ Size: {self.width}x{self.height} | "
            f"Algo: {algo.name} | "
            f"Theme: {theme_name} | "
            # Formatting the date to just HH:MM:SS makes the HUD much cleaner!
            f"Date: {self.date} | "
            f"SEED: {self.seed} | "
            f"DECOUPLE: {self.decouple} | "
            f"Perfect: {self.perfect} ]"
        )
        # 2. Build the actual colored string
        hud_text = (
            f"\033[1;90m[\033[0m "
            f"\033[1;97mSize: \033[92m{self.width}x{self.height}\033[0m | "
            f"\033[1;97mAlgo: \033[92m{algo.name}\033[0m | "
            f"\033[1;97mTheme: \033[92m{theme_name}\033[0m | "
            f"\033[1;97mDate: \033[92m{self.date}\033[0m |"
            f"\033[1;97mSEED: \033[92m{self.seed}\033[0m | "
            f"\033[1;97mDECOUPLE: \033[92m{self.decouple}\033[0m | "
            f"\033[1;97mPerfect: \033[92m{self.perfect}\033[0m "
            "\033[1;90m]\033[0m"
        )
        # 3. Calculate the perfect center X coordinate
        visible_length = len(clean_text)
        center_x = (self.viewport.offset_x +
                    (self.viewport.width // 2) - (visible_length // 2))
        # Safety check: Ensure we don't accidentally push it off the
        # left edge of the box
        center_x = max(1, center_x)
        # 4. First, clear the entire row above the maze (\033[K at the offset)
        print(f"\033[{hud_y};{self.viewport.offset_x}H\033[K", end="")
        # 5. Then, jump to the perfectly centered coordinate and
        # print the colored HUD!
        print(f"\033[{hud_y};{center_x}H{hud_text}", end="", flush=True)

    def reset_grid(self) -> None:
        """
        Only resets the value of each cell in the grid so it
        becomes a new complete grid so its possible to crate
        a completly new maze after the grid is generate
        """
        for row in self.grid:
            for cell in row:
                cell.value = 15
        self.seed = random.randint(0, 9999)
        self.rgn = random.Random(self.seed)
        self.date = datetime.now().strftime('%H:%M:%S')
        self.solved = False

    def decode_path(self) -> List[Tuple[int, int]]:
        """
        Translates the maze solution that is a string
        to a list of tupples that are coord in the grid
        of the maze
        """
        from . import DIRECTION_DELTAS
        if self.path == 'UNSOLVABLE':
            return []
        current_x, current_y = self.entry
        path_coord = [self.entry]
        for letter in self.path:
            dx, dy = DIRECTION_DELTAS[letter]
            current_x += dx
            current_y += dy
            path_coord.append((current_x, current_y))
        return path_coord

    def toogle_solve_path(self) -> None:
        """
        Toggles the terminal visibility of the maze's shortest solution path.
        If the path is currently displayed, it clears it by redrawing the base
        ASCII grid. If the path is hidden, it triggers the path animation.
        """
        if self.solved:
            self.draw_ascii_grid()
            self.draw_stats_hud()
        else:
            self.show_solve_path(value=0.03)
        self.solved = not self.solved

    @supress_terminal_echos
    def show_solve_path(self, value: Optional[Union[int, float]] = 0) -> None:
        """
        Animates the shortest path from the entry to the exit on the terminal.
        Uses the decoded coordinate list to draw custom colored ANSI blocks
        ("bridges") between cells to visually represent the solution.
        Args:
            value (Optional[Union[int, float]]): The delay in seconds between
            drawing each path segment, creating an animation effect. Defaults
            to 0 (instant rendering).
        """
        path_coord = self.decode_path()
        if not path_coord:
            print(f"{self.active_theme.get_color('logo')}\
[Cannot solve this maze...]\033[0m")
            self.solved = False
            return

        PATH_CHAR = "  "
        color_on = self.active_theme.get_color('logo')
        color_off = self.active_theme.get_color('none')
        # 1. Draw the very first room (The Entry)
        curr_x, curr_y = path_coord[0]
        cx = self.offset_x + (curr_x * 4)
        cy = self.offset_y + (curr_y * 2)
        time.sleep(0.05)
        for letter, (next_x, next_y) in zip(self.path, path_coord[1:]):
            if letter == 'E':
                bridge_x, bridge_y = cx + 4, cy + 1
            elif letter == 'W':
                bridge_x, bridge_y = cx, cy + 1
            elif letter == 'S':
                bridge_x, bridge_y = cx + 2, cy + 2
            elif letter == 'N':
                bridge_x, bridge_y = cx + 2, cy
            time.sleep(value or 0)
            print(f"\033[{bridge_y};{bridge_x}H{color_on}\
{PATH_CHAR}{color_off}", end="", flush=True)
            cx = self.offset_x + (next_x * 4)
            cy = self.offset_y + (next_y * 2)
            time.sleep(value or 0)
            if (next_x, next_y) != self.exit:
                print(f"\033[{cy + 1};{cx + 2}H{color_on}\
{PATH_CHAR}{color_off}", end="", flush=True)
        time.sleep(0.05)
        final_y = self.offset_y + (self.height * 2) + 2
        print(f"\033[{final_y};0H")
