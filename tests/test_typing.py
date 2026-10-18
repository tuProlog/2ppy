"""2PPy ships type information (`py.typed`): type checkers check user code against its API."""

from importlib.resources import files

from mypy import api

USAGE = """
from tuprolog.core import struct, to_python
from tuprolog.solve import signature
from tuprolog.solve.prolog import prolog_solver
"""


def test_py_typed_is_shipped():
    assert files("tuprolog").joinpath("py.typed").is_file()


def check(tmp_path, code: str) -> tuple[str, int]:
    module = tmp_path / "usage.py"
    module.write_text(USAGE + code)
    stdout, _, status = api.run(
        [str(module), "--cache-dir", str(tmp_path / ".mypy_cache"), "--no-error-summary"]
    )
    return stdout, status


def test_correct_usage_type_checks(tmp_path):
    stdout, status = check(tmp_path, 'struct("f", "a", 1)\nsignature("f/1")\nprolog_solver()\n')
    assert status == 0, stdout


def test_wrong_usage_is_reported(tmp_path):
    # JVM types are opaque (Any) to type checkers, Python ones are checked
    stdout, status = check(tmp_path, 'prolog_solver(mutable="no")\n')
    assert status == 1
    assert 'Argument "mutable" to "prolog_solver" has incompatible type "str"' in stdout
