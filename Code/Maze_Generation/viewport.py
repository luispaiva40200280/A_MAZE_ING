import os
import sys


class Viewport:
    def __init__(self, requested_maze_w: int, requested_maze_h: int):
        try:
            term_col, term_lines = os.get_terminal_size()
        except OSError:
            term_col, term_lines = 130, 40

        # 1. Calculate Ideal Box Size
        target_box_w = (requested_maze_w * 4) + 6 
        target_box_h = (requested_maze_h * 2) + 5

        # 2. Apply Terminal Limits
        max_term_box_w = max(50, term_col - 4)
        max_term_box_h = max(20, term_lines - 4)

        # 3. Finalize Box Dimensions
        self.width = min(target_box_w, max_term_box_w)
        self.height = min(target_box_h, max_term_box_h)

        # 4. Center the Box on the Screen
        self.offset_x = max(1, (term_col - self.width) // 2)
        self.offset_y = max(1, (term_lines - self.height) // 2)

        # 5. Tell the maze what its maximum allowed size is
        self.max_maze_w = (self.width - 6) // 4
        self.max_maze_h = (self.height - 5) // 2

    def draw(self) -> None:
        # \033[48;5;235m = Deep Slate Grey Background!
        # \033[38;5;250m = Light Grey Text for the borders
        border_color = "\033[1;97m"
        reset = "\033[0m"

        top_border = f"{border_color}╭" + ("─" * (self.width - 2)) + f"╮{reset}"
        bottom_border = f"{border_color}╰" + ("─" * (self.width - 2)) + f"╯{reset}"
        # To make the background solid, we fill the middle with colored spaces!
        empty_line = f"{border_color}│" + (" " * (self.width - 2)) + f"│{reset}"
        print(f"\033[{self.offset_y};{self.offset_x}H{top_border}")
        for i in range(1, self.height - 1):
            print(f"\033[{self.offset_y + i};{self.offset_x}H{empty_line}")
        print(f"\033[{self.offset_y + self.height - 1};{self.offset_x}H{bottom_border}")
        sys.stdout.flush()
