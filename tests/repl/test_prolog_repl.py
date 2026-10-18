import io

import pytest

from tuprolog.core.parsing import parse_struct
from tuprolog.repl import PrologREPL
from tuprolog.solve import Solver
from tuprolog.solve.problog import problog_solver
from tuprolog.solve.prolog import prolog_solver
from tuprolog.theory.parsing import parse_theory

from .test_repl import BoundedInput

INTRO_END = 'Type ":exit" to exit.\n'


def run(text: str, solver: Solver | None = None, name: str = "prolog") -> str:
    """Runs a REPL on `text`, returning its output after the intro."""
    if solver is None:
        solver = prolog_solver(mutable=True)
    stdout = io.StringIO()
    PrologREPL(solver, name, stdin=BoundedInput(text), stdout=stdout).cmdloop()
    output = stdout.getvalue()
    assert INTRO_END in output
    return output.split(INTRO_END, 1)[1]


def test_intro_and_prompt():
    stdout = io.StringIO()
    repl = PrologREPL(prolog_solver(), "prolog", stdin=BoundedInput(""), stdout=stdout)
    assert repl.prompt == "prolog>"
    assert repl.name == "prolog"
    repl.cmdloop()
    output = stdout.getvalue()
    assert "Welcome to the Prolog REPL." in output
    assert output.endswith("prolog>")


def test_assert_and_query_with_several_solutions():
    output = run("p(1).\np(2).\n?- p(X).\n")
    assert output == ("\nprolog>prolog>prolog>yes: p(1)\n    X = 1\nyes: p(2)\n    X = 2\nprolog>")


def test_query_against_static_kb():
    output = run("?- p(X, Y).\n", prolog_solver(static_kb=parse_theory("p(a, b).")))
    assert "yes: p(a, b)\n    X = a\n    Y = b\n" in output


def test_several_clauses_on_one_line():
    assert "yes: a(1)\n    X = 1\nyes: a(2)\n    X = 2\n" in run("a(1). a(2).\n?- a(X).\n")


def test_multi_line_clause():
    output = run("q(X) :-\n  X = 3.\n?- q(Y).\n")
    assert output == "\nprolog>...>prolog>yes: q(3)\n    Y = 3\nprolog>"


def test_multi_line_query():
    output = run("?- X = f(\n  a).\n")
    assert "...>" in output
    assert "X = f(a)" in output


@pytest.mark.parametrize("blank", ["", "   "], ids=["empty", "spaces"])
def test_blank_lines_are_ignored(blank):
    output = run(f"{blank}\n{blank}\n?- true.\n")
    assert output.startswith("\nprolog>prolog>prolog>yes: true")
    assert "...>" not in output


def test_blank_line_does_not_repeat_last_command():
    solver = prolog_solver(mutable=True)
    output = run("?- assertz(c(1)).\n\n?- c(X).\n", solver)
    assert output.count("yes: c(1)") == 1


@pytest.mark.parametrize("text", ["?- t(X). \n", "t(1).\t\n?- t(X).\n"])
def test_trailing_whitespace_after_full_stop(text):
    output = run(text, prolog_solver(static_kb=parse_theory("t(1).")))
    assert "yes: t(1)\n    X = 1\n" in output
    assert "...>" not in output


def test_multi_line_clause_with_blank_line_inside():
    assert "yes: r(1)\n    Z = 1\n" in run("r(X) :-\n\n X = 1.\n?- r(Z).\n")


def test_prompt_while_clause_is_incomplete():
    repl = PrologREPL(prolog_solver(), "prolog", stdin=BoundedInput(""), stdout=io.StringIO())
    assert repl.precmd("q(X) :-") == ""
    assert repl.prompt == "...>"
    assert repl.precmd("X = 1.") == "q(X) :-\nX = 1."
    assert repl.prompt == "prolog>"


def test_failing_query():
    assert run("?- fail.\n") == "\nprolog>no.\nprolog>"


def test_query_of_undefined_predicate_fails():
    assert "no." in run("?- undefined_predicate(1).\n")


def test_assert_then_query_with_assertz():
    output = run("?- assertz(z(1)).\n?- z(X).\n")
    assert "yes: assertz(z(1))" in output
    assert "yes: z(1)\n    X = 1\n" in output


def test_operators_are_pretty_printed():
    assert "    X = 1 + 2 * 3\n" in run("?- X = 1 + 2 * 3.\n")


def test_operators_declared_in_queries_are_used():
    output = run("?- op(700, xfx, ===>).\na ===> b.\n?- X ===> Y.\n")
    assert "Error" not in output
    assert "yes: a ===> b\n    X = a\n    Y = b\n" in output


def test_operator_clauses():
    output = run("p(X) :- X > 1, X < 3.\n?- p(2).\n?- p(5).\n")
    assert "yes: p(2)" in output
    assert "no." in output


@pytest.mark.parametrize(
    "text",
    ["p(.\n?- true.\n", "?- p(.\n?- true.\n"],
    ids=["clause", "query"],
)
def test_syntax_error_is_reported_and_repl_continues(text):
    output = run(text)
    assert "Error: Unexpected token '.' at 1:3; expected term" in output
    assert "yes: true" in output


def test_unterminated_quoted_literal_is_reported():
    output = run('?- "abc.\n')
    assert "Error: Unterminated quoted literal beginning at 1:1" in output
    assert "'<EOF>'" not in output


@pytest.mark.parametrize(
    "text, message",
    [
        ("?- X.\n", "Error: Expected Struct, got: X"),
        ("?- 1.\n", "Error: Expected Struct, got: 1"),
        ("1.\n", "Error: Expected Clause, got: 1"),
        ("X.\n", "Error: Expected Clause, got: X"),
    ],
)
def test_non_callable_input_is_reported(text, message):
    assert message in run(text + "?- true.\n")


def test_uncaught_exception_is_reported_with_stack_trace():
    output = run("?- throw(my).\n")
    assert "halt: Uncaught exception `my`\n    at ?- throw(my)\n" in output


def test_caught_exception():
    assert "    E = my\n" in run("?- catch(throw(my), E, true).\n")


def test_error_in_query_is_reported():
    output = run("?- assertz(foo :- 1).\n?- true.\n")
    assert "halt: " in output
    assert "`assertz/1` should be `clause`" in output
    assert "yes: true" in output


def test_rejected_clause_is_reported_and_repl_continues():
    output = run("foo :- 1.\n?- true.\n")
    assert "Error: ClauseDatabase can contain only well formed clauses" in output
    assert "yes: true" in output


@pytest.mark.parametrize("query", ["halt", "halt(1)"])
def test_halt_exits(query):
    stdin = BoundedInput(f"?- {query}.\n?- true.\n")
    stdout = io.StringIO()
    PrologREPL(prolog_solver(), "prolog", stdin=stdin, stdout=stdout).cmdloop()
    assert stdout.getvalue().endswith("prolog># goodbye.\n")
    assert stdin.readline() == "?- true.\n"


def test_help_lists_commands():
    output = run(":help\n")
    for command in ("assert", "exit", "help", "query"):
        assert command in output


@pytest.mark.parametrize(
    "command, doc",
    [
        ("exit", "Exit the REPL."),
        ("query", "Query the theory."),
        ("assert", "Asserts a clause, appending to the theory."),
    ],
)
def test_help_on_command(command, doc):
    assert f"{doc}\n" in run(f":help {command}\n")


def test_explicit_assert_and_query_commands():
    assert "yes: w(1)\n    X = 1\n" in run(":assert w(1).\n:query w(X).\n")


def test_unknown_command():
    assert "*** Unknown syntax: foo" in run(":foo\n")


def test_exit_stops_reading():
    stdin = BoundedInput(":exit\n?- true.\n")
    stdout = io.StringIO()
    PrologREPL(prolog_solver(), "prolog", stdin=stdin, stdout=stdout).cmdloop()
    assert "yes" not in stdout.getvalue()
    assert stdin.readline() == "?- true.\n"


def test_end_of_input_stops():
    assert run("") == "\nprolog>"


def test_end_of_input_drops_pending_clause():
    solver = prolog_solver(mutable=True)
    assert run("q(1)\n", solver) == "\nprolog>...>"
    assert solver.solve_once(parse_struct("q(1)")).is_no


def test_problog_repl():
    output = run("0.6::heads.\n?- heads.\n", problog_solver(mutable=True), "problog")
    assert output.startswith("\nproblog>")
    assert "yes: heads" in output


@pytest.mark.xfail(
    strict=True,
    reason="the ProbLog REPL solves queries non-probabilistically and never shows probabilities",
)
def test_problog_repl_shows_probabilities():
    output = run("0.6::heads.\n?- heads.\n", problog_solver(mutable=True), "problog")
    assert "0.6" in output


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt's EvaluationError raised by is/2 has no message: the REPL prints "
    "'halt: <no message>' instead of the error term",
)
def test_evaluation_error_is_described():
    output = run("?- X is 1 / 0.\n")
    assert "<no message>" not in output
    assert "evaluation_error(zero_divisor)" in output


@pytest.mark.xfail(
    strict=True,
    reason="2P-Kt's SolutionFormatter prints a whitespace-only line after solutions with an "
    "empty substitution (2P-Kt's own REPL prints 'yes.' via groundQueriesHaveBooleanSolution)",
)
def test_ground_solution_has_no_blank_line():
    output = run("?- true.\n")
    assert all(line.strip() for line in output.splitlines()[1:])


@pytest.mark.xfail(
    strict=True,
    reason="directives (':- goal.') are taken as ':'-prefixed REPL commands ('Unknown syntax')",
)
def test_directive():
    output = run(":- op(700, xfx, ===>).\na ===> b.\n?- X ===> Y.\n")
    assert "Unknown syntax" not in output
    assert "Y = b" in output
