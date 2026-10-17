from collections.abc import Callable, Iterable

from tuprolog.core import Struct
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import Solution, Solver, signature
from tuprolog.solve.exception import ResolutionException
from tuprolog.solve.library import library
from tuprolog.solve.primitive import SolveRequest, SolveResponse, primitive
from tuprolog.solve.prolog import prolog_solver

ErrorFactory = Callable[[SolveRequest], ResolutionException]


def solver_raising(**factories: ErrorFactory) -> Solver:
    """A solver where each `name/0` primitive raises (from Python) the error built by `factories[name]`."""

    def raising(factory: ErrorFactory):
        def solve(request: SolveRequest) -> Iterable[SolveResponse]:
            raise factory(request)

        return primitive(solve)

    primitives = {signature(name, 0): raising(factory) for name, factory in factories.items()}
    return prolog_solver(libraries=library("raising", primitives=primitives))


def solve_once(solver: Solver, query: str | Struct) -> Solution:
    return solver.solve_once(parse_struct(query) if isinstance(query, str) else query)
