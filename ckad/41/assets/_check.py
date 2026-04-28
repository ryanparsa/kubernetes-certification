#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
LOCAL_KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestProbesPod(unittest.TestCase):

    def test_namespace_exists(self):
        ns = kubectl("get", "namespace", "observability", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "observability")

    def test_pod_exists_and_image(self):
        image = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "nginx")

    def test_liveness_probe(self):
        path = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].livenessProbe.httpGet.path}")
        port = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].livenessProbe.httpGet.port}")
        delay = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].livenessProbe.initialDelaySeconds}")
        period = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].livenessProbe.periodSeconds}")

        self.assertEqual(path, "/healthz")
        self.assertEqual(str(port), "80")
        self.assertEqual(str(delay), "10")
        self.assertEqual(str(period), "5")

    def test_readiness_probe(self):
        path = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].readinessProbe.httpGet.path}")
        port = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].readinessProbe.httpGet.port}")
        delay = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].readinessProbe.initialDelaySeconds}")
        period = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].readinessProbe.periodSeconds}")

        self.assertEqual(path, "/")
        self.assertEqual(str(port), "80")
        self.assertEqual(str(delay), "5")
        self.assertEqual(str(period), "3")

    def test_resources(self):
        cpu_req = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].resources.requests.cpu}")
        mem_req = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].resources.requests.memory}")
        cpu_lim = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].resources.limits.cpu}")
        mem_lim = kubectl("get", "pod", "probes-pod", "-n", "observability", "-o", "jsonpath={.spec.containers[0].resources.limits.memory}")

        self.assertEqual(cpu_req, "100m")
        self.assertEqual(mem_req, "128Mi")
        self.assertEqual(cpu_lim, "200m")
        self.assertEqual(mem_lim, "256Mi")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    # Use standard runner to see errors during development/review
    unittest.main(verbosity=2)
