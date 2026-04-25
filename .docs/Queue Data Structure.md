
> In computer science, algorithms are only as efficient as the data structures that power them. While [[Prim's Algorithm (Randomized Maze Generation)|Prim's Algorithm]] relies on a `Set` for instant $O(1)$ look-ups, the [[BFS - breadth first search|Breadth-First Search]] (BFS) solver relies entirely on a **Queue** to manage its traversal state. 

__Understanding how a queue operates at the system level is critical to understanding why BFS guarantees the shortest possible path out of the maze.__

## 1. What is a Queue? (FIFO)

A queue is a linear data structure that strictly follows the **First-In-First-Out (FIFO)** principle. 

* **The Real-World Analogy:** Think of a queue exactly like a line of people waiting at a grocery store checkout. The first person to join the line is the first person to be served and leave. Anyone new who joins must go to the absolute back of the line.
     ![[Dequeue-Operation-in-Queue-1.webp]]

* **Core Operations:**
  * **Enqueue (Push):** Adding a new element to the back (tail) of the queue.
  * **Dequeue (Pop):** Removing the element from the front (head) of the queue.

## 2. Why BFS Requires a Queue

+ Pathfinding algorithms explore graphs by keeping track of which nodes (cells) to visit next. The data structure chosen for this "waiting list" completely changes the algorithm's behavior.

If you used a **Stack** (Last-In-First-Out), the algorithm would dive as deep as possible down a single hallway until it hit a dead end, ignoring all other branches. This is called Depth-First Search (DFS), and it does *not* guarantee the shortest path.

By using a **Queue**, BFS forces the engine to explore the maze **layer by layer**.

1. It looks at the Entry cell (Layer 0).

2. It enqueues all immediate neighbors 1 step away (Layer 1).

3. It must completely dequeue and evaluate every cell in Layer 1 before it is allowed to look at any cells in Layer 2.

Because it radiates outward uniformly, the very first time the queue dequeues the Exit cell, it is mathematically proven to be the shortest route.
