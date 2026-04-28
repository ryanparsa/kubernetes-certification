#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "../lab/kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if "KUBECONFIG" not in os.environ and os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

class TestBrokenDeployment(unittest.TestCase):
    def test_deployment_replicas(self):
        result = kubectl("get", "deployment", "broken-deployment", "-n", "troubleshooting", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(result.returncode, 0, f"Failed to get deployment: {result.stderr}")
        self.assertEqual(result.stdout, "3")

    def test_pods_running(self):
        result = kubectl("get", "pods", "-n", "troubleshooting", "-l", "app=broken-deployment", "-o", "json")
        self.assertEqual(result.returncode, 0, f"Failed to get pods: {result.stderr}")
        pods = json.loads(result.stdout)["items"]
        self.assertEqual(len(pods), 3, "Expected 3 pods")
        for pod in pods:
            status = pod["status"]["phase"]
            self.assertEqual(status, "Running", f"Pod {pod['metadata']['name']} is not Running: {status}")

    def test_correct_image(self):
        result = kubectl("get", "deployment", "broken-deployment", "-n", "troubleshooting", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(result.returncode, 0, f"Failed to get image: {result.stderr}")
        self.assertEqual(result.stdout, "nginx:1.19")

if __name__ == "__main__":
    unittest.main(verbosity=2)
