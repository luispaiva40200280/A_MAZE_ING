"""
this algorithm is to solve the mazes
and find the shortes path possible
"""
from Maze_Generation.helper_maze_classes import Cell
from typing import List, Tuple
from collections import deque


def breadth_first_search(
        grid: list[List[Cell]],
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        ) -> str:
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
                        queue.append((new_x, new_y, path + direction))
    return 'UNSOLVABLE'
