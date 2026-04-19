"""
Implementation of the Hunt and Kill algorithm for maze generation.

Hunt and Kill natively produces a "perfect" maze
(a uniform spanning tree with no loops). If an imperfect
(braided) maze is desired, loops must be manually injected post-generation.
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
    The algorithm operates in two alternating phases
    without using a memory stack:

    1. The "Walk" Phase: Starting from an active cell, it performs a random
       walk through unvisited neighbors, smashing walls and marking cells as
       visited until it reaches a dead end (becomes trapped).

    2. The "Hunt" Phase: Once trapped, it performs a systematic, top-to-bottom,
       left-to-right scan of the entire grid. It searches for the first
       unvisited cell that is adjacent to at least one visited cell. It smashes
       the wall between them, and the unvisited cell becomes the new starting
       point for a new Walk phase.

    This process repeats until the Hunt phase fails to
    find any unvisited cells, meaning the grid is fully connected.
    Args:
        grid (List[List[Cell]]): The 2D array of Cell objects to be carved.
        width (int): The maximum width constraint of the grid.
        height (int): The maximum height constraint of the grid.
        start_coord (Tuple[int, int]): The (x, y) coordinates where the initial
            random walk should begin.
        protected (Set[Tuple[int, int]] | None, optional): A set of coordinates
            (e.g., the '42' pattern) that the algorithm is strictly forbidden
            from modifying or utilizing as paths. Defaults to None.
        on_step (Callable[[Any, Any], None] | None, optional): A callback hook
            triggered after every successful wall breach.
            Passes the two connected Cell objects to drive step-by-step
            UI rendering. Defaults to None.
        rng (Any, optional): A seeded random number generator
        instance to ensure reproducibility. If omitted, the standard
        random module is used.
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
