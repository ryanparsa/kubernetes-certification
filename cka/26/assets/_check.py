#!/usr/bin/env python3
import os
import subprocess
import unittest

LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def node_has_role(node_name, role):
    labels = kubectl("get", "node", node_name, "--show-labels")
    return f"node-role.kubernetes.io/{role}" in labels


class TestManualScheduling(unittest.TestCase):

    def test_pod1_is_running(self):
        phase = kubectl("get", "pod", "manual-schedule", "-n", "default",
                        "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod1_is_on_controlplane(self):
        node = kubectl("get", "pod", "manual-schedule", "-n", "default",
                       "-o", "jsonpath={.spec.nodeName}")
        self.assertTrue(node, "manual-schedule has no nodeName set")
        self.assertTrue(node_has_role(node, "control-plane"),
                        f"manual-schedule is on '{node}', expected a control-plane node")

    def test_pod1_has_single_container(self):
        containers = kubectl("get", "pod", "manual-schedule", "-n", "default",
                             "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod1_has_correct_image(self):
        image = kubectl("get", "pod", "manual-schedule", "-n", "default",
                        "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_pod2_is_running(self):
        phase = kubectl("get", "pod", "manual-schedule2", "-n", "default",
                        "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod2_is_on_worker(self):
        node = kubectl("get", "pod", "manual-schedule2", "-n", "default",
                       "-o", "jsonpath={.spec.nodeName}")
        self.assertTrue(node, "manual-schedule2 has no nodeName set")
        self.assertFalse(node_has_role(node, "control-plane"),
                         f"manual-schedule2 landed on control-plane '{node}', expected a worker")

    def test_pod2_has_single_container(self):
        containers = kubectl("get", "pod", "manual-schedule2", "-n", "default",
                             "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod2_has_correct_image(self):
        image = kubectl("get", "pod", "manual-schedule2", "-n", "default",
                        "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_scheduler_is_running(self):
        phase = kubectl("get", "pod", "-n", "kube-system",
                        "-l", "component=kube-scheduler",
                        "-o", "jsonpath={.items[0].status.phase}")
        self.assertEqual(phase, "Running")

    def test_scheduler_was_restarted(self):
        # The scheduler pod was removed and re-created; the pod should exist and be Running
        pod_name = kubectl("get", "pod", "-n", "kube-system",
                           "-l", "component=kube-scheduler",
                           "-o", "jsonpath={.items[0].metadata.name}")
        self.assertTrue(pod_name, "No kube-scheduler pod found in kube-system")
        phase = kubectl("get", "pod", pod_name, "-n", "kube-system",
                        "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running",
                         "kube-scheduler pod is not Running after restart")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
