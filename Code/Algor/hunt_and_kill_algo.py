"""
this algor is going to be for creating imperfect mazes
"""
import random
from typing import List, Tuple, Set, Callable, Any
from . import DIRECTIONS
from Maze_Generation.helper_maze_classes import Cell


def hunt_and_kill_algo(
    grid: List[List[Cell]],
    width: int,
    height: int,
    start_coord: Tuple[int, int],
    protected: Set[Tuple[int, int]] | None = None,
    on_step: Callable[[Any, Any], None] | None = None,
    rng: Any = None
) -> None:
    """
    Maze algorithm to create an
    """
    if protected is None:
        protected = set()
    rng = rng or random
    visited: set[Tuple[int, int]] = set(protected)

    current_x, current_y = start_coord
    visited.add((current_x, current_y))
    while True:
        trapped = False
        while not trapped:
            unvisited_neighbors = []
            for dx, dy, bit, opp in DIRECTIONS:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        unvisited_neighbors.append((nx, ny, bit, opp))

            if unvisited_neighbors:
                # Pick a random neighbor, smash the wall, and move there!
                nx, ny, bit, opp = rng.choice(unvisited_neighbors)
                grid[current_y][current_x].value &= ~bit
                grid[ny][nx].value &= ~opp
                visited.add((nx, ny))
                if on_step:
                    on_step(grid[current_y][current_x], grid[ny][nx])
                current_x, current_y = nx, ny
            else:
                trapped = True

        new_start_found = False
        for y in range(height):
            if new_start_found:
                break
            for x in range(width):
                if (x, y) not in visited:
                    # Check if this unvisited cell is next to a VISITED cell
                    visited_neighbors = []
                    for dx, dy, bit, opp in DIRECTIONS:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if ((nx, ny) in visited and (nx, ny)
                                    not in protected):
                                visited_neighbors.append((nx, ny, bit, opp))

                    if visited_neighbors:
                        nx, ny, bit, opp = rng.choice(visited_neighbors)
                        grid[y][x].value &= ~bit
                        grid[ny][nx].value &= ~opp
                        visited.add((x, y))
                        if on_step:
                            on_step(grid[y][x], grid[ny][nx])
                        current_x, current_y = x, y
                        new_start_found = True
                        break
        if not new_start_found:
            break
