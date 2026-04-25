> The hunt-and-kill algorithm is in many ways the same as the backtracking algorithm in that it creates long winding paths. 


While Prim's algorithm grows outward uniformly like a crystal, the Hunt and Kill algorithm acts like a tunneling worm.  It prioritizes driving deep, continuous paths into the grid, resulting in a maze topology with a high "river factor" (long, winding corridors) and significantly fewer dead ends.

From a systems engineering perspective, Hunt and Kill is unique because it operates almost entirely without auxiliary memory structures. It does not require a Stack, a Queue, or a Set.

## 1. State Management: The Zero-Memory Footprint

Algorithms like Depth-First Search (DFS) require a `Stack` to remember where they have been so they can backtrack when they hit a dead end. In massive grids, this stack can consume significant memory.

Hunt and Kill bypasses this requirement. It uses the grid itself as its only state tracker. It relies purely on reading the 4-bit integer mask of the `Cell` objects to determine if a cell has been visited (e.g., evaluating if a cell's value is still `15`, meaning all walls are intact).

## 2. The Execution Loop: Two Alternating Phases

The engine continuously alternates between two distinct operational modes until the entire grid is carved.

+ ### Phase A: The "Kill" (Random Walk)

	1. The algorithm begins at a designated starting coordinate

	2. It evaluates the 4 cardinal directions and compiles a list of valid neighbors that are strictly **unvisited** (value equals `15`).

	3. If unvisited neighbors exist, it randomly selects one, mathematically smashes the wall between them using the [[Bitwise Operation|bitwise NOT operator]] (`&= ~bit`), and steps into the new cell.

	4. It repeats this random walk, driving a single continuous path forward, until it steps into a cell where all adjacent neighbors have already been visited. This is a dead end. 

	5. When trapped, the Kill phase terminates, and the engine triggers the Hunt phase.

```python
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
			nx, ny, bit, opp = rng.choice(unvisited_neighbors)
			grid[current_y][current_x].value &= ~bit
			grid[ny][nx].value &= ~opp
			visited.add((nx, ny))
			current_x, current_y = nx, ny			
		else:	
			trapped = True
```

### Phase B: The "Hunt" (Grid Scan)

Once the random walk terminates, the algorithm must find a new starting point. Because it has no memory stack to backtrack through, it must physically scan the grid.

1. The engine initiates a strict `for y... for x...` nested loop, scanning the grid from top-left to bottom-right.

2. It looks for a highly specific condition: **An unvisited cell that is immediately adjacent to at least one visited cell.**

3. The instant it finds a cell matching this condition, the scan halts.

```python
for y in range(height):
	if new_start_found:
		break
	for x in range(width):
		if (x, y) not in visited:
			visited_neighbors = []
			for dx, dy, bit, opp in DIRECTIONS:
				nx, ny = x + dx, y + dy
		if 0 <= nx < width and 0 <= ny < height:
			if ((nx, ny) in visited and (nx, ny) not in protected):
				visited_neighbors.append((nx, ny, bit, opp))
```

4. It randomly selects one of the adjacent *visited* neighbors and carves the wall between them, effectively connecting the unvisited cell to the existing maze.

5. This newly connected cell becomes the new starting coordinate, and the engine immediately switches back to the **Kill Phase**.

```python
if visited_neighbors:
	nx, ny, bit, opp = rng.choice(visited_neighbors)
	grid[y][x].value &= ~bit
	grid[ny][nx].value &= ~opp
	visited.add((x, y))
	current_x, current_y = x, y
	new_start_found = True
	break
```

## 3. Termination
The algorithm naturally terminates when the Hunt phase completes a full scan of the grid and fails to find any unvisited cells. 

```python
if not new_start_found:
	break
```

## 4. Architectural Trade-offs (CPU vs. Memory)

* **The Advantage (Memory):** Because it does not maintain a `frontier` list or a `visited` set, the auxiliary space complexity is $O(1)$. It is exceptionally memory-efficient.

* **The Disadvantage (CPU):** The time complexity suffers. Every time the algorithm hits a dead end, it must rescan the grid. In the late stages of generation, the engine might have to iterate over thousands of cells just to find the last few remaining unvisited blocks. This creates redundant CPU cycles, making it slower on massive grids compared to Prim's or standard Backtracking.

## 5. UI Integration (`on_step`)

To maintain the 60-FPS interactive canvas, the `on_step` callback must be triggered during both phases. 

* During the Kill phase, the UI updates rapidly as the path shoots forward. 

* During the Hunt phase, a visual delay may occur on larger mazes as the engine silently iterates over the 2D matrix in the background before finding its next connection point.