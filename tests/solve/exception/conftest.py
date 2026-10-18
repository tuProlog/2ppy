import pytest

# NB: tuprolog is imported lazily, inside the fixtures. When this directory is passed to pytest,
# this conftest is loaded before pytest's faulthandler plugin is enabled: importing tuprolog here
# would start the JVM first, and faulthandler would then take over the SIGSEGV signals the JVM
# uses internally, randomly crashing the process.


@pytest.fixture(scope="session")
def context():
    """A real ExecutionContext, captured from within a Python primitive while solving `capture`."""
    from tuprolog.core import atom
    from tuprolog.solve import signature
    from tuprolog.solve.library import library
    from tuprolog.solve.primitive import primitive
    from tuprolog.solve.prolog import prolog_solver

    captured = []

    def capture(request):
        captured.append(request.context)
        yield request.reply_success()

    solver = prolog_solver(
        libraries=library("capture", primitives={signature("capture", 0): primitive(capture)})
    )
    assert solver.solve_once(atom("capture")).is_yes
    return captured[0]


@pytest.fixture(scope="session")
def procedure():
    from tuprolog.solve import signature

    return signature("foo", 2)
