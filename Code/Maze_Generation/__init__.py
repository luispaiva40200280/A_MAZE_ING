# A simple dictionary to translate letters back into (dx, dy) math
import sys
import termios
from functools import wraps
from typing import Callable, Any


DIRECTION_DELTAS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}


def supress_terminal_echos(func: Callable[..., Any]) -> Callable[..., Any]:
    """
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
