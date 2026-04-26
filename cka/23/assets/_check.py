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


class TestFixKubelet(unittest.TestCase):

    def test_node_is_ready(self):
        status = kubectl(
            "get", "node", "-l", "node-role.kubernetes.io/control-plane",
            "-o", r"jsonpath={.items[0].status.conditions[?(@.type=='Ready')].status}",
        )
        self.assertEqual(status, "True")

    def test_pod_success_exists(self):
        phase = kubectl("get", "pod", "success", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod_success_image(self):
        image = kubectl("get", "pod", "success", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
