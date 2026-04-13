"""
Data structures and configuration models for the Maze Generator.
Contains the Pydantic configuration validation, the grid Cell representation,
and enumerated colors.
"""
from .pallete import Themes
from pydantic import BaseModel, Field, model_validator
from typing import Tuple, Any, Dict, Optional
from dataclasses import dataclass
import os


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
    output_file: str
    perfect: bool
    theme: Themes = Field(default=Themes.NORMINETTE)
    seed: Optional[Any] = Field(default=None)

    @classmethod
    def parser_file(cls, file_name: str) -> "MazeConfig":
        """
        Reads a configuration text file, parses the variables,
        and returns a validated MazeConfig object.
        The file should contain key-value pairs separated by '='.
        Lines starting with '#' or empty lines are ignored.
        The 'entry' and 'exit' keys are specifically parsed from
        comma-separated strings into tuples of integers.
        Args:
            file_name (str): The path to the configuration text file.
        Returns:
            MazeConfig: An initialized and validated instance of the
            maze configuration.
        Raises:
            FileNotFoundError: If the specified file path does not exist.
            Exception: If a duplicate configuration key is found in the file.
            ValueError: If 'entry' or 'exit' coordinates cannot be
            parsed as integers.
        """
        if not os.path.exists(file_name):
            raise FileNotFoundError

        config_data: Dict[str, Any] = {}
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key in config_data:
                        raise ValueError(f"Duplicated values in conf: {key}")
                    elif key in ["entry", "exit"]:
                        coords = value.split(",")
                        config_data[key] = (int(coords[0].strip()),
                                            int(coords[1].strip()))
                    elif key == "theme":
                        try:
                            config_data[key] = Themes[value.upper()]
                        except KeyError:
                            print(f"\033[33mWarning: Theme '{value}' not \
found. Defaulting to NORMINETTE.\033[0m")
                            config_data[key] = Themes.NORMINETTE
                    else:
                        config_data[key] = value
        return cls(**config_data)

    @model_validator(mode="after")
    def validate_terminal(self) -> "MazeConfig":
        """
        Ensures the requested maze dimensions can physically fit within
        the current terminal window. Calculates the maximum possible maze
        width and height based on the active terminal's columns and lines,
        accounting for UI padding/borders. If the terminal size cannot be
        determined by the OS, it defaults to a safe fallback of 130x40.
        Returns:
            MazeConfig: The current validated instance.
        Raises:
            ValueError: If the configured maze width or height exceeds the
            terminal's capacity.
        """
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 130, 40  # Fallback

        # Calculate the absolute maximum maze size for this terminal
        max_maze_w = (term_col - 10) // 4
        max_maze_h = (term_lines - 9) // 2

        if self.width > max_maze_w or self.height > max_maze_h:
            raise ValueError(
                f"Requested maze size ({self.width}x{self.height}) is too \
large for your terminal!\n"
                f"Please maximize your window, or reduce the config size to \
a maximum of {max_maze_w}x{max_maze_h}."
            )

        return self

    @model_validator(mode='after')
    def validate_entry_exit(self) -> 'MazeConfig':
        """
        Validates that the maze's entry and exit coordinates fall strictly
        within the grid boundaries.
        Checks the (x, y) coordinate tuples for both the 'entry' and 'exit'
        points to ensure they are >= 0 and strictly less than the
        maze's configured width
        and height.
        Returns:
            MazeConfig: The current validated instance.
        Raises:
            ValueError: If either the entry or exit coordinates are
            mapped outside the grid dimensions.
        """
        if self.width and self.height and self.entry and self.exit:
            if not (0 <= self.entry[0] < self.width
                    and 0 <= self.entry[1] < self.height):
                raise ValueError(f"Entry {self.entry} is outside the bounds of\
{self.width}x{self.height}!")
            if not (0 <= self.exit[0] < self.width
                    and 0 <= self.exit[1] < self.height):
                raise ValueError(f"Exit {self.exit} is outside the bounds of\
{self.width}x{self.height}!")
        return self

    @model_validator(mode='after')
    def validate_pattern_exit_entry(self) -> 'MazeConfig':
        """
        Validates that the maze entry and exit coordinates
        do not collide with the internal '42' logo pattern.
        Dynamically reads a binary bitmap pattern and centers it within the
        maze grid. Calculates the absolute (x, y) coordinates for all solid
        walls (characters marked as '1') and ensures the user's entry and
        exit points do not overlap them. Empty spaces or '0's in the pattern
        are treated as walkable ground, allowing spawn points inside the
        hollow areas of the numbers.
        Returns:
            MazeConfig: The current validated instance.
        Raises:
            ValueError: If either the entry or exit coordinate is placed
            exactly on top of a solid wall block within the 42 pattern.
        """
        from .maze_generator import PATTERN
        w_pattern = len(PATTERN[0])
        h_pattern = len(PATTERN)
        start_x = (self.width // 2) - (w_pattern // 2)
        start_y = (self.height // 2) - (h_pattern // 2)
        forbiden = set()
        for y, row in enumerate(PATTERN):
            for x, char in enumerate(row):
                if char == '1':
                    forb_x = start_x + x
                    forb_y = start_y + y
                    forbiden.add((forb_x, forb_y))
        if self.entry in forbiden:
            raise ValueError(f"Entry coord is in the 42 Pattern: {self.entry}")
        if self.exit in forbiden:
            raise ValueError(f"Exit coord is in the 42 Pattern: {self.exit}")
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
    is_entry = False
    is_exit = False

    def get_render_strings(self, active_theme: Themes,
                           dust: str = "  ") -> Tuple[str, str]:
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
        wall_color = active_theme.get_color("walls")
        logo_color = active_theme.get_color("logo")
        path_color = active_theme.get_color("path")
        entry_color = active_theme.get_color("entry")
        exit_color = active_theme.get_color("exit")
        reset = "\033[0m"

        wall_bg = logo_color if self.is_fortytwo else wall_color
        empty_path = f"{path_color}{dust}{reset}"
    # 2. The Center Symbol (ONLY used in the dead center of the cell)
        if self.is_entry:
            # Using 2-character symbols to perfectly center them in the 2-char
            # block!
            symbol = f"{entry_color}▓▓" if dust == "  " else dust
        elif self.is_exit:
            symbol = f"{exit_color}▓▓" if dust == "  " else dust
        else:
            symbol = dust

        center_display = f"{path_color}{symbol}{reset}"
        corner = f"{wall_bg}  {reset}"
        north = f"{wall_bg}  {reset}" if (self.value & 1) else empty_path
        west = f"{wall_bg}  {reset}" if (self.value & 8) else empty_path
        center = f"{wall_bg}  {reset}" if self.value == 15 else center_display
        top = f"{corner}{north}"
        mid = f"{west}{center}"
        return top, mid
