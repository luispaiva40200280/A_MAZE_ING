import random
from typing import List, Tuple, Set, Callable, Any

DIRECTIONS = [
    (0, -1, 1, 4),  # North
    (1, 0, 2, 8),  # East
    (0, 1, 4, 1),  # South
    (-1, 0, 8, 2),  # West
]


def prims_algorithm(
    grid: List[List[Any]],
    width: int,
    height: int,
    start_coord: Tuple[int, int],
    protected: Set[Tuple[int, int]] | None = None,
    on_step: Callable[[Any, Any], None] | None = None,
) -> None:

    if protected is None:
        protected = set()

    in_maze: Set[Tuple[int, int]] = set()
    frontier: List[Tuple[int, int]] = []

    def add_to_frontier(x_pos: int, y_pos: int) -> None:
        for dx, dy, _, _ in DIRECTIONS:
            nx_pos = x_pos + dx
            ny_pos = y_pos + dy
            # Strict boundary check to prevent negative index wrap-around
            if nx_pos >= 0 and nx_pos < width and ny_pos >= 0 and ny_pos < height:
                coord = (nx_pos, ny_pos)
                if (
                    coord not in in_maze
                    and coord not in frontier
                    and coord not in protected
                ):
                    frontier.append(coord)

    start_x, start_y = start_coord
    in_maze.add(start_coord)
    add_to_frontier(start_x, start_y)

    while frontier:
        idx = random.randint(0, len(frontier) - 1)
        fx, fy = frontier.pop(idx)
        maze_neighbors = []

        for dx, dy, bit, opp in DIRECTIONS:
            nx = fx + dx
            ny = fy + dy
            # Strict boundary check here too!
            if nx >= 0 and nx < width and ny >= 0 and ny < height:
                if (nx, ny) in in_maze and (nx, ny) not in protected:
                    maze_neighbors.append((nx, ny, bit, opp))

        if maze_neighbors:
            nx, ny, bit, opp = random.choice(maze_neighbors)

            # Modify the .value property of the Cell objects
            grid[fy][fx].value &= ~bit
            grid[ny][nx].value &= ~opp

            in_maze.add((fx, fy))
            add_to_frontier(fx, fy)

            # Trigger the Delta Renderer (Corrected Y/X indexing)
            if on_step:
                on_step(grid[fy][fx], grid[ny][nx])
