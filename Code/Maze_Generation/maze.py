from pydantic import BaseModel, Field
from typing import Tuple, List, Set
import os
import sys
import time
from Algor.prims import prims_algorithm
from dataclasses import dataclass

N = 1  # 0001
E = 2  # 0010
S = 4  # 0100
W = 8  # 1000
PATTERN = ["1001 1111", "1001 0001", "1111 1111", "0001 1000", "0001 1111"]


class MazeConfig(BaseModel):
    width: int = Field(..., gt=0, description="width must be > 0")
    height: int = Field(..., gt=0, description="height must be > 0")
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    perfect: bool = Field(
        ...,
    )

@dataclass
class Cell:
    x_value: int
    y_value: int
    value: int = 15
    is_fortytwo: bool = False

    def get_render_strings(self) -> Tuple[str, str]:
        # \033[92m = Green Text | \033[90m = Dark Grey Text
        text_color = "\033[92m" if self.is_fortytwo else "\033[90m"
        reset = "\033[0m"

        # upgraded "Font": Sleek Unicode Box Drawing Characters
        corner = "╋"
        north = "━━━" if (self.value & 1) else "   "
        west = "┃" if (self.value & 8) else " "
        
        # If this cell is the 42, fill the inside with a solid block!
        if self.is_fortytwo:
            center = "███"
        else:
            center = "   " # Normal maze paths stay empty

        top = f"{text_color}{corner}{north}{reset}"
        mid = f"{text_color}{west}{center}{reset}"
        return top, mid
"""
TODO : PARSER AND THE READ OF THE config file
and the error handling and more animation
"""


class MazeGenerator:
    """ """

    def __init__(self, maze_config: MazeConfig) -> None:
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        self.grid: List[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()
        # Terminal rendering offsets
        self.offset_x = 1
        self.offset_y = 1

    def carve_42_pattern(self) -> None:
        width_patt = len(PATTERN[0])
        height_patt = len(PATTERN)
        x_start = (self.width // 2) - (width_patt // 2)
        y_start = (self.height // 2) - (height_patt // 2)
        for dy, row in enumerate(PATTERN):
            for dx, char in enumerate(row):
                if char == "1":
                    coord_x = x_start + dx
                    coord_y = y_start + dy
                    self.protected_cells.add((coord_x, coord_y))
                    self.grid[coord_y][coord_x].is_fortytwo = True

    def draw_ascii_grid(self) -> None:
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 80, 24

        maze_w = (self.width * 4) + 1
        maze_h = (self.height * 2) + 1

        self.offset_x = max(1, (term_col - maze_w) // 2)
        self.offset_y = max(1, (term_lines - maze_h) // 2)

        os.system("cls" if os.name == "nt" else "clear")
        print("\033[2J\033[7l\033[?25l", end="")

        output = ""
        for y in range(self.height):
            top_row, mid_row = "", ""
            for x in range(self.width):
                cell = self.grid[y][x]
                top, mid = cell.get_render_strings()
                top_row += top
                mid_row += mid

                # The East Boundary (Updated to Unicode ┃ and ╋)
                if x == self.width - 1:
                    text_color = "\033[92m" if cell.is_fortytwo else "\033[90m"
                    reset = "\033[0m"
                    east = "┃" if (cell.value & 2) else " "
                    top_row += f"{text_color}╋{reset}"
                    mid_row += f"{text_color}{east}{reset}"

            output += f"\033[{self.offset_y + (y * 2)};{self.offset_x}H{top_row}"
            output += f"\033[{self.offset_y + (y * 2) + 1};{self.offset_x}H{mid_row}"

        # The South Boundary (Updated to Unicode ━━━ and ╋)
        boot_row = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            text_color = "\033[92m" if cell.is_fortytwo else "\033[90m"
            reset = "\033[0m"
            south = "━━━" if (cell.value & 4) else "   "
            boot_row += f"{text_color}╋{south}{reset}"

        # The final bottom-right corner
        last_cell = self.grid[self.height - 1][self.width - 1]
        last_text_color = "\033[92m" if last_cell.is_fortytwo else "\033[90m"

        output += f"\033[{self.offset_y + (self.height * 2)};{self.offset_x}H{boot_row}{last_text_color}╋{reset}"
        print(output, end="", flush=True)

    def animated_frame(self, cell1: Cell, cell2: Cell) -> None:
        for cell in [cell1, cell2]:
            top, middle = cell.get_render_strings()
            cx = self.offset_x + (cell.x_value * 4)
            cy = self.offset_y + (cell.y_value * 2)
            print(f"\033[{cy};{cx}H{top}", end="")
            print(f"\033[{cy + 1};{cx}H{middle}", end="")
        sys.stdout.flush()
        time.sleep(0.02)

    def generate_maze(self, starr_coord: Tuple[int, int]) -> None:
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

        end_y = self.offset_y + (self.height * 2) + 2

        # RESTORE line wrap (\033[7h) and SHOW cursor (\033[?25h) so the terminal goes back to normal!
        print(f"\033[{end_y};0H\033[7h\033[?25h")
        print("\n\nMaze Generation Complete!!\n")


if __name__ == "__main__":
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)

        # Pydantic loves keyword arguments!
        # Pass actual tuples (x, y) for entry and exit.
        maze_config = MazeConfig(
            width=30, height=20, entry=(0, 0), exit=(0, 0), perfect=True
        )
        # Instantiate your generator with the config
        maze = MazeGenerator(maze_config)
        # Start carving! (using your exact method name)
        maze.generate_maze(starr_coord=maze_config.entry)
    except KeyboardInterrupt:
        # Safely restore terminal settings if user hits Ctrl+C
        print("\033[7h\033[?25h\n\nAnimation stopped by user. Exiting gracefully.")
