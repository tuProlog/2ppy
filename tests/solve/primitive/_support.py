"""Helpers shared by the tests of the Python API for extending solvers."""

from collections.abc import Callable, Iterable

from tuprolog.core import Struct, Term, atom, struct
from tuprolog.core.parsing import parse_struct
from tuprolog.solve import Signature, Solution, Solver, signature
from tuprolog.solve.library import Library, library
from tuprolog.solve.primitive import SolveRequest, SolveResponse, primitive
from tuprolog.solve.prolog import prolog_solver

CAPTURE = "capture"


class RequestCapturer:
    """A library whose `capture/N` primitives (N = 0..4) record the request they receive."""

    def __init__(self) -> None:
        self.requests: list[SolveRequest] = []
        self.library: Library = library(
            alias="test.capture",
            primitives={signature(CAPTURE, n): primitive(self._capture) for n in range(5)},
        )
        self.solver = prolog_solver(libraries=self.library)

    def _capture(self, request: SolveRequest) -> Iterable[SolveResponse]:
        self.requests.append(request)
        yield request.reply_success()

    def request(self, *arguments: Term) -> SolveRequest:
        """Returns the request a solver issues to a primitive invoked with the given arguments."""
        goal = struct(CAPTURE, *arguments) if arguments else atom(CAPTURE)
        solutions = list(self.solver.solve(goal))
        assert len(solutions) == 1 and solutions[0].is_yes, solutions
        return self.requests[-1]


def goal_of(goal: str | Struct) -> Struct:
    return parse_struct(goal) if isinstance(goal, str) else goal


def solve_all(solver: Solver, goal: str | Struct) -> list[Solution]:
    return list(solver.solve(goal_of(goal)))


def solve_once(solver: Solver, goal: str | Struct) -> Solution:
    return solver.solve_once(goal_of(goal))


def bindings(solutions: Iterable[Solution], variable: str) -> list[str]:
    """The (stringified) values a variable takes in each positive solution."""
    result = []
    for solution in solutions:
        assert solution.is_yes, solution
        for var, value in solution.substitution.items():
            if var.name == variable:
                result.append(str(value))
    return result


def error_of(solution: Solution) -> Term:
    """The error term carried by a halted solution."""
    assert solution.is_halt, solution
    return solution.get_exception().error_struct


def single_primitive_library(
    name: str,
    arity: int,
    implementation: Callable[[SolveRequest], Iterable[SolveResponse]],
    alias: str = "test.single",
) -> Library:
    return library(alias=alias, primitives={signature(name, arity): primitive(implementation)})


def solver_with_primitive(
    name: str,
    arity: int,
    implementation: Callable[[SolveRequest], Iterable[SolveResponse]],
    **kwargs,
) -> Solver:
    return prolog_solver(libraries=single_primitive_library(name, arity, implementation), **kwargs)


__all__ = [
    "CAPTURE",
    "RequestCapturer",
    "Signature",
    "bindings",
    "error_of",
    "goal_of",
    "single_primitive_library",
    "solve_all",
    "solve_once",
    "solver_with_primitive",
]
