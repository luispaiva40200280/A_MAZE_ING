from pydantic import BaseModel, Field
from typing import Tuple
from dataclasses import dataclass
from enum import Enum


class MazeConfig(BaseModel):
    """Class for the maze configuration"""
    width: int = Field(..., gt=0, description="width must be > 0")
    height: int = Field(..., gt=0, description="height must be > 0")
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    perfect: bool = Field(default=True)


@dataclass
class Cell:
    """Class for each cell of the maze
    do that is possible to print each cell
    dynamicly
    """
    x_value: int
    y_value: int
    value: int = 15
    is_fortytwo: bool = False

    def get_render_strings(self, dust: str = "  ") -> Tuple[str, str]:
        """Rendering of the cell in ascii art"""
        wall_bg = "\033[42m" if self.is_fortytwo else "\033[100m"
        dust_color = f"\033[96m{dust}\033[0m" if dust != "  " else "  "
        reset = "\033[0m"
        corner = f"{wall_bg}  {reset}"
        north = f"{wall_bg}  {reset}" if (self.value & 1) else dust_color
        west = f"{wall_bg}  {reset}" if (self.value & 8) else dust_color
        center = f"{wall_bg}  {reset}" if self.value == 15 else dust_color
        top = f"{corner}{north}"
        mid = f"{west}{center}"
        return top, mid


class ColorsMaze(Enum):
    pass
