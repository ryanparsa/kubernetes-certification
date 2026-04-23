#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")


class TestNamespacesAndApiResources(unittest.TestCase):

    def test_resources_file_exists(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        self.assertTrue(os.path.exists(filepath), "File cka/33/course/resources.txt does not exist")

    def test_resources_file_content(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        with open(filepath, "r") as f:
            content = f.read()
        self.assertIn("pods", content)
        self.assertIn("secrets", content)
        self.assertIn("configmaps", content)
        # Check if it contains some namespaced resources that are typically namespaced
        self.assertIn("services", content)
        self.assertIn("deployments.apps", content)

    def test_crowded_namespace_file_exists(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        self.assertTrue(os.path.exists(filepath), "File cka/33/course/crowded-namespace.txt does not exist")

    def test_crowded_namespace_file_content(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        with open(filepath, "r") as f:
            content = f.read().strip()
        self.assertEqual(content, "project-miami with 300 roles")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
