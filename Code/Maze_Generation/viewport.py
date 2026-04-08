"""
Terminal UI scaling and rendering engine.
Handles mathematical calculations to adapt the maze visualization to varying
terminal window sizes safely.
"""
import os
import sys


class Viewport:
    """
    Creates a responsive, centered ASCII UI bounding box that acts as a canvas
    for the maze generator.
    Attributes:
        width (int): The finalized width of the UI box (in terminal columns).
        height (int): The finalized height of the UI box (in terminal rows).
        offset_x (int): The absolute starting X coordinate to center the box
        on screen.
        offset_y (int): The absolute starting Y coordinate to center the box
        on screen.
        max_maze_w (int): The mathematical limit for how wide a maze can be
        without breaking the box.
        max_maze_h (int): The mathematical limit for how tall a maze can be
        without breaking the box.
    """
    def __init__(self, requested_maze_w: int, requested_maze_h: int):
        """
        Initializes the Viewport by comparing the requested maze dimensions
        against the physical constraints of the user's terminal window.
        Args:
            requested_maze_w (int): The user's desired maze width.
            requested_maze_h (int): The user's desired maze height.
        """
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 130, 40

        # 1. Calculate Ideal Box Size
        target_box_w = (requested_maze_w * 4) + 2
        target_box_h = (requested_maze_h * 2) + 1

        # 2. Apply Terminal Limits
        max_term_box_w = max(50, term_col - 8)
        max_term_box_h = max(20, term_lines - 6)

        # 3. Finalize Box Dimensions
        self.width = min(target_box_w, max_term_box_w)
        self.height = min(target_box_h, max_term_box_h)

        # 4. Center the Box on the Screen
        self.offset_x = max(1, (term_col - self.width) // 2)
        self.offset_y = max(3, (term_lines - self.height) // 3)

        # 5. Tell the maze what its maximum allowed size is
        self.max_maze_w = (self.width - 6) // 4
        self.max_maze_h = (self.height - 4) // 2

    def draw(self) -> None:
        """
        Renders the outer bounding box UI to the terminal using ANSI escape
        codes.
        Leaves the interior space transparent so the terminal background shows
        through.
        """
        border_color = "\033[1;97m"
        reset = "\033[0m"

        top_border = (f"{border_color}╭" +
                      ("─" * (self.width - 2)) + f"╮{reset}")
        bottom_border = (f"{border_color}╰" +
                         ("─" * (self.width - 2)) + f"╯{reset}")
        empty_line = (f"{border_color}│" +
                      (" " * (self.width - 2)) + f"│{reset}")
        print(f"\033[{self.offset_y};{self.offset_x}H{top_border}")
        for i in range(1, self.height - 1):
            print(f"\033[{self.offset_y + i};{self.offset_x}H{empty_line}")
        print(f"\033[{self.offset_y + self.height - 1};\
{self.offset_x}H{bottom_border}")
        sys.stdout.flush()
