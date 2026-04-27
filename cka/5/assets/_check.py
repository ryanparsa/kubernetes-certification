#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
LAB_DIR = os.path.join(os.path.dirname(__file__), "..", "lab")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestKustomizeHPA(unittest.TestCase):

    def test_configmap_removed_from_base(self):
        """Kustomize ConfigMap removed from base"""
        base_yaml = os.path.join(LAB_DIR, "api-gateway", "base", "api-gateway.yaml")
        with open(base_yaml) as f:
            content = f.read()
        self.assertNotIn("kind: ConfigMap", content,
                         "ConfigMap should be removed from base/api-gateway.yaml")

    def test_hpa_added_in_base_with_config(self):
        """Kustomize HPA added in base with required configuration"""
        min_replicas = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                               "-o", "jsonpath={.spec.minReplicas}")
        max_replicas = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                               "-o", "jsonpath={.spec.maxReplicas}")
        cpu = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                      "-o", "jsonpath={.spec.metrics[0].resource.target.averageUtilization}")
        self.assertEqual(min_replicas, "2", "HPA minReplicas should be 2")
        self.assertEqual(max_replicas, "4", "HPA maxReplicas should be 4")
        self.assertEqual(cpu, "50", "HPA CPU averageUtilization should be 50")

    def test_prod_hpa_replicas_overridden(self):
        """Kustomize HPA replicas overwritten in prod"""
        value = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-prod",
                        "-o", "jsonpath={.spec.maxReplicas}")
        self.assertEqual(value, "6", "prod HPA maxReplicas should be overridden to 6")

    def test_kustomize_changes_deployed(self):
        """Kustomize changes deployed to cluster"""
        staging_hpa = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-staging",
                               "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        prod_hpa = kubectl("get", "hpa", "api-gateway", "-n", "api-gateway-prod",
                           "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(staging_hpa, "api-gateway", "HPA should be deployed in api-gateway-staging")
        self.assertEqual(prod_hpa, "api-gateway", "HPA should be deployed in api-gateway-prod")

    def test_configmaps_deleted(self):
        """ConfigMaps removed manually from staging and prod namespaces"""
        staging = kubectl("get", "configmap", "horizontal-scaling-config",
                          "-n", "api-gateway-staging", "--ignore-not-found",
                          "-o", "jsonpath={.metadata.name}")
        prod = kubectl("get", "configmap", "horizontal-scaling-config",
                       "-n", "api-gateway-prod", "--ignore-not-found",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(staging, "", "ConfigMap should not exist in api-gateway-staging")
        self.assertEqual(prod, "", "ConfigMap should not exist in api-gateway-prod")

    def test_kustomize_build_valid(self):
        """Kustomize Build base, staging and prod without error after updates"""
        api_gw = os.path.join(LAB_DIR, "api-gateway")
        for overlay in ["base", "staging", "prod"]:
            path = os.path.join(api_gw, overlay)
            result = subprocess.run(
                ["kubectl", "--kubeconfig", KUBECONFIG, "kustomize", path],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0,
                             f"kubectl kustomize {overlay} failed: {result.stderr}")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
