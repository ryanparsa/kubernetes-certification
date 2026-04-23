#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course")


class TestNamespacesAndApiResources(unittest.TestCase):

    def test_resources_txt_exists(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        self.assertTrue(os.path.exists(filepath), "resources.txt does not exist")

    def test_resources_txt_contains_namespaced_resources(self):
        filepath = os.path.join(COURSE_DIR, "resources.txt")
        with open(filepath, "r") as f:
            content = f.read()
        for resource in ["pods", "configmaps", "secrets", "services"]:
            self.assertIn(resource, content, f"resources.txt missing expected resource: {resource}")

    def test_crowded_namespace_txt_exists(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        self.assertTrue(os.path.exists(filepath), "crowded-namespace.txt does not exist")

    def test_crowded_namespace_txt_content(self):
        filepath = os.path.join(COURSE_DIR, "crowded-namespace.txt")
        with open(filepath, "r") as f:
            content = f.read().strip()
        self.assertIn("project-miami", content, "crowded-namespace.txt should identify project-miami")
        self.assertIn("300", content, "crowded-namespace.txt should contain role count 300")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
