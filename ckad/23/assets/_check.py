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


class TestResourceLimitsOnLoggingPod(unittest.TestCase):

    def test_cpu_limit_set(self):
        cpu = kubectl(
            "get", "pod", "logging-pod", "-n", "troubleshooting",
            "-o", "jsonpath={.spec.containers[?(@.name=='log-processor')].resources.limits.cpu}",
        )
        self.assertEqual(cpu, "100m")

    def test_memory_limit_and_pod_running(self):
        mem = kubectl(
            "get", "pod", "logging-pod", "-n", "troubleshooting",
            "-o", "jsonpath={.spec.containers[?(@.name=='log-processor')].resources.limits.memory}",
        )
        phase = kubectl(
            "get", "pod", "logging-pod", "-n", "troubleshooting",
            "-o", "jsonpath={.status.phase}",
        )
        self.assertEqual(mem, "50Mi")
        self.assertEqual(phase, "Running")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
