import unittest
from input.base import Input, Status

class TestBase(unittest.TestCase):
    def test_status(self):
        i = Input()
        i.progress = 500
        self.assertEqual(i.progress, 100)
        self.assertEqual(i.status, Status.DONE)
        i.progress = -5
        self.assertEqual(i.progress, 0)
        self.assertNotEqual(i.status, Status.DONE)
        i.progress = 32
        self.assertEqual(i.progress, 32)
        self.assertEqual(i.status, Status.IN_PROGRESS)