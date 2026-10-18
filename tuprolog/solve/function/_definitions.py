"""The JVM types of logic functions, re-exported by `tuprolog.solve.function`."""

import it.unibo.tuprolog.solve.function as _function  # type: ignore
import jpype.imports  # noqa: F401
from jpype import JImplements, JOverride

from tuprolog import logger

__all__ = [
    "AbstractLogicFunction",
    "ArithmeticUtilsKt",
    "Compute",
    "ComputeRequest",
    "ComputeResponse",
    "LogicFunction",
]


LogicFunction = _function.LogicFunction
"""A logic function: computes the result of an operation in arithmetic expressions.

Its only method is `compute(request)`, taking a `ComputeRequest` and returning a
`ComputeResponse`. Create logic functions with `function` or `logic_function`, or by subclassing
`AbstractLogicFunction`.
"""


Compute = _function.Compute
"""The JVM base class of compute requests and responses.

It nests them as `Compute.Request` (`ComputeRequest`) and `Compute.Response` (`ComputeResponse`).
"""


ArithmeticUtilsKt = _function.ArithmeticUtilsKt
"""The JVM class of 2P-Kt's expression evaluation functions.

Its static methods are wrapped by `eval_as_expression` and `eval_as_arithmetic_expression`.
"""


ComputeRequest = Compute.Request
"""A request to compute a logic function.

Members: `signature`, `arguments` (the evaluated arguments, a list of terms), `context` (the
`tuprolog.solve.ExecutionContext` of the solver), `query` (the expression, i.e. the struct of the
signature and arguments), `request_issuing_instant`, `execution_max_duration` (in
milliseconds), and `reply_with(result)`, returning the `ComputeResponse` with `result`. Create
requests with `compute_request`.
"""


ComputeResponse = Compute.Response
"""The response of a logic function, holding its `result`, a term.

Create responses with `compute_response`, or `ComputeRequest.reply_with`.
"""


@JImplements(LogicFunction)
class AbstractLogicFunction:
    """A base class for logic functions written in Python: subclasses implement `compute`.

    Examples:
        >>> from tuprolog.core import integer
        >>> from tuprolog.solve.library import library
        >>> from tuprolog.solve.prolog import prolog_solver
        >>> class Arity(AbstractLogicFunction):
        ...     def compute(self, request):
        ...         return request.reply_with(integer(len(request.arguments)))
        >>> solver = prolog_solver(libraries=library("my.lib", functions={"arity/3": Arity()}))
        >>> solver.solve_once("X is arity(a, b, c)")["X"]
        3
    """

    @JOverride
    def compute(self, request: ComputeRequest) -> ComputeResponse:
        """Computes the result of the function for `request`.

        Args:
            request: The compute request, with the evaluated arguments.

        Returns:
            The compute response, holding the result.

        Raises:
            NotImplementedError: Unless overridden by subclasses.
        """
        raise NotImplementedError()


logger.debug("Loaded JVM classes from it.unibo.tuprolog.solve.function.*")
