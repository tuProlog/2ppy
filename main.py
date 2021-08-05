import jpype
import jpype.imports

jpype.startJVM(classpath = ['libs/*'])

from it.unibo.tuprolog import Info
from it.unibo.tuprolog.core import Struct
from it.unibo.tuprolog.core import Atom
from it.unibo.tuprolog.core import Integer
from it.unibo.tuprolog.core import Var
from it.unibo.tuprolog.solve import Solver
from it.unibo.tuprolog.theory.parsing import ClausesParser

print("2P-Kt", Info.VERSION)

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

for solution in solver.solve(query).iterator():
    print(solution)
