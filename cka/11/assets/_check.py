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


class TestDaemonSetOnAllNodes(unittest.TestCase):

    def test_daemonset_exists(self):
        name = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "ds-important")

    def test_daemonset_label_id(self):
        label = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels.id}")
        self.assertEqual(label, "ds-important")

    def test_daemonset_label_uuid(self):
        label = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels.uuid}")
        self.assertEqual(label, "18426a0b-5f59-4e10-923f-c0e078e82462")

    def test_pod_label_id(self):
        label = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.metadata.labels.id}")
        self.assertEqual(label, "ds-important")

    def test_pod_label_uuid(self):
        label = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.metadata.labels.uuid}")
        self.assertEqual(label, "18426a0b-5f59-4e10-923f-c0e078e82462")

    def test_container_cpu_request(self):
        cpu = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].resources.requests.cpu}")
        self.assertEqual(cpu, "10m")

    def test_container_memory_request(self):
        mem = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.containers[0].resources.requests.memory}")
        self.assertEqual(mem, "10Mi")

    def test_controlplane_toleration(self):
        tolerations = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.spec.template.spec.tolerations}")
        self.assertIn("control-plane", tolerations)

    def test_runs_on_all_nodes(self):
        desired = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.status.desiredNumberScheduled}")
        ready = kubectl("get", "ds", "ds-important", "-n", "project-tiger", "-o", "jsonpath={.status.numberReady}")
        self.assertTrue(desired and int(desired) > 0, "DaemonSet desiredNumberScheduled is 0")
        self.assertEqual(desired, ready)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
