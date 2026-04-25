+ Like explain in the [[Terminal an UI & UX experience]] page when a process is running in the terminal by default, when a user presses a key, the terminal's line immediately prints (echoes) that character to standard output to provide visual feedback. To make it so the terminal does not visually corrupt the  ASCII canvas with random input characters the application actively suppress this behavior.

* #### How:
	* THE `sys` module:
		* Standard UNIX terminals are "line-buffered," meaning they hold text in memory and refuse to paint it to the physical monitor until they receive a newline character (`\n`).
		* During the "dust" animation the program updates specific ANSI coordinate cells rapidly using `print(..., end="")`. Because there is no newline, the terminal automatically buffers the frames. `sys.stdout.flush()` forcefully empties the standard output buffer, commanding the operating system to paint the modified characters instantly.
		* In the menu of the maze the `sys.stdin` to capture raw keystrokes instantly without forcing the user to hit the `Enter` key
	* **The `termios` Interface:**
		* The application utilizes a custom Python decorator, `@supress_terminal_echos`, to safely modify the default behavior of the terminal. Rather than permanently altering the system, the decorator retrieves the file descriptor for standard input (`sys.stdin`) and extracts its current attribute matrix using the `termios` library. It then applies a bitwise mask to explicitly disable the `ECHO` flag. Crucially, the decorator wraps the execution of the target function inside a `try/finally` block. This guarantees that the exact moment the function completes—or even if the program encounters a fatal exception—the original terminal settings are instantly restored, preventing the user from being trapped in a "blind" terminal.
		* ![[terminal_echos_supressing.png]]


 - #### The Usage and integration of both modules:
	 - The `termios` library needs a specific file descriptor to know exactly which system stream to modify. The `sys.stdin` object represents the standard input stream. Your `@supress_terminal_echos` decorator extracts the exact file descriptor from `sys.stdin` (using `sys.stdin.fileno()`) to explicitly flip the `ECHO` bitmask to `0`.
    
	- **Why it matters:** This allows the application to step outside of Python's high-level abstractions and interface directly with the low-level UNIX layer handling keyboard hardware inputs.

>> Those libraries only work on Unix base systems (Mac & Linux)
