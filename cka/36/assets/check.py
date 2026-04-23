#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestKubeProxyIptables(unittest.TestCase):

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "p2-pod", "-n", "project-hamster", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_iptables_file_exists_and_contains_rules(self):
        filepath = os.path.join(COURSE_DIR, "iptables.txt")
        self.assertTrue(os.path.exists(filepath), f"File {filepath} does not exist")
        with open(filepath, "r") as f:
            content = f.read()
        self.assertIn("p2-service", content, "iptables.txt does not contain 'p2-service'")

    def test_service_is_deleted(self):
        result = subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "get", "svc", "p2-service", "-n", "project-hamster"],
            capture_output=True, text=True,
        )
        self.assertIn("Error from server (NotFound)", result.stderr)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
