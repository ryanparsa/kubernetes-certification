#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestScaleStatefulSet(unittest.TestCase):

    def test_replicas_is_one(self):
        replicas = kubectl("get", "sts", "o3db", "-n", "project-h800",
                           "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "1")

    def test_ready_replicas_is_one(self):
        ready = kubectl("get", "sts", "o3db", "-n", "project-h800",
                        "-o", "jsonpath={.status.readyReplicas}")
        self.assertEqual(ready, "1")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
