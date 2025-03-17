import unittest
from unittest import skip

class MyTestCase(unittest.TestCase):
    @skip
    def test100_smoke(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
