"""
Implementation of the Breadth-First Search (BFS) algorithm
for maze solving.

BFS is the optimal pathfinding algorithm for unweighted grid graphs
(such as these mazes) because its level-by-layer exploration
naturally guarantees finding the absolute shortest path between two points.
"""
from Maze_Generation.helper_maze_classes import Cell
from typing import List, Tuple, Callable, Any
from collections import deque


def breadth_first_search(
        grid: list[List[Cell]],
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        on_step: Callable[[Any, Any], None] | None = None,
        ) -> str:
    """
    Solves the maze by finding the shortest path from entry to exit.

    This algorithm uses a double-ended queue (`collections.deque`) to evaluate
    accessible cells in a First-In-First-Out (FIFO) sequence. For each cell, it
    checks the 4-bit wall mask against the available cardinal directions. If a
    wall is open (`(current_cell.value & bit) == 0`) and the adjacent cell has
    not been visited, it appends that neighbor to the queue along with the
    newly appended directional character.

    The use of a `visited` set ensures the algorithm never backtracks or enters
    an infinite loop within braided (imperfect) mazes.

    Args:
        grid (list[List[Cell]]): The completed 2D matrix of Cell objects
            representing the maze.
        width (int): The total width of the maze.
        height (int): The total height of the maze.
        entry (Tuple[int, int]): The (x, y) starting coordinate.
        exit (Tuple[int, int]): The (x, y) target destination coordinate.

    Returns:
        str: A string of concatenated directional characters (e.g., 'NNEESW')
        representing the exact shortest sequence of moves to reach the exit.
        Returns 'UNSOLVABLE' if the queue is exhausted without finding
        the exit.
    """
    from . import DIRECTIONS, LETTER_MAP
    queue = deque([(entry[0], entry[1], "")])
    visited = {entry}
    while queue:
        current_x, current_y, path = queue.popleft()
        if (current_x, current_y) == exit:
            return path
        current_cell = grid[current_y][current_x]
        for dir_x, dir_y, bit, _ in DIRECTIONS:
            if (current_cell.value & bit) == 0:
                new_x = current_x + dir_x
                new_y = current_y + dir_y
                if 0 <= new_x < width and 0 <= new_y < height:
                    if not (new_x, new_y) in visited:
                        visited.add((new_x, new_y))
                        direction = LETTER_MAP[bit]
                        next_cell = grid[new_y][new_x]
                        if on_step:
                            on_step(current_cell, next_cell)
                        queue.append((new_x, new_y, path + direction))
    return 'UNSOLVABLE'
