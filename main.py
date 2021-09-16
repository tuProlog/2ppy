from tuprolog.core import *
from tuprolog.core.operators import *
from tuprolog.solve import *
from tuprolog.theory.parsing import *

parser = clauses_parser(with_default_operators=True, operators=operator_set(operator('f', XFX, 100)))

theory = parser.parseTheory(
    """
    male(james1). male(charles1). male(charles2). male(james2). male(george1).

    female(catherine). female(elizabeth). female(sophia).

    parent(charles1, james1). parent(elizabeth, james1). parent(charles2, charles1). parent(catherine, charles1).
    parent(james2, charles1). parent(sophia, elizabeth). parent(george1, sophia).

    grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
    """
)

solver = Solver.getClassic().solverWithDefaultBuiltins(theory)

query = struct("grandparent", var("X"), var("Y"))

solutions = solver.solve(query)
print(solutions)
for solution in solutions:
    print(solution)

variables = query.getVariables()
print(variables)
for variable in variables:
    print(variable)
