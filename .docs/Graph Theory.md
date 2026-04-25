### 1. What is Graph Theory?

__A graph is not a chart (like a bar graph or a pie chart). In discrete mathematics, a graph is formally defined as *G=(V,E)*.__
+ **V (Vertices):** Also called nodes. These represent the fundamental objects or entities.
+  **E (Edges):** Also called links or lines. These represent the connections or relationships between the vertices.

>   Graphs can be **undirected** (the connection goes both ways, like a physical hallway between two rooms) or **directed** (the connection is one-way, like a one-way street). They can also be **weighted** (where traversing an edge costs a certain amount of time, distance, or resources) or **unweighted** (all connections cost the same).

### 2. What is it Used For?

> Graph theory is used to solve any problem that involves networks, routing, or relationship mapping.

- **Computer Networks and the Internet:** Routers use graph algorithms (like OSPF or BGP ) to calculate the most efficient path to send data packets across the globe. The routers are the vertices, and the physical cables are the edges.
 
- **GPS and Navigation Systems:** Google Maps treats intersections as vertices and roads as weighted edges (where the weight is the time it takes to drive that road). It then runs pathfinding algorithms like Dijkstra's or A*, or [[BFS - breadth first search|Bread First Search]] to find the shortest rout.

- **Social Networks:** Platforms like LinkedIn or Facebook use massive graphs to calculate connections. You are a vertex; your friends are connected to you via edges. This is how the system calculates "Degrees of Separation" or suggests people you might know.

- **Compilers and Software Engineering:** When code is compiled, the compiler builds a "Dependency Graph" to figure out which modules must be built first before other modules can compile.

### 3. Why Use It?

**Absolute Abstraction** Graph theory strips away irrelevant physical and visual details. It strictly isolates the problem down to pure topology: _What connects to what?_ This allows you to write clean, mathematical logic that is immune to physical constraints.

**Algorithmic Standardization** Once you translate a real-world problem into a mathematical graph, you do not have to invent a solution from scratch. You immediately unlock decades of heavily optimized, peer-reviewed algorithms.

- Need to find the shortest path out of a grid? You apply **[[BFS - breadth first search]]**.

- Need to connect a dozen computer servers with the minimum amount of physical cable? You apply **Prim's Algorithm** to find the Minimum Spanning Tree.

By modeling a system as a graph, you transform complex, subjective real-world problems into solvable mathematical equations.