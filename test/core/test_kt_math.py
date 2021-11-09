from decimal import Decimal
import unittest

from tuprolog.core import big_integer, python_integer, big_decimal, python_decimal, BIG_INTEGER_ZERO, BIG_INTEGER_TEN, \
    BIG_INTEGER_ONE, BIG_INTEGER_NEGATIVE_ONE, BIG_INTEGER_TWO, BIG_DECIMAL_PI, BIG_DECIMAL_E, BIG_DECIMAL_ONE_TENTH, \
    BIG_DECIMAL_ONE_HALF, BIG_DECIMAL_ONE, BIG_DECIMAL_ZERO, BigInteger


class TestKtMath(unittest.TestCase):

    def assertSameStringRepresentation(self, expected, actual):
        self.assertEqual(str(expected), str(actual))


class TestBigInteger(TestKtMath):

    def setUp(self):
        self.large_int = 1 << 64

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
        self.assertEqual(0, python_integer(big_integer("0")))
        self.assertEqual(0, python_integer(big_integer(0)))
        self.assertEqual(1, python_integer(big_integer("1")))
        self.assertEqual(1, python_integer(big_integer(1)))
        self.assertEqual(self.large_int, python_integer(big_integer(self.large_int)))
        self.assertEqual(-1, python_integer(big_integer("-1")))
        self.assertEqual(-1, python_integer(big_integer(-1)))
        self.assertEqual(-self.large_int, python_integer(big_integer(-self.large_int)))
        self.assertEqual(0x16, python_integer(big_integer("16", 16)))
        self.assertEqual(-0x16, python_integer(big_integer("-16", 16)))

    def test_constants(self):
        self.assertEqual(big_integer(0), BIG_INTEGER_ZERO)
        self.assertEqual(big_integer(10), BIG_INTEGER_TEN)
        self.assertEqual(big_integer(1), BIG_INTEGER_ONE)
        self.assertEqual(big_integer(-1), BIG_INTEGER_NEGATIVE_ONE)
        self.assertEqual(big_integer(2), BIG_INTEGER_TWO)

    def test_integers(self):
        for i in range(-512, 513):
            self.assertEqual(BigInteger.of(i), big_integer(i))
        for t in [8, 16, 32, 64, 128]:
            for i in [1 << t - 1, 1 << t]:
                self.assertEqual(BigInteger.of(str(i)), big_integer(i))
                self.assertEqual(BigInteger.of(str(-i)), big_integer(-i))


class TestBigDecimal(TestKtMath):

    def setUp(self):
        self.e = '2.71828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852' + \
                 '5166427427466391932003059921817413596629043572900334295260595630738132328627943490763233829880' + \
                 '753195251019011573834187930702154089149934884167509244761460668082264'

        self.pi = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253' + \
                  '421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446' + \
                  '22948954930381964428810975665933446128475648233786783165271201909145648'

        self.one_tenth = "0.01000000000000000020816681711721685132943093776702880859375"

    def test_python_to_java_zero(self):
        self.assertSameStringRepresentation(0, big_decimal("0"))
        self.assertSameStringRepresentation(0, big_decimal("0.0"))
        self.assertSameStringRepresentation(0, big_decimal("0.00"))
        self.assertSameStringRepresentation(0, big_decimal(0))
        self.assertSameStringRepresentation(0, big_decimal(0.0))
        self.assertSameStringRepresentation(0, big_decimal(0.00))
        self.assertSameStringRepresentation(0, big_decimal(Decimal(0)))
        self.assertSameStringRepresentation(0, big_decimal(Decimal(0.0)))
        self.assertSameStringRepresentation(0, big_decimal(Decimal(0.00)))

    def test_python_to_java_one(self):
        self.assertSameStringRepresentation(1, big_decimal("1"))
        self.assertSameStringRepresentation(1, big_decimal("1.0"))
        self.assertSameStringRepresentation(1, big_decimal("1.00"))
        self.assertSameStringRepresentation(1, big_decimal(1))
        self.assertSameStringRepresentation(1, big_decimal(1.0))
        self.assertSameStringRepresentation(1, big_decimal(1.00))
        self.assertSameStringRepresentation(1, big_decimal(Decimal(1)))
        self.assertSameStringRepresentation(1, big_decimal(Decimal(1.0)))
        self.assertSameStringRepresentation(1, big_decimal(Decimal(1.00)))

    def test_python_to_java_minus_one(self):
        self.assertSameStringRepresentation(-1, big_decimal("-1"))
        self.assertSameStringRepresentation(-1, big_decimal("-1.0"))
        self.assertSameStringRepresentation(-1, big_decimal("-1.00"))
        self.assertSameStringRepresentation(-1, big_decimal(-1))
        self.assertSameStringRepresentation(-1, big_decimal(-1.0))
        self.assertSameStringRepresentation(-1, big_decimal(-1.00))
        self.assertSameStringRepresentation(-1, big_decimal(Decimal(-1)))
        self.assertSameStringRepresentation(-1, big_decimal(Decimal(-1.0)))
        self.assertSameStringRepresentation(-1, big_decimal(Decimal(-1.00)))

    def test_python_to_java_one_half(self):
        self.assertSameStringRepresentation(0.5, big_decimal("0.5"))
        self.assertSameStringRepresentation(0.5, big_decimal("0.50"))
        self.assertSameStringRepresentation(0.5, big_decimal("0.500"))
        self.assertSameStringRepresentation(0.5, big_decimal(0.5))
        self.assertSameStringRepresentation(0.5, big_decimal(0.50))
        self.assertSameStringRepresentation(0.5, big_decimal(0.500))
        self.assertSameStringRepresentation(0.5, big_decimal(Decimal(0.5)))
        self.assertSameStringRepresentation(0.5, big_decimal(Decimal(0.50)))
        self.assertSameStringRepresentation(0.5, big_decimal(Decimal(0.500)))

    def test_python_to_java_one_cent(self):
        self.assertSameStringRepresentation(0.01, big_decimal("0.01"))
        self.assertSameStringRepresentation(0.01, big_decimal("0.010"))
        self.assertSameStringRepresentation(0.01, big_decimal("0.0100"))
        self.assertSameStringRepresentation(0.01, big_decimal(0.01))
        self.assertSameStringRepresentation(0.01, big_decimal(0.010))
        self.assertSameStringRepresentation(0.01, big_decimal(0.0100))
        self.assertSameStringRepresentation(self.one_tenth, big_decimal(Decimal(0.01)))
        self.assertSameStringRepresentation(self.one_tenth, big_decimal(Decimal(0.010)))
        self.assertSameStringRepresentation(self.one_tenth, big_decimal(Decimal(0.0100)))

    def test_java_to_python_zero(self):
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal("0")))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal("0.0")))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal("0.00")))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(0)))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(0.0)))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(0.00)))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(Decimal(0))))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(Decimal(0.0))))
        self.assertSameStringRepresentation(Decimal(0), python_decimal(big_decimal(Decimal(0.00))))

    def test_java_to_python_one(self):
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal("1")))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal("1.0")))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal("1.00")))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(1)))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(1.0)))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(1.00)))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(Decimal(1))))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(Decimal(1.0))))
        self.assertSameStringRepresentation(Decimal(1), python_decimal(big_decimal(Decimal(1.00))))

    def test_java_to_python_minus_one(self):
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal("-1")))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal("-1.0")))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal("-1.00")))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(-1)))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(-1.0)))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(-1.00)))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(Decimal(-1))))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(Decimal(-1.0))))
        self.assertSameStringRepresentation(Decimal(-1), python_decimal(big_decimal(Decimal(-1.00))))

    def test_java_to_python_one_half(self):
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal("0.5")))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal("0.50")))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal("0.500")))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(0.5)))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(0.50)))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(0.500)))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(Decimal(0.5))))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(Decimal(0.50))))
        self.assertSameStringRepresentation(Decimal(0.5), python_decimal(big_decimal(Decimal(0.500))))

    def test_java_to_python_one_cent(self):
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal("0.01")))
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal("0.010")))
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal("0.0100")))
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal(0.01)))
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal(0.010)))
        self.assertSameStringRepresentation(Decimal("0.01"), python_decimal(big_decimal(0.0100)))
        self.assertSameStringRepresentation(Decimal(self.one_tenth), python_decimal(big_decimal(Decimal(0.01))))
        self.assertSameStringRepresentation(Decimal(self.one_tenth), python_decimal(big_decimal(Decimal(0.010))))
        self.assertSameStringRepresentation(Decimal(self.one_tenth), python_decimal(big_decimal(Decimal(0.0100))))

    def test_constants(self):
        self.assertEqual(big_decimal(0), BIG_DECIMAL_ZERO)
        self.assertEqual(big_decimal(1), BIG_DECIMAL_ONE)
        self.assertEqual(big_decimal(0.5), BIG_DECIMAL_ONE_HALF)
        self.assertEqual(big_decimal("0.1"), BIG_DECIMAL_ONE_TENTH)
        self.assertEqual(big_decimal(self.e), BIG_DECIMAL_E)
        self.assertEqual(big_decimal(self.pi), BIG_DECIMAL_PI)


if __name__ == '__main__':
    unittest.main()
