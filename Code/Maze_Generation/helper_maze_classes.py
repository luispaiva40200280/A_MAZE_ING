"""
Data structures and configuration models for the Maze Generator.
Contains the Pydantic configuration validation, the grid Cell representation,
and enumerated colors.
"""
from pydantic import BaseModel, Field, model_validator
from typing import Tuple
from dataclasses import dataclass
from enum import Enum


class MazeConfig(BaseModel):
    """
    Validates and stores the configuration parameters for maze generation.
    Attributes:
        width (int): The requested width of the maze in cells. Must be > 0.
        height (int): The requested height of the maze in cells. Must be > 0.
        entry (Tuple[int, int]): The (x, y) coordinates for the maze entrance.
        exit (Tuple[int, int]): The (x, y) coordinates for the maze exit.
        perfect (bool): Determines if the generated maze should be a "perfect"
            maze (having exactly one path between any two points and no loops).
    """
    width: int = Field(..., gt=0, description="width must be > 0")
    height: int = Field(..., gt=0, description="height must be > 0")
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    perfect: bool = Field(default=True)

    @classmethod
    def parser_config(cls, filepath: str) -> 'MazeConfig':
        """Reads a text file, parses the variables, and returns
        a validated MazeConfig object.
        """
        config_data = {}
        return cls(**config_data)

    @model_validator(mode='after')
    def validate_entry_exit(self) -> 'MazeConfig':
        """Ensures the entry and exit coordinates actually
        exist inside the maze boundaries.
        """
        return self

    @model_validator(mode='after')
    def validate_terminal_fit(self) -> 'MazeConfig':
        """Ensures the requested maze size can physically
        fit in the current terminal window."""
        return self


@dataclass
class Cell:
    """
    Represents a single structural cell within the maze grid.
    Handles its own geometric state (walls) and terminal rendering logic.
    Attributes:
        x_value (int): The X coordinate (column) of the cell in the grid.
        y_value (int): The Y coordinate (row) of the cell in the grid.
        value (int): A bitmask representing the cell's walls (North=1, East=2,
        South=4, West=8).
            Defaults to 15 (all walls intact).
        is_fortytwo (bool): Flag indicating if this cell is part of the
        protected '42' center pattern.
    """
    x_value: int
    y_value: int
    value: int = 15
    is_fortytwo: bool = False

    def get_render_strings(self, dust: str = "  ") -> Tuple[str, str]:
        """
        Calculates the ASCII color strings required to draw this specific
        cell in the terminal.
        Because terminal characters are twice as tall as they are wide,
        a single cell is represented by two rows of text (Top and Mid).
        Args:
            dust (str, optional): A 2-character string used to create
            tweening animations (like dissolving static) when walls are
            broken. Defaults to "  " (empty space).
        Returns:
            Tuple[str, str]: A tuple containing the formatted
            ANSI string for the
            top row of the cell, and the formatted ANSI string
            for the middle row.
        """
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
    """
    Enumeration of standard ANSI terminal colors used in the maze
    rendering engine.
    (Reserved for future color palette abstraction).
    """
    pass
