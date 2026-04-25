 >While mathematically designed to find the [[Spanning Tree|Minimum Spanning Tree]] of a weighted graph, this project utilizes a [[Core Engine The Algorithms Registry|randomized variation ]]of Prim's Algorithm to carve the maze. 
> Unlike the [[Hunt and Kill Algorithm The Dual-Phase Carver|"Hunt and Kill"]] or "Recursive Backtracker" algorithms which act like tunnel diggers boring deep into the grid, Prim's algorithm grows outward uniformly like a crystal or a mold. Because it constantly picks a random edge along its entire perimeter, it produces a distinct topological texture: highly organic mazes with a massive amount of short, branching dead ends.

## 1. The Core Concept: "The Frontier"

   The entire algorithm is governed by a single data structure called the **Frontier**. 

* **Definition:** The frontier is the exact perimeter of the currently carved maze. It consists of all unvisited `Cell` objects that are immediately adjacent (North, South, East, West) to a cell that is already part of the maze.

* **How it dictates growth:** The algorithm never looks at the whole grid. It only looks at the frontier. By randomly selecting a cell from the frontier and connecting it to the existing maze, the maze slowly "eats" its way through the grid until the frontier is empty.

## 2. Function Architecture & State Management

   The `prims_algorithm()` function requires strict state management to prevent infinite loops and ensure it doesn't overwrite protected UI elements.

### The Tracking Sets
   __The function initializes two primary memory structures:__

* `in_maze`: A `Set` tracking the `(X, Y)` coordinates of every cell that has been successfully carved.

* `frontier`: A `List` of `(X, Y)` coordinates representing the current perimeter.

*(Note: `in_maze` uses a `Set` for $O(1)$ lockups, ensuring massive performance gains over standard lists when checking if a neighbor is already part of the maze).*

### The `add_to_frontier` Helper

  To expand the perimeter, this nested helper function is called every time a new cell is added to the maze.
  
* It scans the 4 cardinal directions around the newly added cell.

* **Boundary Safety:** It enforces strict bounds checking (`nx_pos >= 0 and nx_pos < width`) to prevent negative index wrap-around, which is a common fatal error in Python matrix traversal.

* If a neighbor is valid, not already in the maze, not already in the frontier, and not in the `protected` set (like the 42 pattern cells), it is appended to the frontier list.

## 3. The Execution Loop (Carving the Grid)

  Once the starting coordinate is added to `in_maze` and its neighbors populate the initial `frontier`, the core `while frontier:` loop begins.

1. **Selection:** It picks a totally random cell from the `frontier` list and pops it out.

2. **Finding the Anchor:** It looks at the 4 cardinal neighbors of this popped cell to find which ones are already inside `in_maze`. (There will always be at least one, but there might be multiple).

3. **The Bitwise Carve:** It randomly selects one of those valid `in_maze` neighbors. It extracts the directional `bit` and the opposite `opp` bit.
   * It executes `grid[fy][fx].value &= ~bit` on the frontier cell.
   * It executes `grid[ny][nx].value &= ~opp` on the anchor cell.
   * This mathematically "smashes" the wall between them.
   
```python
DIRECTIONS = [
	(0, -1, 1, 4), # North 0001
	(1, 0, 2, 8), # East
	(0, 1, 4, 1), # South
	(-1, 0, 8, 2), # West
]
```

3. **Expansion:** The former frontier cell is now officially added to `in_maze`, and `add_to_frontier()` is called to evaluate its unvisited neighbors.

## 4. UI Engine Integration (`on_step`)

  Because this algorithm executes instantly in system memory, the user would normally just see the finished maze pop onto the screen. 

* To mimic the 60-FPS terminal animation, the function accepts an `on_step` callback. The exact millisecond the bitwise carve is completed, it triggers `on_step(grid[fy][fx], grid[ny][nx])`. This yields execution back to the `MazeGenerator`'s Delta Renderer, forcing the terminal to paint the "dust" tweening animation for those two specific cells before the loop continues.