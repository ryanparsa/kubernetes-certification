#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

if os.getenv("GITHUB_ACTIONS"):
    KUBECONFIG = os.path.expanduser("~/.kube/config")
else:
    KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result

class TestPod1(unittest.TestCase):
    def test_pod1_exists_and_running(self):
        result = kubectl("get", "pod", "pod1", "-o", "json")
        self.assertEqual(result.returncode, 0, f"Pod pod1 does not exist: {result.stderr}")
        pod = json.loads(result.stdout)

        container = pod["spec"]["containers"][0]
        self.assertEqual(container["name"], "pod1", "Container name is not pod1")
        self.assertEqual(container["image"], "httpd:2.4.41-alpine", "Container image is incorrect")

        # Check port
        ports = container.get("ports", [])
        self.assertTrue(any(p.get("containerPort") == 80 for p in ports), "Container port 80 not configured")

    def test_svc_exists(self):
        result = kubectl("get", "svc", "pod1-svc", "-o", "json")
        self.assertEqual(result.returncode, 0, f"Service pod1-svc does not exist: {result.stderr}")
        svc = json.loads(result.stdout)

        self.assertEqual(svc["spec"]["type"], "NodePort", "Service type is not NodePort")
        self.assertEqual(svc["spec"]["ports"][0]["port"], 80, "Service port is not 80")

    def test_command_file_exists(self):
        file_path = os.path.join(SCRIPT_DIR, "course", "pod1-svc.sh")
        self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist")

        with open(file_path, 'r') as f:
            content = f.read().strip()
            self.assertIn("kubectl expose pod pod1", content)
            self.assertIn("--name=pod1-svc", content)
            self.assertIn("--type=NodePort", content)

if __name__ == "__main__":
    unittest.main(verbosity=2)
