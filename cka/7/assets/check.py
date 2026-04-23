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


class TestNodePodResourceUsage(unittest.TestCase):

    def test_node_sh_exists(self):
        path = os.path.join(os.path.dirname(__file__), "..", "course", "node.sh")
        self.assertTrue(os.path.isfile(path), "course/node.sh does not exist")

    def test_node_sh_contains_top_node(self):
        path = os.path.join(os.path.dirname(__file__), "..", "course", "node.sh")
        with open(path) as f:
            content = f.read()
        self.assertIn("kubectl top node", content)

    def test_pod_sh_exists(self):
        path = os.path.join(os.path.dirname(__file__), "..", "course", "pod.sh")
        self.assertTrue(os.path.isfile(path), "course/pod.sh does not exist")

    def test_pod_sh_contains_top_pod_containers(self):
        path = os.path.join(os.path.dirname(__file__), "..", "course", "pod.sh")
        with open(path) as f:
            content = f.read()
        self.assertIn("kubectl top pod", content)
        self.assertIn("--containers=true", content)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
