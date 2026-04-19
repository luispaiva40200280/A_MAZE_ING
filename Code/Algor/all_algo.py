"""
Centralized Algorithm Registry for the Maze Generator.

This module implements the Registry Design Pattern to manage, categorize, and
route all mathematical algorithms used within the application. By decoupling
the algorithm implementations from the core execution engine and user
interface, this registry enables dynamic algorithm selection,
seamless UI menu integration, and strict runtime validation
(e.g., preventing a solver from being used to construct a maze).

Components:
    AlgoMetadata (dataclass): A strongly-typed data structure storing the
        metadata for a single algorithm. It tracks the pretty-formatted
        display `name` (used by the terminal HUD), the `job` category
        ("construct" for maze generation, "solve" for pathfinding), and the
        `func` pointer (the callable executable for the algorithm itself).

    ALGORITHM_REGISTRY (Dict[str, AlgoMetadata]): The primary global dictionary
        acting as the single source of truth for all available algorithms. The
        keys are standardized configuration strings (e.g., "PRIMS", "BFS"),
        which are parsed directly from the user's `config.txt`.
"""
from dataclasses import dataclass
from typing import Callable, Dict, Any
from .prims import prims_algorithm
from .hunt_and_kill_algo import hunt_and_kill_algo
from .breadth_first_search import breadth_first_search


@dataclass
class AlgoMetadata:
    name: str
    job: str
    func: Callable[..., Any]


ALGORITHM_REGISTRY: Dict[str, AlgoMetadata] = {
    "PRIMS": AlgoMetadata(
        name="Prim's Algorithm",
        job="construct",
        func=prims_algorithm
    ),
    "HUNT_KILL": AlgoMetadata(
        name="Hunt & Kill",
        job="construct",
        func=hunt_and_kill_algo
    ),
    "BFS": AlgoMetadata(
        name="Breadth First Search",
        job="solve",
        func=breadth_first_search
    )
}
