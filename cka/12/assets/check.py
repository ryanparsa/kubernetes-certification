#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG):
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestSchedulePodOnControlplaneNodes(unittest.TestCase):
    def test_pod_running(self):
        status = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Running")

    def test_pod_container_count(self):
        count = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(count.split()), 1)

    def test_container_name(self):
        name = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.containers[0].name}")
        self.assertEqual(name, "pod1-container")

    def test_container_image(self):
        image = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_scheduled_on_controlplane(self):
        node_name = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.nodeName}")
        # In kind, the value is usually empty string for key-only labels
        control_plane_nodes = kubectl("get", "nodes", "-l", "node-role.kubernetes.io/control-plane", "-o", "jsonpath={.items[*].metadata.name}").split()
        self.assertIn(node_name, control_plane_nodes)

    def test_node_selector_configured(self):
        selector = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.nodeSelector.node-role\\.kubernetes\\.io/control-plane}")
        self.assertEqual(selector, "")

if __name__ == "__main__":
    unittest.main(verbosity=2)
