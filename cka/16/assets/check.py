#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestNamespacesAndApiResources(unittest.TestCase):
    def test_resources_file(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, 'r') as f:
            content = f.read()

        # Check for some common namespaced resources
        self.assertIn("pods", content)
        self.assertIn("secrets", content)
        self.assertIn("configmaps", content)
        self.assertIn("services", content)

        # Check for non-namespaced resource (should NOT be in there)
        self.assertNotIn("nodes", content.splitlines())
        self.assertNotIn("namespaces", content.splitlines())

    def test_crowded_namespace_file(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        self.assertTrue(os.path.exists(filepath), f"{filepath} does not exist")

        with open(filepath, 'r') as f:
            content = f.read().strip()

        self.assertEqual(content, "project-miami with 300 roles")

if __name__ == "__main__":
    unittest.main(verbosity=2)
