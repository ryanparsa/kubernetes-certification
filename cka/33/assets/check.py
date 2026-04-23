#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
COURSE_DIR = os.path.join(SCRIPT_DIR, "..", "course")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestNamespacesAndApiResources(unittest.TestCase):

    def test_resources_file_exists(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        self.assertTrue(os.path.exists(filepath), "resources.txt does not exist")

    def test_resources_file_content(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        with open(filepath, "r") as f:
            content = f.read().splitlines()

        expected_resources = kubectl("api-resources", "--namespaced", "-o", "name").splitlines()
        for res in expected_resources:
            self.assertIn(res, content, f"Resource {res} missing from resources.txt")

    def test_crowded_namespace_file_exists(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        self.assertTrue(os.path.exists(filepath), "crowded-namespace.txt does not exist")

    def test_crowded_namespace_file_content(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        with open(filepath, "r") as f:
            content = f.read().strip()

        # We know from up.sh that project-miami should have 300 roles
        self.assertEqual(content, "project-miami with 300 roles")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
