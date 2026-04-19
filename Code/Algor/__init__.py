"""
Core algorithmic constants for the Maze Generator.
Contains coordinate math deltas and letter mappings used by both
constructors and pathfinding solvers.
"""
DIRECTIONS = [
    (0, -1, 1, 4),  # North 0001
    (1, 0, 2, 8),  # East
    (0, 1, 4, 1),  # South
    (-1, 0, 8, 2),  # West
]

LETTER_MAP = {
    1: 'N',
    2: 'E',
    4: 'S',
    8: 'W'
}
