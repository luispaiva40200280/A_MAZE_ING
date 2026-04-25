
**[[The Theory of Maze Generation Algorithms]]**

> The A-Maze-Ing generator separates the logic of *what* a maze is (the grid) from *how* it is carved (the algorithm). This separation of concerns allows the application to dynamically hot-swap generation techniques during the interactive UI loop. 

## The Registry Pattern

Rather than hard coding `if/else` statements for every algorithm in the main menu, the engine utilizes a registry pattern in `all_algo.py` module. 

+ Using a dictionary approach the algorithms are store on it to be able to call them when necessary using the Callable typing keyword and storing it with different metadata (using a dataclass decorator) to give it extra more information on what to use it and its name.

* All constructor algorithms share a standardized function signature: they accept a 2D matrix of `Cell` objects and the configurations of the same grid and is starting point.
## The Algorithmic Suite

> The engine currently supports two distinct carving architectures and one solver:

1. **[[Prim's Algorithm (Randomized Maze Generation)|Prim's Algorithm]]**: Produces highly organic mazes with many short dead ends.

2. **[[Hunt and Kill Algorithm The Dual-Phase Carver|Hunt and kill]]**: Produces mazes with long, winding corridors (a high "river" factor).

3. **[[BFS - breadth first search]]**: The deterministic path finding engine that guarantees the shortest route from entry to exit.

## The randomize effect and seed recreation:

+ *__Computers cannot generate true random numbers on their own__*
	*__This module implements pseudo-random number generators for various distributions. __*
	
	*Because of this  they rely on mathematical algorithms to simulate randomness. This is known as **Pseudo-Random Number Generation (PRNG)**.

* When the `random` module is imported, its initialized a specific algorithm called the **[[Mersenne Twister]]** (specifically, the `MT19937` variant). 

+ #### 2. The Concept of the "Seed"

Every PRNG needs a starting point. This starting point is called the **Seed**.

To understand the mathematics conceptually, consider a much simpler PRNG algorithm called a __Linear Congruential Generator (LCG)__, which progresses state using this formula:

$Xn+1​=(a⋅Xn​+c)$ *(mod m)*

In this formula:

- Xn​ is the current state.
    
- Xn+1​ is the next "random" number.
    
- a, c, and m are constants.

The **Seed** is $X0$ — the very first number plugged into the equation. Once $X0$​ is provided, the entire infinite sequence of numbers is mathematically locked in.

- **Default Behavior:** If the seed is not provided, Python automatically seeds the `random` module using the operating system's current system time (down to the microsecond) or an OS-provided randomness source (like `/dev/urandom` in UNIX). Because the exact microsecond the script is run changes every time, the resulting sequence appears entirely random to the user.

* #### Seed Recreation (Procedural Reproducibility)

Seed recreation is the act of intentionally overriding the system time and forcing the PRNG to start at a specific, hard-coded value.

```python
import random
# Forcing the seed to a specific integer
random.seed(42)

print(random.randint(1, 100))  # Will ALWAYS print 82
print(random.randint(1, 100))  # Will ALWAYS print 15
print(random.randint(1, 100))  # Will ALWAYS print 4
```

#### 3. Hash and String Seeding** Python's
+ `random.seed()` does not strictly require an integer. You can pass strings or bytes into it (e.g., `random.seed("HACKER_THEME")`). Python will automatically hash the string into an integer and use that to initialize the Mersenne Twister. This allows developers to use human-readable words as configuration inputs for complex procedural tasks.