from pydantic import BaseModel, Field
from typing import Tuple, List

N = 1  # 0001
E = 2  # 0010
S = 4  # 0100
W = 8  # 1000


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

    def generate_maze(self) -> None:
        pass
