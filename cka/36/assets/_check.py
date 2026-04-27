#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CLUSTER_NAME = f"{EXAM}-lab-{LAB_ID}"

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

def docker_exec(container, *args):
    result = subprocess.run(
        ["docker", "exec", container, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestKubeProxyIptables(unittest.TestCase):

    def test_pod_exists(self):
        phase = kubectl("get", "pod", "p2-pod", "-n", "project-hamster", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod_image(self):
        image = kubectl("get", "pod", "p2-pod", "-n", "project-hamster", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_iptables_file_exists_and_contains_rules(self):
        file_path = os.path.join(SCRIPT_DIR, "..", "lab", "iptables.txt")
        self.assertTrue(os.path.exists(file_path), "iptables.txt file does not exist")
        with open(file_path, 'r') as f:
            content = f.read()
        self.assertIn("p2-service", content, "iptables.txt does not contain p2-service rules")

    def test_service_deleted(self):
        result = subprocess.run(
            ["kubectl", "--kubeconfig", KUBECONFIG, "get", "svc", "p2-service", "-n", "project-hamster"],
            capture_output=True, text=True,
        )
        self.assertIn("NotFound", result.stderr)

    def test_no_iptables_rules_left(self):
        rules = docker_exec(f"{CLUSTER_NAME}-control-plane", "iptables-save")
        self.assertNotIn("p2-service", rules, "iptables rules for p2-service still exist on control-plane")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
