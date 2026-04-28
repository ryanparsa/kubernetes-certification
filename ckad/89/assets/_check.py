#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestDeploymentRollback(unittest.TestCase):
    def test_deployment_image_rolled_back(self):
        # Check the image of the deployment
        image = kubectl("get", "deployment", "api-new-c32", "-n", "neptune", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2.4.40-alpine", f"Deployment image is {image}, expected httpd:2.4.40-alpine")

    def test_pods_image_rolled_back(self):
        # Check the image of all pods in the deployment
        output = kubectl("get", "pods", "-n", "neptune", "-l", "app=api-new-c32", "-o", "json")
        pods = json.loads(output)
        for pod in pods.get("items", []):
            image = pod["spec"]["containers"][0]["image"]
            self.assertEqual(image, "httpd:2.4.40-alpine", f"Pod {pod['metadata']['name']} image is {image}, expected httpd:2.4.40-alpine")

    def test_rollout_history_exists(self):
        # Check if there is rollout history (at least 2 revisions should have existed at some point)
        # Undoing creates a new revision, so we should see at least revision 3 if we did 1 -> 2 -> undo(1)
        history = kubectl("rollout", "history", "deployment/api-new-c32", "-n", "neptune")
        self.assertIn("REVISION", history)
        lines = history.splitlines()
        self.assertGreater(len(lines), 2, "Deployment should have at least 2 revisions in history")

if __name__ == "__main__":
    unittest.main(verbosity=2)
