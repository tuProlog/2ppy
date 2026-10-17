import unittest
from tuprolog.core import struct, var
from tuprolog.theory.parsing import parse_theory
from tuprolog.solve import solve_options
from tuprolog.solve.library import library, libraries, Runtime
from tuprolog.solve.sideffects import load_library, update_library, add_libraries, reset_libraries
from tuprolog.solve.prolog import prolog_solver


def aliases(runtime):
    return {str(alias) for alias in runtime.keySet()}


class TestLibraries(unittest.TestCase):

    def test_empty_libraries(self):
        self.assertEqual(set(), aliases(libraries()))

    def test_libraries_aggregates_into_runtime(self):
        runtime = libraries(library("a"), [library("b")], c=library())
        self.assertIsInstance(runtime, Runtime)
        self.assertEqual({"a", "b", "c"}, aliases(runtime))

    def test_solver_accepts_runtime_or_library(self):
        self.assertTrue({"a", "b"} <= aliases(prolog_solver(libraries=libraries(library("a"), library("b"))).libraries))
        self.assertIn("a", aliases(prolog_solver(libraries=library("a")).libraries))


class TestLibrarySideEffects(unittest.TestCase):

    def test_load_library_applies_alias(self):
        self.assertEqual("x", str(load_library("x", library("a")).library.alias))

    def test_update_library_applies_alias(self):
        self.assertEqual("y", str(update_library("y", library("a")).library.alias))

    def test_add_and_reset_libraries(self):
        self.assertEqual({"a", "b"}, aliases(add_libraries(library("a"), library("b")).libraries))
        self.assertEqual({"a"}, aliases(reset_libraries(library("a")).libraries))


class TestSolverAdapters(unittest.TestCase):

    def setUp(self):
        self.solver = prolog_solver(static_kb=parse_theory("p(1). p(2)."))

    def test_solve_once(self):
        self.assertEqual("p(1)", str(self.solver.solve_once(struct("p", var("X"))).solved_query))

    def test_solve_options_mapping(self):
        options = solve_options(lazy=False, custom={"key": 1})
        self.assertFalse(options["lazy"])
        self.assertTrue(options["eager"])
        self.assertIn("key", options.options)
        with self.assertRaises(KeyError):
            options["missing"]
