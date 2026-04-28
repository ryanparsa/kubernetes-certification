#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestManualScheduling(unittest.TestCase):
    def test_manual_schedule_pod_running_on_worker(self):
        node = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.spec.nodeName}")
        phase = kubectl("get", "pod", "manual-schedule", "-o", "jsonpath={.status.phase}")
        self.assertEqual(node, "cka-lab-108-worker")
        self.assertEqual(phase, "Running")

    def test_manual_schedule2_pod_running_on_worker(self):
        node = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.spec.nodeName}")
        phase = kubectl("get", "pod", "manual-schedule2", "-o", "jsonpath={.status.phase}")
        # In a 2-node kind cluster (control-plane and worker),
        # it should land on worker unless control-plane is untainted.
        # Kind clusters usually have control-plane tainted.
        self.assertEqual(node, "cka-lab-108-worker")
        self.assertEqual(phase, "Running")

    def test_scheduler_running(self):
        # Check if kube-scheduler pod is running in kube-system
        status = kubectl("get", "pods", "-n", "kube-system", "-l", "component=kube-scheduler", "-o", "jsonpath={.items[0].status.phase}")
        self.assertEqual(status, "Running")

if __name__ == "__main__":
    unittest.main()
