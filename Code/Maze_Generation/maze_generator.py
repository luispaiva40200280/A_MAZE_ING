from pydantic import BaseModel, Field
from typing import Tuple, List, Set
import os
import time
from Algor.prims import prims_algorithm

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


class MazeGenerator:
    """ """

    def __init__(self, maze_config: MazeConfig) -> None:
        self.config = maze_config
        self.width: int = maze_config.width
        self.height: int = maze_config.height
        self.grid: List[list[int]] = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.protected_cells: Set[Tuple[int, int]] = set()

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

    def print_ascii(self) -> None:
        print("\033[H", end="")
        output = ""
        # 1. We only draw the Top and Left edges for each cell to prevent
        # double-thick walls!
        for y in range(self.height):
            top_row = ""
            mid_row = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                is_fortytwo = (x, y) in self.protected_cells
                start_color = "\033[95m" if is_fortytwo else ""
                end_color = "\033[91m" if is_fortytwo else ""
                # THIN WALLS (1 char), WIDE PATHS (3 chars)
                corner = "█"
                # Check North Wall (1)
                north = "██" if (cell & 1) else "  "
                # Check West Wall (8)
                west = "█" if (cell & 8) else " "
                # Center of the room
                center = "██" if cell == 15 else "  "
                top_row += f"{start_color}{corner}{north}{end_color}"
                mid_row += f"{start_color}{west}{center}{end_color}"
                # If we are at the far right edge, draw the final East wall (2)
                if x == self.width - 1:
                    east = "█" if (cell & 2) else " "
                    top_row += f"{start_color}{corner}{end_color}"
                    mid_row += f"{start_color}{east}{end_color}"
            output += top_row + "\n" + mid_row + "\n"
        # 2. Draw the final bottom boundary (South walls of the very last row)
        bot_row = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            is_fortytwo = (x, self.height - 1) in self.protected_cells
            start_color = "\033[92m" if is_fortytwo else ""
            end_color = "\033[0m" if is_fortytwo else ""
            corner = "█"
            south = "██" if (cell & 4) else "  "
            bot_row += f"{start_color}{corner}{south}{end_color}"
        # The very last corner on the bottom right
        bot_row += "█\n"
        output += bot_row
        print(output)

    def animated_frame(self) -> None:
        self.print_ascii()
        time.sleep(0.2)

    def generate_maze(self, starr_coord: Tuple[int, int]) -> None:
        self.carve_42_pattern()
        os.system("cls" if os.name == "nt" else "clear")
        prims_algorithm(
            grid=self.grid,
            width=self.width,
            height=self.height,
            start_coord=starr_coord,
            protected=self.protected_cells,
            on_step=self.animated_frame,
        )
        self.print_ascii()
        print("\n\nMaze Generation Complete!!\n")


if __name__ == "__main__":
    try:
        print("Initializing Maze Generator...")
        time.sleep(1)

        # Pydantic loves keyword arguments!
        # Pass actual tuples (x, y) for entry and exit.
        maze_config = MazeConfig(
            width=20, height=18, entry=(0, 0), exit=(9, 0), perfect=True
        )
        # Instantiate your generator with the config
        maze = MazeGenerator(maze_config)
        # Start carving! (using your exact method name)
        maze.generate_maze(starr_coord=maze_config.entry)
    except KeyboardInterrupt:
        print("\n\nAnimation stopped by user. Exiting gracefully.")
