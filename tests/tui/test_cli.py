"""Tests for the command line of the terminal IDE: what it parses, and what it rejects."""

from pathlib import Path

import pytest

from tuprolog import tui
from tuprolog.tui import JvmGuiBridge, Startup, parse_command_line
from tuprolog.tui._cli import environment_arguments

RESOURCES = Path(__file__).parent / "resources"


def test_defaults():
    bridge, startup = parse_command_line([])
    assert isinstance(bridge, JvmGuiBridge)
    assert (bridge.timeout, bridge.flags, bridge.scheduling) == (5.0, {}, "concurrent")
    assert startup == Startup()
    assert startup.page_count == 1


def test_everything(tmp_path):
    existing, missing, facts, stdin = (tmp_path / n for n in ["a.pl", "b.pl", "kb.pl", "in"])
    existing.write_text("a.", encoding="utf-8")
    facts.write_text("d(1).", encoding="utf-8")
    stdin.write_text("input.", encoding="utf-8")
    bridge, startup = parse_command_line(
        [
            str(existing),
            str(missing),
            "-t",
            "t.",
            "-q",
            "q",
            "-s",
            "hundred",
            "--stdin-file",
            str(stdin),
            "-d",
            str(facts),
            "-f",
            "unknown=fail",
            "--flag",
            "occurs_check = true",
            "--timeout",
            "2.5",
            "--scheduling",
            "single",
            "--dialect",
            "problog",
        ]
    )
    assert startup == Startup(
        documents=((existing.absolute(), "a."), (missing.absolute(), "")),
        theory="t.",
        query="q",
        stdin="input.",
        solve="HUNDRED",
    )
    assert startup.page_count == 3
    assert bridge.flags == {"unknown": "fail", "occurs_check": "true"}
    assert (bridge.timeout, bridge.scheduling) == (2.5, "single")
    assert str(bridge.profiles[0].display_name) == "ProbLog"


def test_solve_defaults_to_one():
    assert parse_command_line(["-s"])[1].solve == "ONE"
    assert parse_command_line(["--solve", "all"])[1].solve == "ALL"


@pytest.mark.parametrize(
    "argv, message",
    [
        (["-f", "unknown"], "expected NAME=VALUE"),
        (["-f", "unknown=f("], ""),
        (["--timeout", "0"], "timeout must be positive"),
        (["-d", "missing.pl"], "missing.pl"),
        (["--stdin-file", "missing.txt"], "missing.txt"),
        (["-l", "nothing"], "expected MODULE:NAME"),
        (["-l", "no_such_module_xyz:lib"], "no_such_module_xyz"),
        (["-l", "missing.py:lib"], "no such file"),
        ([f"-l={RESOURCES / 'custom_library.py'}:absent"], "has no 'absent'"),
        ([f"-l={RESOURCES / 'custom_library.py'}:NOT_A_LIBRARY"], "is not a library"),
        (["--unificator", "tuprolog:__version__"], "is not a unificator"),
        (["--dialect", "lisp"], "invalid choice"),
        (["--stdin", "a", "--stdin-file", "b"], "not allowed with"),
        (["-s", "every"], "invalid choice"),
    ],
)
def test_invalid_arguments(capsys, argv, message):
    with pytest.raises(SystemExit) as exit_info:
        parse_command_line(argv)
    assert exit_info.value.code == 2
    assert message in capsys.readouterr().err


def test_dynamic_kb_syntax_errors_are_reported(tmp_path, capsys):
    broken = tmp_path / "broken.pl"
    broken.write_text("p(", encoding="utf-8")
    with pytest.raises(SystemExit):
        parse_command_line(["-d", str(broken)])
    assert "2ppy-tui: error:" in capsys.readouterr().err


@pytest.mark.parametrize(
    "option, expected", [("--help", "--dynamic-kb"), ("--version", "2ppy-tui")]
)
def test_help_and_version(capsys, option, expected):
    with pytest.raises(SystemExit) as exit_info:
        parse_command_line([option])
    assert exit_info.value.code == 0
    assert expected in capsys.readouterr().out


def test_main_runs_the_ide(monkeypatch):
    runs = []
    monkeypatch.setattr(tui.PrologTui, "run", lambda self: runs.append(self))
    tui.main(["-q", "q"])
    assert runs[0].startup.query == "q" and isinstance(runs[0].bridge, JvmGuiBridge)


def test_environment_variables_stand_for_options(tmp_path):
    theory = tmp_path / "t.pl"
    environ = {
        "TWOPPY_FILES": str(theory),
        "TWOPPY_QUERY": "p(X)",
        "TWOPPY_SOLVE": "ten",
        "TWOPPY_FLAG": "unknown=fail 'occurs_check = true'",
        "TWOPPY_NO_BUILTINS": "yes",
        "TWOPPY_OOP_ALLOW_PRIVATE": "false",
        "TWOPPY_TIMEOUT": "",  # ignored
        "OTHER": "x",
    }
    bridge, startup = parse_command_line([], environ)
    assert startup.documents == ((theory.absolute(), ""),)
    assert (startup.query, startup.solve, bridge.timeout) == ("p(X)", "TEN", 5.0)
    assert bridge.flags == {"unknown": "fail", "occurs_check": "true"}
    # the command line comes after: it overrides single values, and adds files and repeated ones
    bridge, startup = parse_command_line(["-q", "q", "b.pl", "-f", "x=1"], environ)
    assert startup.query == "q" and len(startup.documents) == 2
    assert bridge.flags == {"unknown": "fail", "occurs_check": "true", "x": "1"}


def test_environment_variables_keep_backslashes():
    environ = {"TWOPPY_FILES": r"C:\a\b.pl 'C:\c d\e.pl'", "TWOPPY_DYNAMIC_KB": r"x\y.pl"}
    assert environment_arguments(environ) == [
        r"C:\a\b.pl",
        r"C:\c d\e.pl",
        "--dynamic-kb",
        r"x\y.pl",
    ]


def test_environment_variables_are_read_by_default(monkeypatch):
    monkeypatch.setenv("TWOPPY_THEORY", "p(1).")
    assert parse_command_line([])[1].theory == "p(1)."
