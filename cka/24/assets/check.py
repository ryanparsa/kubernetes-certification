#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")


class TestEtcdOperations(unittest.TestCase):

    def test_etcd_version_file(self):
        filepath = os.path.join(COURSE_DIR, "etcd-version")
        self.assertTrue(os.path.exists(filepath), f"File {filepath} does not exist")
        with open(filepath, "r") as f:
            content = f.read()
            self.assertIn("etcd Version:", content)

    def test_etcd_snapshot_file(self):
        filepath = os.path.join(COURSE_DIR, "etcd-snapshot.db")
        self.assertTrue(os.path.exists(filepath), f"File {filepath} does not exist")
        # Check if file is not empty
        self.assertGreater(os.path.getsize(filepath), 0, f"File {filepath} is empty")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
