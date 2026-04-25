> At its core, maze generation is an exercise in applied **[[Graph Theory]]**. While visually a maze appears as a 2D grid of walls and corridors, mathematically, it is treated as a network of connected points.

#### 1. The Graph Theory Model

+ **Nodes (Vertices):** Every individual cell (or room) in the grid is a node.

- **Edges:** The potential connections between adjacent cells are the edges. A solid wall means the edge is "cut" or absent; an open path means the edge is intact.

- **Weights:** In randomized generation, algorithms often assign random "weights" to these edges to mathematically decide which walls to break and which to keep
#### 2. [[Spanning Tree|The "Perfect Maze" (Spanning Trees)]]

   The vast majority of standard maze algorithms are designed to generate **Perfect Mazes** (also known as simply connected mazes).

- A perfect maze has **no loops** (cycles) and **no inaccessible areas**.
- This means there is exactly one unique path between any two cells in the grid.
- In mathematical terms, generating a perfect maze is identical to finding a **Spanning Tree** across the grid graph

#### 3. Algorithmic Categories

   Because generating a spanning tree is a solved mathematical problem, maze algorithms are simply different mathematical traversal methods for building that tree. Each approach produces a distinct topological bias or "texture":

- **Graph Traversal (Depth-First / Recursive Backtracker):** Acts like a tunnel digger. It carves a path as far as it can go until it hits a dead end, then backtracks to the nearest branch.
    
    - _Theoretical output:_ Produces a tree with a high "river factor" (long, winding, deeply nested corridors with few dead ends).

- **Minimum Spanning Trees (Kruskal's / [[Prim's Algorithm (Randomized Maze Generation)]]):** These look at the edges (walls) rather than the nodes, assigning them random weights and breaking them only if they do not create a loop.
    
    - _Theoretical output:_ Prim's algorithm produces highly branched trees with many short, trivial dead ends.

- **Random Walks (Aldous-Broder / [[Hunt-and-Kill]]):** The algorithm wanders randomly through the grid, carving paths to unvisited nodes.
    
    - _Theoretical output:_ Algorithms like Aldous-Broder are computationally inefficient but produce mathematically uniform spanning trees (meaning every possible perfect maze has an exact equal probability of being generated).

- **Space Partitioning (Recursive Division):** A top-down approach. It starts with an empty room, builds a wall to divide it, leaves a single gap (edge), and recursively divides the sub-rooms.
    
    - _Theoretical output:_ It is a fractal-based algorithm that produces highly visible, long straight walls