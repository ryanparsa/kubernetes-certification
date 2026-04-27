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


class TestKustomizeHPA(unittest.TestCase):

    def test_staging_hpa_min_replicas(self):
        value = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                        "-o", "jsonpath={.spec.minReplicas}")
        self.assertEqual(value, "2")

    def test_staging_hpa_max_replicas(self):
        value = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                        "-o", "jsonpath={.spec.maxReplicas}")
        self.assertEqual(value, "4")

    def test_staging_hpa_cpu_utilization(self):
        value = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                        "-o", "jsonpath={.spec.metrics[0].resource.target.averageUtilization}")
        self.assertEqual(value, "50")

    def test_prod_hpa_max_replicas(self):
        value = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-prod",
                        "-o", "jsonpath={.spec.maxReplicas}")
        self.assertEqual(value, "6")

    def test_staging_configmap_deleted(self):
        value = kubectl("get", "configmap", "horizontal-scaling-config",
                        "-n", "api-gateway-staging", "--ignore-not-found",
                        "-o", "jsonpath={.metadata.name}")
        self.assertEqual(value, "")

    def test_prod_configmap_deleted(self):
        value = kubectl("get", "configmap", "horizontal-scaling-config",
                        "-n", "api-gateway-prod", "--ignore-not-found",
                        "-o", "jsonpath={.metadata.name}")
        self.assertEqual(value, "")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
