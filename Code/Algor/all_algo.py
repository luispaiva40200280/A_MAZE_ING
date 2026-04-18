"""

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
