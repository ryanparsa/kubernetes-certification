#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestPodReadyIfServiceReachable(unittest.TestCase):

    def test_pod1_is_running(self):
        phase = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod1_has_single_container(self):
        containers = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod1_container_is_ready(self):
        ready = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.status.containerStatuses[0].ready}")
        self.assertEqual(ready, "true")

    def test_pod1_container_has_correct_image(self):
        image = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")

    def test_pod1_container_has_liveness_probe(self):
        probe = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.spec.containers[0].livenessProbe}")
        self.assertTrue(probe != "")

    def test_pod1_container_has_readiness_probe(self):
        probe = kubectl("get", "pod", "ready-if-service-ready", "-n", "default", "-o", "jsonpath={.spec.containers[0].readinessProbe}")
        self.assertTrue(probe != "")

    def test_pod2_is_running(self):
        phase = kubectl("get", "pod", "am-i-ready", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod2_has_correct_label(self):
        label = kubectl("get", "pod", "am-i-ready", "-n", "default", "-o", "jsonpath={.metadata.labels.id}")
        self.assertEqual(label, "cross-server-ready")

    def test_pod2_has_single_container(self):
        containers = kubectl("get", "pod", "am-i-ready", "-n", "default", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod2_container_is_ready(self):
        ready = kubectl("get", "pod", "am-i-ready", "-n", "default", "-o", "jsonpath={.status.containerStatuses[0].ready}")
        self.assertEqual(ready, "true")

    def test_pod2_container_has_correct_image(self):
        image = kubectl("get", "pod", "am-i-ready", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx:1-alpine")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
