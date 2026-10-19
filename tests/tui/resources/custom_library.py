"""A library for the `--library FILE.py:NAME` option of the terminal IDE's tests."""

from tuprolog.solve.library import library
from tuprolog.theory.parsing import parse_theory


def greetings():
    return library("test.greetings", clauses=parse_theory("greeting(hello). greeting(ciao)."))


NOT_A_LIBRARY = 42
