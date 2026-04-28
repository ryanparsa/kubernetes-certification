#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestNeptuneMaintenance(unittest.TestCase):
    def test_neptune_10ab_scaled_to_0(self):
        replicas = kubectl("get", "deployment", "neptune-10ab", "-n", "neptune", "-o", "jsonpath={.spec.replicas}")
        self.assertEqual(replicas, "0")

    def test_neptune_10ab_pods_terminated(self):
        pod_count = kubectl("get", "pods", "-n", "neptune", "-l", "app=neptune-10ab", "--no-headers")
        self.assertEqual(pod_count, "")

    def test_neptune_20ab_annotated(self):
        annotation = kubectl("get", "deployment", "neptune-20ab", "-n", "neptune", "-o", "jsonpath={.metadata.annotations['admission\\.datree\\.io/warn']}")
        self.assertEqual(annotation, "true")

    def test_neptune_20ab_protected(self):
        # Check for finalizer or last-applied-configuration as requested in README
        finalizers = kubectl("get", "deployment", "neptune-20ab", "-n", "neptune", "-o", "jsonpath={.metadata.finalizers}")
        last_applied = kubectl("get", "deployment", "neptune-20ab", "-n", "neptune", "-o", "jsonpath={.metadata.annotations['kubectl\\.kubernetes\\.io/last-applied-configuration']}")

        is_protected = "kubernetes.io/prevent-deletion" in finalizers or last_applied != ""
        self.assertTrue(is_protected, "Deployment neptune-20ab should be protected from deletion")

if __name__ == "__main__":
    unittest.main(verbosity=2)
