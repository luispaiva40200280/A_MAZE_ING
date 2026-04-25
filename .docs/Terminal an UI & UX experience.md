
Most terminal scripts simply print lines of text from top to bottom. The **A-Maze-Ing** generator breaks this paradigm by utilizing absolute *ANSI cursor positioning*, dynamic view-port scaling, and raw UNIX keystroke capturing to mimic a responsive, 60-FPS-style interactive canvas.

This document breaks down the architectural components that drive the User Experience (UX).

---
## 1. The View-port Engine (Dynamic Scaling & Centering)

   Because monitors can have various sizes, the maze cannot rely on hard-coded coordinates. The UI uses a dynamic View-port class creating a responsive, centered ASCII UI bounding box that acts as a canvas for the maze generator.

+ #### **ANSI Escape Codes**:
	**ANSI escape sequences** are a standard for [in-band signaling](https://en.wikipedia.org/wiki/In-band_signaling "In-band signaling") to control cursor location, color, font styling, and other options on [text terminals](https://en.wikipedia.org/wiki/Text_terminal "Text terminal") and [terminal emulators](https://en.wikipedia.org/wiki/Terminal_emulator "Terminal emulator"), allowing an application to treat the terminal like a 2D graphical canvas.
	They always start with the `esc` character sequence `\033` in python.
	
	### [[How ANSI codes are used in the project]]

+ ### How Viewport works:

	 On top of the use the ANSI and ASCII codes to paint the hallow box with only the bordes visible using the characters [`- , | , ╭ ,  ╮`], the viewport needs to be draw with the __maze and the terminal in mind__.

	 + #### Terminal size:
		The terminal size is calculated using the library `import os` and is method `.get_terminal_size()` that returns a `tuple[int, int]` that represents the size of the terminal in columns and lines respectively. 
		__*It falls back to a safe 130x40*__
			
	+ #### Maze size: 
		Its calculated by the maze configuration on the `config.txt` file and than is use on the Viewport to scale it, so the width is (* 4 + 2) the width of the maze and the height is (* 2 + 1) the maze height.

This calcule is use to find the max value for each dimension between the size of the maze and the terminal itself, and also the center of the box. 

![[code_vierport_cal.png]]

---

## 2. Rendering the Grid (ANSI Coordinate Math)
 
   To render a 2D maze inside the terminal, the engine abandons standard `print()` statements in favor of the same [[How ANSI codes are used in the project|**ANSI Escape Sequences**]] use in on the Viewport.

* ### Dividing the Grid: Logical and Visual Architecture

   The A-Maze-Ing generator does not treat the terminal as a raw text file. Instead, it constructs a strict 2D coordinate system. The maze is divided into individual structural units called **Cells**, which manage their own mathematical state (value of the walls break) and their own terminal rendering logic.
  
	* #### 1. The Logical Grid (Data Structure)
	   + Inside the `MazeGenerator` class, the entire maze is stored in memory as a 2D matrix (a List of Lists). 
	*During initialization, the grid is built using a nested list comprehension:*

```python
self.grid: List[List[Cell]] = [
    [Cell(x, y) for x in range(self.width)] for y in range(self.height)
]
```
	
  * This guarantees that every single cell has an exact `(X, Y)` coordinate, allowing path finding algorithms to easily calculate neighbor positions by adding or subtracting '1' from the X or Y coordinates.

* #### 2. The `Cell` Object
   Each unit in the grid is an instance of the `Cell` dataclass. Instead of storing a complex list of strings for walls, the Cell uses extreme memory efficiency by storing its wall states as a **4-bit integer mask**.

- **Base Value:** Every cell starts with a `value` of `15` (binary `1111`), meaning all 4 walls are intact.
    
- **Bitwise Directions:**

	* North = 1 (`0001`)
    - East = 2 (`0010`)
    - South = 4 (`0100`)
    - West = 8 (`1000`)
        
	- When an algorithm "smashes" a wall, it uses bitwise operators (e.g., `cell.value &= ~bit`) to flip the corresponding bit to `0`.

#### 3. The Visual Architecture (The 4x2 Terminal Block)

+ Standard terminal font characters are roughly twice as tall as they are wide so if you try to  print a maze using 1 character per cell, it will look stretched and distorted. So to get a way to ignore that, the `Generator` divides each cell int blocks of 4x2 characters.

	+ ##### The Cell Anatomy:
		+ Every cell is responsible to draw itself, and it does so rendering to string, one for the top row and for the middle row. 
			+ \[top row\] »» (corner)(north wall) == "2 char" + "2 char"
			+ \[middle row\] »» (west wall)(center) == "2 char" + "2 char"
		
		* #### Special attributes:
			* Aside from wall states, the `Cell` also tracks its identity within the maze using boolean flags: `is_entry`, `is_exit`, and `is_fortytwo`. These flags tell the rendering engine to apply specific colors or protect the cell from being destroyed by the maze algorithms.
		
	Because the South and East walls overlap with the North and West walls of neighboring cells, a cell only needs to render its own North and West.
	The absolute outer right and bottom borders of the maze are drawn dynamically by the `draw_ascii_grid()` loop in the the `MazeGenerator` class.
	- The Cell also evaluates its own bitmask with the `get_render_strings()` method.
		- If the wall bit is active `(= 1)` it paints it with the wall color of the Themes else it paints it with the path color then it returns the formatted ANSI strings for `(top, mid)` back to the generator, which uses ANSI absolute positioning (`\033[{y};{x}H`) to print those two rows on top of each other.
```python
empty_path = "  "
north = f"{wall_bg}  {reset}" if (self.value & 1) else empty_path
west = f"{wall_bg} {reset}" if (self.value & 8) else empty_path
center = f"{wall_bg} {reset}" if self.value == 15 else center_display
```

+ **The Center Display:** If a cell is marked as `is_entry` or `is_exit`, the `get_render_strings()` method injects a special 2-character block symbol `▓▓` into the center of the cell. It colors this symbol using the specific `entry` or `exit` ANSI codes defined in the current Theme, making the start and end points stand out from the standard path.

- If the North bit (`1`) is active, it paints the `top` row with the current Theme's wall color. If the bit is `0`, it paints it with the path color.
    
- It returns the formatted ANSI strings for `(top, mid)` back to the generator, which uses ANSI absolute positioning (`\033[{y};{x}H`) to print those two rows on top of each other.

  * ### Animations

	  On the the class `MazeGenerator` the method `animated_frame()` as a list of special characters `["▓▓", "▒▒", "░░", " "]` making it possible to mimic a dust effect iterating trough that list for each 2 `Cell` in on the grid and rendering it multiple times in a fraction of a second.

```python
	dust_stages = ["▓▓", "▒▒", "░░", " "]
	for dust in dust_stages:
		for cell in [cell1, cell2]:
			top, middle = cell.get_render_strings(self.active_theme, dust)
			cx = self.offset_x + (cell.x_value * 4)
			cy = self.offset_y + (cell.y_value * 2)
			print(f"\033[{cy};{cx}H{top}", end="")
			print(f"\033[{cy + 1};{cx}H{middle}", end="")	
			sys.stdout.flush()
			time.sleep(0.004)
```

   * ***The Flush:** By default, standard UNIX terminals are "line-buffered," meaning they wait until they receive a newline character (`\n`) before actually drawing text to the monitor. Because our `print` statements end with `end=""` (no newline), the terminal would normally hold the animation in memory and print it all at once at the end. `sys.stdout.flush()` forcefully empties the buffer, demanding the terminal paint the pixels immediately.
    
   - **The Sleep:** `time.sleep(0.004)` introduces a microscopic 4-millisecond delay between loop iterations. This acts as the engine's frame-rate limiter, creating a smooth sequence rather than finishing the calculation before the human eye can process it.

*__This animation is used on the algorithms functions when call on the grid with all walls close and when the bit (value) of a cell is change the animation happens on the current cell that are being change and the next cell of the direction where the algorithm is going.__*

* ### MENU CONTROLLER:

	+ The `Controller` class provides an menu to interact to the maze generator and rather than executing sequentially and terminating, the `menu_controller` establishes a **continuous event loop**. This keeps the application process alive, permanently listening for I/O interrupts and redrawing the terminal buffer in real-time until the user explicitly sends an exit signal.

		1. "Generate new maze:"
			+ This option makes a new maze, resenting the grid to is first state (all values = 15) and calling the `generate_maze()` method to carve a new maze with the same algorithm and different `seed`

		2. "Toggle path:"
			+ Makes it possible to show or hide the shortest path that is solve after the maze is generated
		
		3. "Change theme:"
			+ Allows the user to see the same maze with different themes changing the attribute `active_theme` to a random theme form the [[Themes|list of themes]] 
		
		4. "Change Algorithm:"
			+  Changes the algorithm to construct the maze using the same functions of the option 1 but calling the method to create it with a different [[Core Engine The Algorithms Registry|algorithm to construct]]
		
		5. "Exit :"
			* This terminates the program giving a `break` to the loop and clearing the terminal

* #### Terminal echoing:
	* In the normal terminal every time some one makes a key-press when a program is running the terminal grabs the signal and prints the character of the key that was press. Also when that happens if a python script is running in the terminal without techniques and external libraries like [[TTY & Terminos]] 
	
	* __Using this libraries allows the program to grab each key stroke of the user and not show the output on the terminal while the maze is being shown and while continuous event loop keeps the process live__
