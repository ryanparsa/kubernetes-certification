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

def can_i(verb, resource, namespace="project-hamster"):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, "-n", namespace,
         "auth", "can-i", verb, resource,
         "--as", "system:serviceaccount:project-hamster:processor"],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestProcessorRBAC(unittest.TestCase):
    def test_serviceaccount_exists(self):
        val = kubectl("-n", "project-hamster", "get", "sa", "processor", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(val, "processor")

    def test_role_exists(self):
        val = kubectl("-n", "project-hamster", "get", "role", "processor", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(val, "processor")

    def test_rolebinding_exists(self):
        val = kubectl("-n", "project-hamster", "get", "rolebinding", "processor", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(val, "processor")

    def test_can_create_secrets(self):
        self.assertEqual(can_i("create", "secrets"), "yes")

    def test_can_create_configmaps(self):
        self.assertEqual(can_i("create", "configmaps"), "yes")

    def test_cannot_delete_secrets(self):
        self.assertEqual(can_i("delete", "secrets"), "no")

if __name__ == "__main__":
    unittest.main()
