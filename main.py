from tuprolog.core.operators import DEFAULT_OPERATORS
from tuprolog.dsl.core import logic, lp, logic_programming


@logic(operators=DEFAULT_OPERATORS)
def my_term():
    return "f(X)"


@logic
def my_term2():
    return "f(Y)"


@lp
def my_term3():
    return "f(Z)"


@logic_programming(operators=DEFAULT_OPERATORS)
def my_term4():
    return "f(Y)"


print(my_term())
print(my_term2())
print(my_term3())
print(my_term4())
print(lp@'f(1, a)')
