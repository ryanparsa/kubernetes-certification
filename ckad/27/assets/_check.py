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


class TestHealthProbes(unittest.TestCase):

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_liveness_probe_http_get_path(self):
        path = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o",
                       "jsonpath={.spec.containers[0].livenessProbe.httpGet.path}")
        self.assertEqual(path, "/healthz")

    def test_liveness_probe_http_get_port(self):
        port = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o",
                       "jsonpath={.spec.containers[0].livenessProbe.httpGet.port}")
        self.assertEqual(port, "80")

    def test_liveness_probe_period_seconds(self):
        period = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o",
                         "jsonpath={.spec.containers[0].livenessProbe.periodSeconds}")
        self.assertEqual(period, "15")

    def test_readiness_probe_tcp_socket_port(self):
        port = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o",
                       "jsonpath={.spec.containers[0].readinessProbe.tcpSocket.port}")
        self.assertEqual(port, "80")

    def test_readiness_probe_period_seconds(self):
        period = kubectl("get", "pod", "health-pod", "-n", "workloads", "-o",
                         "jsonpath={.spec.containers[0].readinessProbe.periodSeconds}")
        self.assertEqual(period, "10")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
