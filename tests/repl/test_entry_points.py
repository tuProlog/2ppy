import builtins
import code
import os
import re
import runpy
import subprocess
import sys

import pytest

import tuprolog.core
import tuprolog.solve.exception.error
import tuprolog.solve.primitive
import tuprolog.solve.prolog
import tuprolog.theory

from .test_repl import BoundedInput

TIMEOUT = 300  # seconds: each subprocess starts its own JVM


def run_module(module: str, stdin: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", module],
        input=stdin,
        capture_output=True,
        check=False,
        text=True,
        timeout=TIMEOUT,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


@pytest.fixture(scope="module")
def shell_namespace():
    """The namespace `python -m tuprolog` hands to code.interact (run in-process)."""
    captured = {}
    patcher = pytest.MonkeyPatch()
    patcher.setattr(code, "interact", lambda local=None, **_: captured.update(local))
    try:
        runpy.run_module("tuprolog.__main__", run_name="__main__")
    finally:
        patcher.undo()
    return captured


@pytest.mark.parametrize(
    "name, module",
    [
        ("struct", tuprolog.core),
        ("var", tuprolog.core),
        ("Struct", tuprolog.core),
        ("Atom", tuprolog.core),
        ("Var", tuprolog.core),
        ("Integer", tuprolog.core),
        ("Clause", tuprolog.core),
        ("rule", tuprolog.core),
        ("primitive", tuprolog.solve.primitive),
        ("prolog_solver", tuprolog.solve.prolog),
        ("theory", tuprolog.theory),
        ("DomainError", tuprolog.solve.exception.error),
        ("domain_error_for_term", tuprolog.solve.exception.error),
    ],
)
def test_shell_exposes_the_api(shell_namespace, name, module):
    assert shell_namespace[name] is getattr(module, name)


def test_shell_can_solve(shell_namespace):
    ns = shell_namespace
    solver = ns["prolog_solver"](static_kb=ns["parse_theory"]("p(1)."))
    assert solver.solve_once(ns["parse_struct"]("p(X)")).is_yes


@pytest.mark.parametrize(
    "name", ["type", "TypeError", "SyntaxError", "SystemError", "PermissionError", "Warning"]
)
def test_shell_keeps_builtins(shell_namespace, name):
    assert shell_namespace.get(name, getattr(builtins, name)) is getattr(builtins, name)


@pytest.mark.parametrize(
    "module, solver_name, text, expected",
    [
        ("tuprolog.repl.prolog", "prolog", "p(1).\n?- p(X).\n", "yes: p(1)\n    X = 1\n"),
        ("tuprolog.repl.problog", "problog", "0.5::a.\n?- a.\n", "yes: a"),
    ],
)
@pytest.mark.filterwarnings("ignore:.*found in sys.modules:RuntimeWarning")
def test_repl_modules_in_process(monkeypatch, capsys, module, solver_name, text, expected):
    monkeypatch.setattr(sys, "stdin", BoundedInput(text))
    runpy.run_module(module, run_name="__main__")
    output = capsys.readouterr().out
    assert f"Welcome to the {solver_name.title()} REPL." in output
    assert expected in output


def test_repl_prolog_subprocess():
    result = run_module("tuprolog.repl.prolog", "p(1).\np(2).\n?- p(X).\n:exit\n")
    assert result.returncode == 0, result.stderr
    assert "Welcome to the Prolog REPL." in result.stdout
    assert "yes: p(1)\n    X = 1\nyes: p(2)\n    X = 2\n" in result.stdout
    assert "Traceback" not in result.stderr


def test_repl_problog_subprocess():
    result = run_module("tuprolog.repl.problog", "0.5::a.\n?- a.\n")
    assert result.returncode == 0, result.stderr
    assert "Welcome to the Problog REPL." in result.stdout
    assert "yes: a" in result.stdout
    assert "Traceback" not in result.stderr


def test_shell_subprocess():
    result = run_module("tuprolog", "print(prolog_solver().solve_once(parse_struct('X = 1')))\n")
    assert result.returncode == 0, result.stderr
    assert re.search(r"substitution=\{X_\d+=1\}", result.stdout)
    assert "now exiting InteractiveConsole" in result.stderr
    assert "Traceback" not in result.stderr
