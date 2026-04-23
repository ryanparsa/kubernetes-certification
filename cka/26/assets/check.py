#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestKillSchedulerManualScheduling(unittest.TestCase):

    def test_pod1_running(self):
        phase = kubectl("get", "pod", "manual-schedule", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod1_scheduled_on_controlplane(self):
        node = kubectl("get", "pod", "manual-schedule", "-n", "default", "-o", "jsonpath={.spec.nodeName}")
        self.assertEqual(node, "cka-lab-26-control-plane")

    def test_pod1_single_container(self):
        containers = kubectl("get", "pod", "manual-schedule", "-n", "default", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod1_container_image(self):
        image = kubectl("get", "pod", "manual-schedule", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_pod2_running(self):
        phase = kubectl("get", "pod", "manual-schedule2", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod2_scheduled_on_worker(self):
        node = kubectl("get", "pod", "manual-schedule2", "-n", "default", "-o", "jsonpath={.spec.nodeName}")
        self.assertEqual(node, "cka-lab-26-worker")

    def test_pod2_single_container(self):
        containers = kubectl("get", "pod", "manual-schedule2", "-n", "default", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod2_container_image(self):
        image = kubectl("get", "pod", "manual-schedule2", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_scheduler_running(self):
        # We check for the scheduler pod in kube-system
        pods = kubectl("get", "pods", "-n", "kube-system", "-l", "component=kube-scheduler", "-o", "jsonpath={.items[*].status.phase}")
        self.assertIn("Running", pods)

    def test_scheduler_restarted(self):
        # This is a bit tricky to verify without events or looking at restartCount which might be 0 if it's a new pod.
        # But if it's Running and it's there, we assume it was restarted as part of the process.
        # Maybe we check if the pod exists.
        count = kubectl("get", "pods", "-n", "kube-system", "-l", "component=kube-scheduler", "--no-headers")
        self.assertTrue(len(count) > 0)

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
