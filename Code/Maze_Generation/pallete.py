"""
Enum class to store the colors and themes for the
MazeGenerator to use in the rendering of the strings
on the terminal
"""

from enum import Enum


class ColorsMaze(Enum):
    """
    Enumeration of standard ANSI terminal BACKGROUND colors used in the
    maze rendering engine.
    """
    # Standard Background Colors (40-47)
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"
    RESET = "\033[0m"

    # NEW: Bold Foreground Text Colors for symbols!
    TXT_BOLD_GREEN = "\033[38;2;10;255;10m"     # Pure, blinding hacker green
    TXT_BOLD_PINK = "\033[38;2;255;0;150m"       # Intense neon pink/magenta
    TXT_BOLD_YELLOW = "\033[38;2;255;255;0m"     # Pure absolute yellow
    TXT_BOLD_CYAN = "\033[38;2;0;220;255m"  # Piercing cyan
    TXT_BOLD_RED = "\033[38;2;255;0;0m"
    TXT_BOLD_WHITE = "\033[1;97m"


class Themes(Enum):
    """
    Pre-defined color palettes for the maze components.
    """
    CYBERPUNK = {
        "logo": ColorsMaze.BG_BRIGHT_MAGENTA,
        "walls": ColorsMaze.BG_BLACK,
        "path": ColorsMaze.BG_BLUE,
        "entry": ColorsMaze.TXT_BOLD_YELLOW,
        "exit": ColorsMaze.TXT_BOLD_PINK
    }
    INFERNO = {
        "logo": ColorsMaze.BG_BRIGHT_YELLOW,
        "walls": ColorsMaze.BG_RED,
        "path": ColorsMaze.BG_BLACK,
        "entry": ColorsMaze.TXT_BOLD_YELLOW,
        "exit": ColorsMaze.TXT_BOLD_GREEN
    }
    NORMINETTE = {
        "logo": ColorsMaze.BG_BRIGHT_GREEN,
        "walls": ColorsMaze.BG_BLACK,
        "path": ColorsMaze.BG_BRIGHT_WHITE,
        "entry": ColorsMaze.TXT_BOLD_PINK,
        "exit": ColorsMaze.TXT_BOLD_RED
    }
    HACKER = {
        "logo": ColorsMaze.BG_WHITE,
        "walls": ColorsMaze.BG_BLUE,
        "path": ColorsMaze.BG_BLACK,
        "entry": ColorsMaze.TXT_BOLD_GREEN,
        "exit": ColorsMaze.TXT_BOLD_WHITE
    }
    FOREST = {
        "logo": ColorsMaze.BG_BRIGHT_RED,
        "walls": ColorsMaze.BG_GREEN,
        "path": ColorsMaze.BG_BLACK,
        "entry": ColorsMaze.TXT_BOLD_YELLOW,
        "exit": ColorsMaze.TXT_BOLD_CYAN
    }

    def get_color(self, component: str) -> str:
        """
        Helper method to safely retrieve the ANSI string for a
        specific component.
        """
        color_enum = self.value.get(component.lower())
        if color_enum:
            return color_enum.value
        return ColorsMaze.RESET.value
