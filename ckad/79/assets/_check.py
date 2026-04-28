#!/usr/bin/env python3

import json
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


class TestPodWithLabelsAndResources(unittest.TestCase):

    def test_namespace_exists(self):
        output = kubectl("get", "namespace", "workloads", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(output, "workloads")

    def test_pod_running_with_labels(self):
        phase = kubectl("get", "pod", "web", "-n", "workloads", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

        app_label = kubectl("get", "pod", "web", "-n", "workloads", "-o", "jsonpath={.metadata.labels.app}")
        self.assertEqual(app_label, "web")

        tier_label = kubectl("get", "pod", "web", "-n", "workloads", "-o", "jsonpath={.metadata.labels.tier}")
        self.assertEqual(tier_label, "frontend")

    def test_resource_constraints(self):
        cpu_req = kubectl(
            "get", "pod", "web", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].resources.requests.cpu}",
        )
        self.assertEqual(cpu_req, "100m")

        cpu_lim = kubectl(
            "get", "pod", "web", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].resources.limits.cpu}",
        )
        self.assertEqual(cpu_lim, "250m")

        mem_req = kubectl(
            "get", "pod", "web", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].resources.requests.memory}",
        )
        self.assertEqual(mem_req, "128Mi")

        mem_lim = kubectl(
            "get", "pod", "web", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].resources.limits.memory}",
        )
        self.assertEqual(mem_lim, "256Mi")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
