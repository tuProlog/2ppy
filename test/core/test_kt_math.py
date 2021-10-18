import unittest
from tuprolog import *
from tuprolog.core import *


class TestBigInteger(unittest.TestCase):

    def setUp(self):
        self.large_int = 1 << 64

    def assertSameStringRepresentation(self, expected, actual):
        self.assertEqual(str(expected), str(actual))

    def test_python_to_java(self):
        self.assertSameStringRepresentation(0, big_integer("0"))
        self.assertSameStringRepresentation(0, big_integer(0))
        self.assertSameStringRepresentation(1, big_integer("1"))
        self.assertSameStringRepresentation(1, big_integer(1))
        self.assertSameStringRepresentation(self.large_int, big_integer(self.large_int))
        self.assertSameStringRepresentation(-1, big_integer("-1"))
        self.assertSameStringRepresentation(-1, big_integer(-1))
        self.assertSameStringRepresentation(-self.large_int, big_integer(-self.large_int))
        self.assertSameStringRepresentation(0x16, big_integer("16", 16))
        self.assertSameStringRepresentation(-0x16, big_integer("-16", 16))

    def test_java_to_python(self):
        self.assertEquals(0, python_integer(big_integer("0")))
        self.assertEquals(0, python_integer(big_integer(0)))
        self.assertEquals(1, python_integer(big_integer("1")))
        self.assertEquals(1, python_integer(big_integer(1)))
        self.assertEquals(self.large_int, python_integer(big_integer(self.large_int)))
        self.assertEquals(-1, python_integer(big_integer("-1")))
        self.assertEquals(-1, python_integer(big_integer(-1)))
        self.assertEquals(-self.large_int, python_integer(big_integer(-self.large_int)))
        self.assertEquals(0x16, python_integer(big_integer("16", 16)))
        self.assertEquals(-0x16, python_integer(big_integer("-16", 16)))


if __name__ == '__main__':
    unittest.main()
