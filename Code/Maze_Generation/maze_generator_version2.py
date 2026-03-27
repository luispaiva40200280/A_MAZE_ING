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
        black_bg = "\033[40m" # The open path
        cyan_bg = "\033[46m"  # The solid wall
        reset = "\033[0m"

        # The room itself (Black for paths, Bright Green for the 42)
        room_color = "\033[42m" if self.is_fortytwo else black_bg
        center = f"{room_color}  {reset}"

        # The corners are always solid walls (Cyan)
        corner = f"{cyan_bg}  {reset}"

        # The walls: If closed, they are Cyan. If broken, they become the Black path!
        north = f"{cyan_bg}  {reset}" if (self.value & 1) else center
        west = f"{cyan_bg}  {reset}" if (self.value & 8) else center

        top = f"{corner}{north}"
        mid = f"{west}{center}"
        return top, mid


class MazeGenerator:
    def __init__(self, maze_config: MazeConfig) -> None:
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        
        self.entry = maze_config.entry
        self.exit = maze_config.exit

        # --- RESPONSIVE VIEWPORT SIZE ---
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 130, 40 

        # Make the box relative to the terminal window
        self.box_width = max(50, term_col - 8) 
        self.box_height = max(20, term_lines - 4) 
        
        self.clamp_dimensions()

        self.grid: List[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()
        self.offset_x = 1
        self.offset_y = 1
        self.box_offset_x = 1
        self.box_offset_y = 1

    def clamp_dimensions(self) -> None:
        # Calculate max maze size based on the BOX size, not terminal size
        max_w = (self.box_width - 4) // 4
        max_h = (self.box_height - 4) // 2

        # Force the dimensions to be within safe bounds
        self.width = max(11, min(self.width, max_w))
        self.height = max(7, min(self.height, max_h))

        # Clamp entry and exit points to stay inside the newly sized grid
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

        # Center the FIXED BOX on the terminal screen
        self.box_offset_x = max(1, (term_col - self.box_width) // 2)
        self.box_offset_y = max(1, (term_lines - self.box_height) // 2)

        # Center the MAZE inside the FIXED BOX
        maze_pixel_w = (self.width * 4) + 2
        maze_pixel_h = (self.height * 2) + 1
        self.offset_x = self.box_offset_x + (self.box_width - maze_pixel_w) // 2
        self.offset_y = self.box_offset_y + (self.box_height - maze_pixel_h) // 2

        os.system("cls" if os.name == "nt" else "clear")
        
        # Enter Alternate Screen Buffer, clear screen, hide cursor
        print("\033[?1049h\033[2J\033[?25l", end="")

        # --- DRAW THE UI BOUNDING BOX ---
        border_color = "\033[90m" 
        reset = "\033[0m"
        
        top_border = f"{border_color}╭" + ("─" * (self.box_width - 2)) + f"╮{reset}"
        bottom_border = f"{border_color}╰" + ("─" * (self.box_width - 2)) + f"╯{reset}"
        
        print(f"\033[{self.box_offset_y};{self.box_offset_x}H{top_border}")
        for i in range(1, self.box_height - 1):
            print(f"\033[{self.box_offset_y + i};{self.box_offset_x}H{border_color}│{reset}")
            print(f"\033[{self.box_offset_y + i};{self.box_offset_x + self.box_width - 1}H{border_color}│{reset}")
        print(f"\033[{self.box_offset_y + self.box_height - 1};{self.box_offset_x}H{bottom_border}")
        sys.stdout.flush()

        # --- THE CELL-BY-CELL GENERATION ANIMATION ---
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                top, mid = cell.get_render_strings()
                
                cx = self.offset_x + (x * 4)
                cy = self.offset_y + (y * 2)
                
                print(f"\033[{cy};{cx}H{top}", end="")
                print(f"\033[{cy + 1};{cx}H{mid}", end="")
                
                # East boundary wall (Cyan)
                if x == self.width - 1:
                    wall_bg = "\033[46m" 
                    east = f"{wall_bg}  {reset}"
                    print(f"\033[{cy};{cx + 4}H{wall_bg}  {reset}", end="")
                    print(f"\033[{cy + 1};{cx + 4}H{east}", end="")

                sys.stdout.flush()
                time.sleep(0.002) # Matrix-style drawing delay

        # South boundary wall (Cyan)
        boot_row = ""
        for x in range(self.width):
            boot_row += f"\033[46m  \033[0m\033[46m  \033[0m"
            
        print(f"\033[{self.offset_y + (self.height * 2)};{self.offset_x}H{boot_row}\033[46m  \033[0m", end="")
        sys.stdout.flush()
        time.sleep(0.5)

    def animated_frame(self, cell1: Cell, cell2: Cell) -> None:
        # Snap render just the updated cells
        for cell in [cell1, cell2]:
            top, middle = cell.get_render_strings()
            cx = self.offset_x + (cell.x_value * 4)
            cy = self.offset_y + (cell.y_value * 2)
            print(f"\033[{cy};{cx}H{top}", end="")
            print(f"\033[{cy + 1};{cx}H{middle}", end="")
        sys.stdout.flush()
        time.sleep(0.015) 

    def generate_maze(self) -> None:
        self.carve_42_pattern()
        self.draw_ascii_grid()

        prims_algorithm(
            grid=self.grid,
            width=self.width,
            height=self.height,
            start_coord=self.entry,
            protected=self.protected_cells,
            on_step=self.animated_frame,
        )
        
        time.sleep(1.5)
        # Exit Alternate Buffer and show cursor
        print("\033[?1049l\033[?25h", end="")
        print("\nMaze Generation Complete!!\n")


if __name__ == "__main__":
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)

        maze_config = MazeConfig(
            width=50, height=50, entry=(20, 20), exit=(49, 0), perfect=True
        )
        maze = MazeGenerator(maze_config)
        maze.generate_maze() # Passes no arguments since we saved entry to `self`!

    except KeyboardInterrupt:
        # Safely restore terminal settings if user hits Ctrl+C
        print("\033[?1049l\033[7h\033[?25h\n\nAnimation stopped by user. Exiting gracefully.")