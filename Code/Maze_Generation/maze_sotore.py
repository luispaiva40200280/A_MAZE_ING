from .helper_maze_classes import Cell
from .maze_generator import MazeGenerator
from dataclasses import dataclass
from typing import List
# import json


@dataclass
class MazeDataBase:
    maze: MazeGenerator
    json_file: str = "mazes_database.json"

    def export_maze_txt(self, hex_rep: List[List[Cell]]) -> None:
        path = "Configs"
        output = self.maze.config.output_file

        with open(f"{path}/{output}", "w") as file:
            for row in hex_rep:
                output = "".join([hex(cell.value)[2:].upper() for cell in row])
                file.write(f"{output}\n")
            entry_x, entry_y = self.maze.entry
            exit_x, exit_y = self.maze.exit
            file.write(f"\n{entry_x},{entry_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write(f"\n{self.maze.path}")

    def export_maze_json(self) -> None:
        pass
