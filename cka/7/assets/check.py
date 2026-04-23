#!/usr/bin/env python3
import os
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
COURSE_DIR = os.path.join(SCRIPT_DIR, "..", "course")


class TestNodePodResourceUsage(unittest.TestCase):

    def test_node_sh_exists(self):
        path = os.path.join(COURSE_DIR, "node.sh")
        self.assertTrue(os.path.isfile(path), "course/node.sh does not exist")

    def test_node_sh_contains_top_node(self):
        path = os.path.join(COURSE_DIR, "node.sh")
        with open(path) as f:
            content = f.read()
        self.assertIn("kubectl top node", content)

    def test_pod_sh_exists(self):
        path = os.path.join(COURSE_DIR, "pod.sh")
        self.assertTrue(os.path.isfile(path), "course/pod.sh does not exist")

    def test_pod_sh_contains_top_pod_containers(self):
        path = os.path.join(COURSE_DIR, "pod.sh")
        with open(path) as f:
            content = f.read()
        self.assertIn("kubectl top pod", content)
        self.assertIn("--containers", content)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
