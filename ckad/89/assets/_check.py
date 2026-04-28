#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestNamespaceList(unittest.TestCase):
    def test_namespace_file_exists(self):
        self.assertTrue(os.path.exists("/opt/course/1/namespaces"), "File /opt/course/1/namespaces does not exist")

    def test_namespace_file_content(self):
        # Read the file
        with open("/opt/course/1/namespaces", "r") as f:
            content_lines = set(line.strip() for line in f if line.strip())

        # Get actual namespaces
        # We used -o name which returns "namespace/default" etc.
        expected_namespaces = set(kubectl("get", "namespaces", "-o", "name").split())

        self.assertEqual(content_lines, expected_namespaces, "File content does not match the expected list of namespaces")

if __name__ == "__main__":
    unittest.main(verbosity=2)
