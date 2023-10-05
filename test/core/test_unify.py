import unittest
from tuprolog.core import scope
from tuprolog.unify import DEFAULT_UNIFICATOR
from tuprolog.jvmutils import Pair

class TestSubstitutionMerge(unittest.TestCase):
    def test_merge_with(self):
        s = scope("X", "Y", "Z")
        base = s.unifier_of(
            ("X", s["Y"]),
            ("Y", s["Z"]),
        )
        a = s.atom_of("a")

        for v_name, v in s.variables.items():
            assignment = s.unifier_of(Pair(v_name, a))
            self.assertEqual(
                s.unifier_of(
                    ("X", a),
                    ("Y", a),
                    ("Z", a),
                ),
                DEFAULT_UNIFICATOR.merge(base, assignment),
            )
            self.assertEqual(
                s.unifier_of(
                    ("X", a),
                    ("Y", a),
                    ("Z", a),
                ),
                DEFAULT_UNIFICATOR.merge(assignment, base),
            )
