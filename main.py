from tuprolog import Info
from tuprolog.core import *
from tuprolog.solve import *
from tuprolog.theory.parsing import *

parser = ClausesParser.getWithDefaultOperators()

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

query = Struct.of("grandparent", Var.of("X"), Var.of("Y"))

for solution in solver.solve(query):
    print(solution)
