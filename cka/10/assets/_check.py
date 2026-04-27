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

def can_i(verb, resource, namespace="project-hamster"):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, "-n", namespace,
         "auth", "can-i", verb, resource,
         "--as", "system:serviceaccount:project-hamster:processor"],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestRBACServiceAccountRoleRoleBinding(unittest.TestCase):

    def test_serviceaccount_exists(self):
        name = kubectl("get", "serviceaccount", "processor", "-n", "project-hamster",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "processor")

    def test_role_exists(self):
        name = kubectl("get", "role", "processor", "-n", "project-hamster",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "processor")

    def test_rolebinding_exists(self):
        name = kubectl("get", "rolebinding", "processor", "-n", "project-hamster",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "processor")

    def test_role_allows_create_secrets(self):
        self.assertEqual(can_i("create", "secrets"), "yes")

    def test_role_allows_create_configmaps(self):
        self.assertEqual(can_i("create", "configmaps"), "yes")

    def test_role_denies_create_pods(self):
        self.assertEqual(can_i("create", "pods"), "no")

    def test_role_denies_delete_secrets(self):
        self.assertEqual(can_i("delete", "secrets"), "no")

    def test_role_denies_get_configmaps(self):
        self.assertEqual(can_i("get", "configmaps"), "no")

    def test_rolebinding_references_correct_role(self):
        role = kubectl("get", "rolebinding", "processor", "-n", "project-hamster",
                       "-o", "jsonpath={.roleRef.name}")
        self.assertEqual(role, "processor")

    def test_rolebinding_references_correct_serviceaccount(self):
        sa = kubectl("get", "rolebinding", "processor", "-n", "project-hamster",
                     "-o", "jsonpath={.subjects[0].name}")
        self.assertEqual(sa, "processor")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
