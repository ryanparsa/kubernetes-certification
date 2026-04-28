#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestManualScheduling(unittest.TestCase):
    def setUp(self):
        self.pod_json = kubectl("get", "pod", "pod", "-n", "default", "-o", "json")
        self.pod = json.loads(self.pod_json) if self.pod_json else {}

    def test_pod_exists(self):
        self.assertTrue(self.pod, "Pod 'pod' not found in 'default' namespace")

    def test_container_name(self):
        container_names = [c["name"] for c in self.pod["spec"]["containers"]]
        self.assertIn("pod-container", container_names, "Container 'pod-container' not found")
        self.assertEqual(len(self.pod["spec"]["containers"]), 1, "Pod should have exactly one container")

    def test_container_image(self):
        image = self.pod["spec"]["containers"][0]["image"]
        self.assertEqual(image, "httpd:2.4.41-alpine", "Incorrect container image")

    def test_pod_scheduled_on_controlplane(self):
        node_name = self.pod["spec"].get("nodeName")
        self.assertIsNotNone(node_name, "Pod is not scheduled on any node")

        node_labels_json = kubectl("get", "node", node_name, "-o", "json")
        node = json.loads(node_labels_json)
        labels = node["metadata"].get("labels", {})

        self.assertIn("node-role.kubernetes.io/control-plane", labels, f"Pod is scheduled on {node_name}, which is not a control-plane node")

    def test_no_tolerations(self):
        tolerations = self.pod["spec"].get("tolerations", [])
        # Default K8s tolerations (like notReady/unreachable) are usually added automatically
        # We want to ensure no manual tolerations for the control-plane taint were added
        for t in tolerations:
            self.assertNotEqual(t.get("key"), "node-role.kubernetes.io/control-plane", "Pod should not have tolerations for control-plane")
            self.assertNotEqual(t.get("key"), "node-role.kubernetes.io/master", "Pod should not have tolerations for master")

if __name__ == "__main__":
    unittest.main()
