>  Breadth First Search (BFS) is a graph traversal algorithm that starts from a source node and explores the graph level by level. First, it visits all nodes directly adjacent to the source. Then, it moves on to visit the adjacent nodes of those nodes, and this process continues until all reachable nodes are visited.

- BFS is different from [DFS](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/) in a way that closest vertices are visited before others. We mainly traverse vertices level by level

- Popular graph algorithms like [Dijkstra's shortest path](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/), [Kahn's Algorithm](https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/), and [[Prim's Algorithm (Randomized Maze Generation)|Prim's algorithm]] are based on BFS.

- BFS itself can be used to detect cycle in a directed and undirected graph, find shortest path in an unweighted graph and many more problems.

+ ### The implementation

	+ This algorithm uses a __[[Queue Data Structure|double-ended queue]]__ (`collections.deque`) to evaluate accessible cells in a First-In-First-Out (FIFO) sequence.
	
	+ It stores the entry point in a **Set** that serves to track all the visited cells in the grid, preventing infinite loops and O(N) lookup bottlenecks.
	
	+ Inicializes a loop to go trough the maze grid using the queue and pops the first and only element (forcing the algorithm to explore the maze evenly layer-by-layer to mathematically guarantee finding the shortest possible path.). From there, the execution follows these strict steps:
	
		+ **1. The Termination Check:** Immediately after removing the current element, the algorithm verifies if these coordinates match the target If they match, the algorithm halts and returns the final path string.
		
		+  **2. Bitwise Inspection (Reading the Walls):** The `Cell` object from the matrix is retrieved. It iterates through the four cardinal directions and evaluates the cell's 4-bit integer mask. By applying the bitwise AND operator (`&`) against the directional bit, it identifies which walls are broken (the operation evaluates to `0`).
```python
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
```
 
   +  **3. Neighbor Validation** For every direction where a wall is open, the algorithm calculates the exact `(X, Y)` coordinate of that neighbor. It must then pass two strict checks:
		- **Boundary Check:** The new coordinates must fall within the absolute width and height of the grid.
    
		- **Visited Check:** The new coordinates must _not_ exist in the `visited` Set.

   - **4. State Update and Enqueue** If the neighbor passes validation, it is immediately added to the `visited` Set. The algorithm then appends this new neighbor to the back of the double-ended queue. Crucially, it takes the directional movement used to reach it (e.g., 'N' for North) and concatenates it to the parent's path string, ensuring the sequence of moves is perfectly preserved as the queue expands layer by layer.

```python
if 0 <= new_x < width and 0 <= new_y < height:
	if not (new_x, new_y) in visited:
		visited.add((new_x, new_y))
		direction = LETTER_MAP[bit]
		next_cell = grid[new_y][new_x]
		queue.append((new_x, new_y, path + direction))
```
