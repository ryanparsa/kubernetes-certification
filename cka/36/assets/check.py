#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")
IPTABLES_FILE = os.path.join(COURSE_DIR, "iptables.txt")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestKubeProxyIptables(unittest.TestCase):

    def test_pod_exists_and_running(self):
        phase = kubectl("get", "pod", "p2-pod", "-n", "project-hamster", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running", "Pod p2-pod is not Running")

    def test_pod_image(self):
        image = kubectl("get", "pod", "p2-pod", "-n", "project-hamster", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine", "Pod p2-pod is not using nginx:1-alpine image")

    def test_service_deleted(self):
        # Service should not exist
        result = subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "get", "svc", "p2-service", "-n", "project-hamster"],
            capture_output=True, text=True
        )
        self.assertIn("Error from server (NotFound)", result.stderr, "Service p2-service still exists")

    def test_iptables_file_contains_rules(self):
        self.assertTrue(os.path.exists(IPTABLES_FILE), f"{IPTABLES_FILE} does not exist")
        with open(IPTABLES_FILE, "r") as f:
            content = f.read()
            self.assertIn("p2-service", content, "iptables.txt does not contain p2-service rules")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
