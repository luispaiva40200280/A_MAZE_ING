"""
prims algorithm:
construct of the maze
"""

import random
from typing import List, Tuple, Set, Callable

# North: y-1, break North (1) on current, South (4) on neighbor
# East:  x+1, break East (2) on current, West (8) on neighbor
# South: y+1, break South (4) on current, North (1) on neighbor
# West:  x-1, break West (8) on current, East (2) on neighbor
DIRECTIONS = [
    (0, -1, 1, 4),
    (1, 0, 2, 8),
    (0, 1, 4, 1),
    (-1, 0, 8, 2),
]


def prims_algorithm(
    grid: List[List[int]],
    width: int,
    height: int,
    start_coord: Tuple[int, int],
    protected: Set[Tuple[int, int]] | None = None,
    on_step: Callable[[], None] | None = None,
) -> None:

    if protected is None:
        protected = set()

    in_maze: Set[Tuple[int, int]] = set()
    frontier: List[Tuple[int, int]] = []

    def add_to_frontier(x_pos: int, y_pos: int) -> None:
        for dx, dy, _, _ in DIRECTIONS:
            nx_pos = x_pos + dx
            ny_pos = y_pos + dy
            if 0 <= nx_pos < width and 0 <= ny_pos < height:
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
    steps = 0
    while frontier:
        idx = random.randint(0, len(frontier) - 1)
        fx, fy = frontier.pop(idx)
        maze_neigbors = []
        for dx, dy, bit, opp in DIRECTIONS:
            nx = fx + dx
            ny = fy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) in in_maze and (nx, ny) not in protected:
                    maze_neigbors.append((nx, ny, bit, opp))
        if maze_neigbors:
            nx, ny, bit, opp = random.choice(maze_neigbors)
            grid[fy][fx] &= ~bit
            grid[ny][nx] &= ~opp
            in_maze.add((fx, fy))
            add_to_frontier(fx, fy)

            if on_step:
                steps += 1
                if steps % 3 == 0:
                    on_step()


""""
def print_grid_hex(grid: List[List[int]]) -> None:
    for row in grid:
        # Convert each cell integer to an uppercase hexadecimal string
        print("".join(f"{cell:X}" for cell in row))


if __name__ == "__main__":
    WIDTH = 25
    HEIGHT = 15

    # 1. Initialize a solid grid (all 15s)
    maze_grid = [[15 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # 2. Mock a protected area (Let's make a 5x5 block of Fs in the middle)
    # This represents where your "42" will eventually go.
    mock_protected: Set[Tuple[int, int]] = set()
    for y in range(5, 10):
        for x in range(10, 15):
            mock_protected.add((x, y))

    # 3. Pick a starting point (Entry)
    start = (1, 0)

    print("=== BEFORE PRIM'S (Solid Block) ===")
    print_grid_hex(maze_grid)

    # 4. Run the algorithm!
    prims_algorithm(maze_grid, WIDTH, HEIGHT, start, mock_protected)

    print("\n=== AFTER PRIM'S (Carved Maze) ===")
    print_grid_hex(maze_grid)
    print("\nLook closely at the middle. You should see a solid 5x5
    block of 'F's")
    print("that the algorithm completely ignored and routed around!")
"""
