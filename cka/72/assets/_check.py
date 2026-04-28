#!/usr/bin/env python3

import os
import unittest

PODS_FILE = "/opt/course/7/pods.txt"
NODES_FILE = "/opt/course/7/nodes.txt"


def read_lines(path):
    with open(path) as f:
        return [line.rstrip() for line in f]


class TestKubectlTopOutput(unittest.TestCase):

    def test_pods_file_exists(self):
        self.assertTrue(os.path.isfile(PODS_FILE), f"{PODS_FILE} does not exist")

    def test_pods_file_not_empty(self):
        lines = read_lines(PODS_FILE)
        self.assertGreater(len(lines), 1, f"{PODS_FILE} is empty or has only a header")

    def test_pods_file_has_namespace_column(self):
        """--all-namespaces produces a NAMESPACE column in the header."""
        lines = read_lines(PODS_FILE)
        header = lines[0].upper()
        self.assertIn("NAMESPACE", header, "pods.txt header missing NAMESPACE column (use --all-namespaces)")

    def test_pods_file_has_container_column(self):
        """--containers produces a NAME column (container name) alongside the POD column."""
        lines = read_lines(PODS_FILE)
        header = lines[0].upper()
        # With --containers the header shows both POD and NAME (container)
        self.assertIn("POD", header, "pods.txt header missing POD column")
        self.assertIn("NAME", header, "pods.txt header missing NAME (container) column (use --containers)")

    def test_pods_file_sorted_by_pod_name(self):
        """Pod names (column 2) should be in non-decreasing alphabetical order."""
        lines = read_lines(PODS_FILE)
        # Skip header; extract pod name (2nd whitespace-separated field)
        pod_names = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                pod_names.append(parts[1])
        self.assertGreater(len(pod_names), 0, "No pod data rows found in pods.txt")
        self.assertEqual(pod_names, sorted(pod_names),
                         "Pod names in pods.txt are not sorted alphabetically (use --sort-by=name)")

    def test_nodes_file_exists(self):
        self.assertTrue(os.path.isfile(NODES_FILE), f"{NODES_FILE} does not exist")

    def test_nodes_file_not_empty(self):
        lines = read_lines(NODES_FILE)
        self.assertGreater(len(lines), 1, f"{NODES_FILE} is empty or has only a header")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
