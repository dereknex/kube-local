import unittest
from informer import Informer, Status

class MockObserver:

    reviced_progress = 0
    reviced_status = None

    def update_progress(self, info):
        self.reviced_progress = info.progress
        self.reviced_status = info.status

class TestInformer(unittest.TestCase):
    def test_status(self):
        i = Informer()
        i.progress = 500
        self.assertEqual(i.progress, 100)
        self.assertEqual(i.status, Status.DONE)
        i.progress = -5
        self.assertEqual(i.progress, 0)
        self.assertNotEqual(i.status, Status.DONE)
        i.progress = 32
        self.assertEqual(i.progress, 32)
        self.assertEqual(i.status, Status.IN_PROGRESS)

    def test_observer(self):
        i = Informer()
        m = MockObserver()
        i.watch(m)
        i.progress = 500
        self.assertEqual(m.reviced_progress, 100)
        self.assertEqual(m.reviced_status, Status.DONE)
        