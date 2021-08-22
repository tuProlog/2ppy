import unittest
from tuprolog import *
from tuprolog.core import *

class TestTermCreation(unittest.TestCase):

    def test_simple_terms_creation(self):
        atom = Atom.of('a')
        integer = Integer.of(1)
        real = Real.of(1.2)
        var = Var.of("X")
        true = Truth.of(True)
        false = Truth.of(False)
        fail = Truth.FAIL

        self.assertEqual(atom.getValue(), 'a')
        self.assertEqual(integer.getValue().toInt(), 1)
        self.assertEqual(real.getValue().toDouble(), 1.2)
        self.assertEqual(var.getName(), 'X')
        self.assertEqual(true.getValue(), 'true')
        self.assertEqual(false.getValue(), 'false')
        self.assertEqual(fail.getValue(), 'fail')

    def test_struct_creation(self):
        atom = Atom.of('a')
        integer = Integer.of(1)
        real = Real.of(1.2)

        struct = Struct.of('f', atom, integer, real)
        self.assertEqual(struct.getFunctor(), 'f')
        self.assertEqual(struct.getArity(), 3)
        self.assertEqual(struct.getArgAt(0), atom)
        self.assertEqual(struct.getArgAt(1), integer)
        self.assertEqual(struct.getArgAt(2), real)

        struct2 = Struct.of('f', jiterable([atom, integer, real]))
        self.assertEqual(struct, struct2)

        
