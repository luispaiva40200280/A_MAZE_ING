#### The Enum Class: Managing Theme State

+ In software engineering, dealing with raw, hard coded values —often called "magic strings" or "magic numbers"— is a major architectural anti-pattern. If you scatter raw [[How ANSI codes are used in the project|ANSI escape codes]] (`\033[47m`) across multiple files, updating a color or adding a new theme requires manually hunting down every instance in the codebase.

To solve this, the A-Maze-Ing generator uses Python's built-in `Enum` (Enumeration) class to handle its visual themes. 

#### 1. What is an Enum?

+ An `Enum` is a special Python class used to define a set of symbolic names (members) bound to unique, constant values. According to the [official Python documentation](https://docs.python.org/3/library/enum.html), enumerations are useful for defining an immutable, related set of constant values that may or may not have semantic meaning.

By inheriting from `Enum`, you tell Python: *"These variables are constants. They belong together, and they should never be changed while the program is running."*

#### 2. Architectural Benefits: 

  __Using an `Enum` to manage the UI color palettes provides three massive technical advantages:__

* **Decoupling Logic from Aesthetics:** The pathfinder algorithms and the `Cell` rendering logic never need to know the actual ANSI string for "Red." They simply ask for `active_theme.value`. This separates the mathematical grid logic from the visual presentation layer.
* 
* **Type Safety:** If a function expects a `Theme` object, passing a random string like `"blue"` will fail immediately, preventing runtime rendering errors.
* 
* **Iteration:** Enums in Python are iterable. When the user presses the `3` key to "Cycle Random Theme", the application can simply cast the Enum to a list (`list(Themes)`) and pick the next one. making it possible to scale it in a simple way 

## 3. Implementation in the Themes Section

* In the application, the `Themes` (or `ColorsMaze`) Enum acts as the central registry for all visual styles. Each member of the Enum represents a distinct visual theme, and its value is a dictionary containing the specific ANSI Escape Codes for the colors of that theme .

####  Architecture:

```python
from enum import Enum

class ColorsMaze(Enum):
	BG_BLACK = "\033[40m"
	BG_RED = "\033[41m"
	BG_GREEN = "\033[42m"
	BG_YELLOW = "\033[43m"
	BG_BLUE = "\033[44m"
		.
		.
		.
	RESET = "\033[0m"


class Themes(Enum):
    # Standard terminal theme
  CYBERPUNK = {
		"logo": ColorsMaze.BG_BRIGHT_MAGENTA,
		"walls": ColorsMaze.BG_BLACK,
		"path": ColorsMaze.BG_BLUE,
		"entry": ColorsMaze.TXT_BOLD_YELLOW,
		"exit": ColorsMaze.TXT_BOLD_PINK
	}
```

