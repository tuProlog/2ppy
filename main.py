from tuprolog.core import *
from tuprolog.core.parsing import *
from tuprolog.core.visitors import AbstractTermVisitor

formatter = TermFormatter.prettyExpressions()


def is_sum(term: Struct):
    return term.getArity() == 2 and term.getFunctor() == '+'


def is_mult(term: Struct):
    return term.getArity() == 2 and term.getFunctor() == '*'


def is_negative(term: Term):
    if isinstance(term, Integer):
        return term < Integer.ZERO
    if isinstance(term, Real):
        return term < Real.ZERO
    if isinstance(term, Struct) and is_mult(term):
        return any(map(is_negative, term.getArgs()))
    return False


def is_zero(term: Term):
    if isinstance(term, Integer):
        return term == Integer.ZERO
    if isinstance(term, Real):
        return term == Real.ZERO
    if isinstance(term, Struct) and is_mult(term):
        return any(map(is_zero, term.getArgs()))
    return False


def absolute(term: Term):
    if is_negative(term):
        if isinstance(term, Numeric):
            return numeric(term.getValue().unaryMinus())
        return struct(term.getFunctor(), map(absolute, term.getArgs()))
    return term


def is_sum(term: Struct):
    return term.getArity() == 2 and term.getFunctor() == '+'


def foldr(accumulator, iterable, default=None):
    items = list(iterable)
    if len(items) == 0:
        return default
    current = items[-1]
    items.pop(-1)
    while len(items) > 0:
        current = accumulator(items[-1], current)
        items.pop(-1)
    return current


class Simplifier(AbstractTermVisitor):
    def defaultValue(self, term):
        return term

    def visitStruct(self, term):
        args = term.getArgs()
        if is_sum(term):
            left, right = args
            if is_mult(right):
                if is_negative(right):
                    return struct('-', map(absolute, args))
            right_left, right_right = right
            if is_sum(right) and is_negative(right_left):
                return struct(
                    '-',
                    left,
                    struct(right.getFunctor(), absolute(right_left), right_right).accept(self)
                )
        return struct(term.getFunctor(), [a.accept(self) for a in args])


features = map(var, ["A", 'B', 'C', 'D', 'E', 'F'])
weights = map(real, [2.5, -3.4, -0.09, 0.2, 0.0, -2.0])


x = zip(features, weights)
x = filter(lambda fw: not is_zero(fw[1]), x)
x = map(lambda fw: struct('*', fw[1], fw[0]), x)
x = foldr(lambda a, b: struct('+', a, b), x)
x = struct('is', var('Y'), x)

print(formatter.format(x))
print(formatter.format(x.accept(Simplifier())))