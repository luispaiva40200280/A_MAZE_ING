from Algor.prims import prims_algorithm
from .viewport import Viewport
from .helper_maze_classes import Cell, MazeConfig
from typing import Tuple, List, Set
import os
import sys
import time


PATTERN = ["101 111", "101 001", "111 111", "001 100", "001 111"]


class MazeGenerator:
    def __init__(self, maze_config: MazeConfig) -> None:
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        self.entry = maze_config.entry
        self.exit = maze_config.exit
        self.viewport = Viewport(self.width, self.height)
        self.clamp_dimensions()
        self.calculate_offsets()
        self.grid: List[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()

    def calculate_offsets(self) -> None:
        """Calculates the exact coordinates to center the maze
        inside the Viewport.
        """
        maze_pixel_w = (self.width * 4) + 2
        maze_pixel_h = (self.height * 2) + 1

        self.offset_x = (self.viewport.offset_x +
                         (self.viewport.width - maze_pixel_w) // 2)
        self.offset_y = (self.viewport.offset_y +
                         (self.viewport.height - maze_pixel_h) // 2)

    def clamp_dimensions(self) -> None:
        # Ask the viewport what the maximum sizes are!
        self.width = max(11, min(self.width, self.viewport.max_maze_w))
        self.height = max(7, min(self.height, self.viewport.max_maze_h))

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
        os.system("cls" if os.name == "nt" else "clear")
        print("\033[?1049h\033[2J\033[?25l", end="")
        self.viewport.draw()
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
                    reset = "\033[48;5;235m"
                    east = f"{wall_bg}  {reset}" if (cell.value & 2) else "  "
                    top_row += f"{wall_bg}  {reset}"
                    mid_row += east

            output += (f"\033[{self.offset_y + (y * 2)};\
{self.offset_x}H{top_row}")
            output += (f"\033[{self.offset_y + (y * 2) + 1};\
{self.offset_x}H{mid_row}")

        boot_row = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            wall_bg = "\033[42m" if cell.is_fortytwo else "\033[100m"
            reset = "\033[0m"
            south = f"{wall_bg}  {reset}" if (cell.value & 4) else "  "
            boot_row += f"{wall_bg}  {reset}{south}"

        last_cell = self.grid[self.height - 1][self.width - 1]
        last_wall_bg = "\033[42m" if last_cell.is_fortytwo else "\033[100m"

        output += (f"\033[{self.offset_y + (self.height * 2)};{self.offset_x}H\
{boot_row}{last_wall_bg}  \033[0m")
        print(output, end="", flush=True)

    def animated_frame(self, cell1: Cell, cell2: Cell) -> None:
        # THE TWEENING FRAMES: Heavy static -> Medium -> Light -> Empty Space
        dust_stages = ["▓▓", "▒▒", "░░", "  "]

        for dust in dust_stages:
            for cell in [cell1, cell2]:
                top, middle = cell.get_render_strings(dust)
                cx = self.offset_x + (cell.x_value * 4)
                cy = self.offset_y + (cell.y_value * 2)
                print(f"\033[{cy};{cx}H{top}", end="")
                print(f"\033[{cy + 1};{cx}H{middle}", end="")
            sys.stdout.flush()
            time.sleep(0.002)

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
        end_y = self.viewport.offset_y + self.viewport.height
        msg = ("\033[92m ╰─▶ Generation Complete! Press \
[ENTER] to exit...\033[0m")
        print(f"\033[{end_y};{self.viewport.offset_x}H{msg}",
              end="", flush=True)
        input()
        print("\033[?1049l\033[?25h", end="")
