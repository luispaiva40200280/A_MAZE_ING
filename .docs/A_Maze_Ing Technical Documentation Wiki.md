> **“A labyrinth is not a place to be lost, but a path to be found.”**

## 1. Project Overview
* [[Brief explanation of the project]]: The core objectives, bitwise hexadecimal representation, and the application execution flowchart.

## 2. The Core Engine (Algorithms)
The mathematical brain of the application. These modules handle the manipulation of the 2D matrix.

* [[Core Engine The Algorithms Registry|Algorithms]]: Master registry of constructor logic.
    * [[Prim's Algorithm (Randomized Maze Generation)]]
    * [[Hunt and Kill Algorithm The Dual-Phase Carver]]
    * [[BFS - breadth first search]]

## 3. The Presentation Layer (UI/UX)
How the underlying grid is translated into a human-readable, responsive interface.
* [[Terminal an UI & UX experience]]: The dynamic viewport, 4x2 cell rendering, and animation.

* [[Themes]]: How the `Enum` class safely manages color palettes and separates aesthetics from math.

## 4. Low-Level System Infrastructure

+ The UNIX-specific modules that allow the terminal to behave like a graphical canvas without tearing or blocking.

* [[How ANSI codes are used in the project]]: Absolute cursor positioning, buffer management, and color rendering.

* [[TTY & Terminos]]: Unbuffered input (`sys.stdin`), suppressing echo(`sys.stdout.flush()`), and terminal state safety.