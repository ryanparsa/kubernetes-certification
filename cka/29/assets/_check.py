#!/usr/bin/env python3

import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestSchedulePodOnControlplaneNodes(unittest.TestCase):

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_single_container(self):
        names = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={range .spec.containers[*]}{.name} {end}")
        self.assertEqual(len(names.split()), 1)

    def test_container_name(self):
        name = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.containers[0].name}")
        self.assertEqual(name, "pod1-container")

    def test_container_image(self):
        image = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_pod_scheduled_on_controlplane(self):
        node = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.nodeName}")
        labels = kubectl("get", "node", node, "--show-labels") if node else ""
        self.assertIn("node-role.kubernetes.io/control-plane", labels)

    def test_pod_restricted_to_controlplane(self):
        selector = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.nodeSelector}")
        affinity = kubectl("get", "pod", "pod1", "-n", "default", "-o", "jsonpath={.spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution}")
        self.assertTrue(selector or affinity, "Pod has no nodeSelector or nodeAffinity")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
