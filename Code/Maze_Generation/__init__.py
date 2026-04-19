# A simple dictionary to translate letters back into (dx, dy) math
import sys
import termios
from functools import wraps
from typing import Callable, Any

"""
This constant is used to translate a string-based path solution
(e.g., "NNEES") into physical 2D grid movements.
"""
DIRECTION_DELTAS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}


def supress_terminal_echos(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator to temporarily disable terminal echoing during
    function execution.
    Modifies the raw terminal attributes (using termios) to suppress the
    visibility of user keystrokes. This prevents key presses
    (like menu navigation) from printing to the standard output
    and corrupting the active ASCII UI.
    The original terminal settings are securely backed up before execution
    and strictly restored in a 'finally' block, ensuring the terminal is
    never left in a broken state even if the wrapped function crashes.
    Args:
        func (Callable[..., Any]): The function to be executed silently.
    Returns:
        Callable[..., Any]: The wrapped function with terminal echo suppression
        applied during its runtime.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # 2. Turn off ECHO (prevents key presses from showing)
            new_settings = termios.tcgetattr(fd)
            new_settings[3] = new_settings[3] & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
            return func(*args, **kwargs)
        finally:
            # 4. ALWAYS restore settings, even if the algorithm crashes
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return wrapper
