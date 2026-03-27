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
PATTERN = ["1001 1111",
           "1001 0001", 
           "1111 1111", 
           "0001 1000", 
           "0001 1111"]


class MazeConfig(BaseModel):
    width: int = Field(..., gt=0, description="width must be > 0")
    height: int = Field(..., gt=0, description="height must be > 0")
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    perfect: bool = Field(...)


@dataclass
class Cell:
    x_value: int
    y_value: int
    value: int = 15
    is_fortytwo: bool = False

    def get_render_strings(self) -> Tuple[str, str]:
        # \033[42m = Bright Green BG | \033[100m = Dark Grey BG | \033[0m = 
        # Default BG
        wall_bg = "\033[42m" if self.is_fortytwo else "\033[100m"
        reset = "\033[0m"

        # SYMMETRIC SQUARES: Everything is exactly 2 spaces wide!
        corner = f"{wall_bg}  {reset}"
        north = f"{wall_bg}  {reset}" if (self.value & 1) else "  "
        west = f"{wall_bg}  {reset}" if (self.value & 8) else "  "
        center = f"{wall_bg}  {reset}" if self.value == 15 else "  "

        top = f"{corner}{north}"
        mid = f"{west}{center}"
        return top, mid


class MazeGenerator:
    def __init__(self, maze_config: MazeConfig) -> None:
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        
        # 1. Define these BEFORE calling clamp_dimensions!
        self.entry = maze_config.entry
        self.exit = maze_config.exit
        
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 130, 40

        # Make the box relative to the window!
        # Subtracting 8 columns and 4 lines gives a perfect
        # padding around the outside of the box.
        # We use max() just in case the user shrinks the window to a tiny square.
        self.box_width = max(50, term_col - 12)
        self.box_height = max(20, term_lines - 5)
        # 3. NOW we can safely clamp everything
        self.clamp_dimensions()

        # 4. Build the grid
        self.grid: List[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()
        self.offset_x = 1
        self.offset_y = 1
        self.box_offset_x = 1
        self.box_offset_y = 1
    def clamp_dimensions(self) -> None:
        # We NO LONGER care about the terminal size here!
        # The maximum size the maze can be to fit INSIDE our fixed 100x30 box:
        # We subtract 4 to leave a 2-character padding inside the box borders.
        max_w = (self.box_width - 4) // 4
        max_h = (self.box_height - 4) // 2

        # Force the dimensions to be within the box's strict limits!
        self.width = max(11, min(self.width, max_w))
        self.height = max(7, min(self.height, max_h))

        # Force entry and exit to stay inside the newly clamped bounds!
        safe_entry_x = min(self.entry[0], self.width - 1)
        safe_entry_y = min(self.entry[1], self.height - 1)
        self.entry = (safe_entry_x, safe_entry_y)

        safe_exit_x = min(self.exit[0], self.width - 1)
        safe_exit_y = min(self.exit[1], self.height - 1)
        self.exit = (safe_exit_x, safe_exit_y)

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
            term_col, term_lines = 130, 40

        # 1. Center the FIXED BOX on the terminal screen
        self.box_offset_x = max(1, (term_col - self.box_width) // 2)
        self.box_offset_y = max(1, (term_lines - self.box_height) // 2)

        # 2. Center the MAZE inside the FIXED BOX
        maze_pixel_w = (self.width * 4) + 2
        maze_pixel_h = (self.height * 2) + 1
        self.offset_x = self.box_offset_x + (self.box_width - maze_pixel_w) // 2
        self.offset_y = self.box_offset_y + (self.box_height - maze_pixel_h) // 2

        os.system("cls" if os.name == "nt" else "clear")
        print("\033[?1049h\033[2J\033[?25l", end="")

        # --- DRAW THE FIXED UI BOUNDING BOX ---
        border_color = "\033[90m" 
        reset = "\033[0m"
        
        # Calculate the top and bottom lines using the fixed box width
        top_border = f"{border_color}╭" + ("─" * (self.box_width - 2)) + f"╮{reset}"
        bottom_border = f"{border_color}╰" + ("─" * (self.box_width - 2)) + f"╯{reset}"
        
        # Draw Top
        print(f"\033[{self.box_offset_y};{self.box_offset_x}H{top_border}")
        
        # Draw Sides (using the fixed box height)
        for i in range(1, self.box_height - 1):
            print(f"\033[{self.box_offset_y + i};{self.box_offset_x}H{border_color}│{reset}")
            print(f"\033[{self.box_offset_y + i};{self.box_offset_x + self.box_width - 1}H{border_color}│{reset}")
            
        # Draw Bottom
        print(f"\033[{self.box_offset_y + self.box_height - 1};{self.box_offset_x}H{bottom_border}")
        sys.stdout.flush()
        # -------------------------------------

        output = ""
        for y in range(self.height):
            top_row, mid_row = "", ""
            for x in range(self.width):
                cell = self.grid[y][x]
                top, mid = cell.get_render_strings()
                top_row += top
                mid_row += mid

                if x == self.width - 1:
                    wall_bg = "\033[42m" if cell.is_fortytwo else "\033[100m"
                    reset = "\033[0m"
                    east = f"{wall_bg}  {reset}" if (cell.value & 2) else "  "
                    top_row += f"{wall_bg}  {reset}"
                    mid_row += east

            output += f"\033[{self.offset_y + (y * 2)};{self.offset_x}H{top_row}"
            output += f"\033[{self.offset_y + (y * 2) + 1};{self.offset_x}H{mid_row}"

        boot_row = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            wall_bg = "\033[42m" if cell.is_fortytwo else "\033[100m"
            reset = "\033[0m"
            south = f"{wall_bg}  {reset}" if (cell.value & 4) else "  "
            boot_row += f"{wall_bg}  {reset}{south}"

        last_cell = self.grid[self.height - 1][self.width - 1]
        last_wall_bg = "\033[42m" if last_cell.is_fortytwo else "\033[100m"

        output += f"\033[{self.offset_y + (self.height * 2)};{self.offset_x}H{boot_row}{last_wall_bg}  \033[0m"
        print(output, end="", flush=True)

    def animated_frame(self, cell1: Cell, cell2: Cell) -> None:
        for cell in [cell1, cell2]:
            top, middle = cell.get_render_strings()
            cx = self.offset_x + (cell.x_value * 4)
            cy = self.offset_y + (cell.y_value * 2)
            print(f"\033[{cy};{cx}H{top}", end="")
            print(f"\033[{cy + 1};{cx}H{middle}", end="")
        sys.stdout.flush()
        time.sleep(0.015)  # Sped up slightly for the bigger maze!

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

        maze_config = MazeConfig(
            width=30, height=30, entry=(0, 0), exit=(29, 29), perfect=True
        )
        maze = MazeGenerator(maze_config)
        maze.generate_maze(starr_coord=maze.entry)

    except KeyboardInterrupt:
        # Safely restore terminal settings if user hits Ctrl+C
        print("\033[7h\033[?25h\n\nAnimation stopped by user. Exiting gracefully.")
