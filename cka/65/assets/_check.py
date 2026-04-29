#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_PATH = os.path.join(SCRIPT_DIR, "../lab/kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_PATH):
        cmd.extend(["--kubeconfig", KUBECONFIG_PATH])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestRollingUpdate(unittest.TestCase):
    def test_deployment_exists_and_replicas(self):
        replicas = kubectl("get", "deployment", "app-v1", "-n", "upgrade", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "4")

    def test_image_is_v1_19(self):
        # After rollback it should be 1.19
        image = kubectl("get", "deployment", "app-v1", "-n", "upgrade", "-o", "jsonpath={.spec.template.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1.19")

    def test_strategy(self):
        max_unavailable = kubectl("get", "deployment", "app-v1", "-n", "upgrade", "-o", "jsonpath={.spec.strategy.rollingUpdate.maxUnavailable}")
        max_surge = kubectl("get", "deployment", "app-v1", "-n", "upgrade", "-o", "jsonpath={.spec.strategy.rollingUpdate.maxSurge}")
        self.assertEqual(str(max_unavailable), "1")
        self.assertEqual(str(max_surge), "1")

    def test_rollout_history_file(self):
        self.assertTrue(os.path.exists("/tmp/exam/rollout-history.txt"))
        with open("/tmp/exam/rollout-history.txt", "r") as f:
            content = f.read()
            self.assertIn("deployment.apps/app-v1", content)
            self.assertIn("REVISION", content)

    def test_all_pods_running(self):
        available_replicas = kubectl("get", "deployment", "app-v1", "-n", "upgrade", "-o", "jsonpath={.status.availableReplicas}")
        self.assertEqual(available_replicas, "4")

if __name__ == "__main__":
    unittest.main(verbosity=2)
