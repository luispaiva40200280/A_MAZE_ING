"""
Data persistence and export handling for the Maze Generator.

This module provides the `MazeDataBase` class, which is responsible for
translating the in-memory, bitmask-based maze grid into the specific
text format required by the project specifications.
It handles all file I/O operations to safely save the
generated maze structure, entry/exit coordinats and the solved path.
"""
from .helper_maze_classes import Cell
from .maze_generator import MazeGenerator
from dataclasses import dataclass
from typing import List


@dataclass
class MazeDataBase:
    """
    Handles the exporting and saving of maze data.

    Attributes:
        maze (MazeGenerator): The active maze generator instance containing
        the configuration, grid, entry/exit points, and solved path.
    """
    maze: MazeGenerator

    def export_maze_txt(self, hex_rep: List[List[Cell]]) -> None:
        path = "Configs"
        output = self.maze.config.output_file

        with open(f"{path}/{output}", "w") as file:
            for row in hex_rep:
                line = "".join([hex(cell.value)[2:].upper() for cell in row])
                file.write(f"{line}\n")
            entry_x, entry_y = self.maze.entry
            exit_x, exit_y = self.maze.exit
            file.write(f"\n{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write(f"{self.maze.path}\n")
