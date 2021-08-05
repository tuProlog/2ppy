import unittest
from root_package.sub_package import Example

class TestExample(unittest.TestCase):

    def test_hello(self):
        e = Example()
        self.assertEqual(e.hello("world"), 'Hello world')
