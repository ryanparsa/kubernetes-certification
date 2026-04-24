#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CLUSTER_NAME = f"{EXAM}-lab-{LAB_ID}"

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestKillScheduler(unittest.TestCase):
    def test_pod1_running(self):
        phase = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod1_node(self):
        node = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.spec.nodeName}")
        self.assertEqual(node, f"{CLUSTER_NAME}-control-plane")

    def test_pod1_container(self):
        image = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

        count = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(count.split()), 1)

    def test_pod2_running(self):
        phase = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod2_node(self):
        node = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.spec.nodeName}")
        self.assertEqual(node, f"{CLUSTER_NAME}-worker")

    def test_pod2_container(self):
        image = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

        count = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(count.split()), 1)

    def test_scheduler_running(self):
        # Find pod name
        pod_name = kubectl("get", "pod", "-n", "kube-system", "-l", "component=kube-scheduler", "-o", "jsonpath={.items[0].metadata.name}")
        self.assertTrue(pod_name.startswith(f"kube-scheduler-{CLUSTER_NAME}-control-plane"))

        phase = kubectl("get", "pod", "-n", "kube-system", pod_name, "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

if __name__ == "__main__":
    unittest.main(verbosity=2)
