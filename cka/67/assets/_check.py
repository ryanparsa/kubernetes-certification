#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# Priority: 1. KUBECONFIG env var, 2. Local lab/kubeconfig.yaml
KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG and os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)

    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestTroubleshootApp(unittest.TestCase):
    def test_deployment_exists(self):
        output = kubectl("get", "deployment", "failing-app", "-n", "troubleshoot", "-o", "json")
        self.assertTrue(len(output) > 0, "Deployment failing-app does not exist in troubleshoot namespace")
        deploy = json.loads(output)
        self.assertEqual(deploy["spec"]["replicas"], 3, "Replicas should be 3")

    def test_container_port(self):
        port = kubectl("get", "deployment", "failing-app", "-n", "troubleshoot", "-o", "jsonpath={.spec.template.spec.containers[0].ports[0].containerPort}")
        self.assertEqual(port, "80", "Container port should be 80")

    def test_memory_limit(self):
        memory = kubectl("get", "deployment", "failing-app", "-n", "troubleshoot", "-o", "jsonpath={.spec.template.spec.containers[0].resources.limits.memory}")
        self.assertEqual(memory, "256Mi", "Memory limit should be 256Mi")

    def test_liveness_probe_port(self):
        probe_port = kubectl("get", "deployment", "failing-app", "-n", "troubleshoot", "-o", "jsonpath={.spec.template.spec.containers[0].livenessProbe.httpGet.port}")
        self.assertEqual(probe_port, "80", "Liveness probe port should be 80")

    def test_pods_running(self):
        available_replicas = kubectl("get", "deployment", "failing-app", "-n", "troubleshoot", "-o", "jsonpath={.status.availableReplicas}")
        self.assertEqual(available_replicas, "3", "All 3 pods should be available")

if __name__ == "__main__":
    unittest.main(verbosity=2)
