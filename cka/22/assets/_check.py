#!/usr/bin/env python3
import os
import unittest

LAB_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lab"))


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""


class TestKubectlSorting(unittest.TestCase):

    def test_find_pods_file_exists(self):
        path = os.path.join(LAB_DIR, "find_pods.sh")
        self.assertTrue(os.path.isfile(path), f"File not found: {path}")

    def test_find_pods_contains_sort_by_timestamp(self):
        path = os.path.join(LAB_DIR, "find_pods.sh")
        content = read_file(path)
        self.assertIn("--sort-by=.metadata.creationTimestamp", content)

    def test_find_pods_uid_file_exists(self):
        path = os.path.join(LAB_DIR, "find_pods_uid.sh")
        self.assertTrue(os.path.isfile(path), f"File not found: {path}")

    def test_find_pods_uid_contains_sort_by_uid(self):
        path = os.path.join(LAB_DIR, "find_pods_uid.sh")
        content = read_file(path)
        self.assertIn("--sort-by=.metadata.uid", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
