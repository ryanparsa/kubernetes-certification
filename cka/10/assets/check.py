#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def can_i(verb, resource, namespace="project-hamster"):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(["-n", namespace, "auth", "can-i", verb, resource, "--as", "system:serviceaccount:project-hamster:processor"])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestRBACServiceAccountRoleRoleBinding(unittest.TestCase):

    def test_serviceaccount_exists(self):
        name = kubectl("get", "serviceaccount", "processor", "-n", "project-hamster", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "processor")

    def test_role_exists(self):
        name = kubectl("get", "role", "processor", "-n", "project-hamster", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "processor")

    def test_rolebinding_exists(self):
        name = kubectl("get", "rolebinding", "processor", "-n", "project-hamster", "-o", "jsonpath={.metadata.name}")
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

if __name__ == "__main__":
    unittest.main(verbosity=2)
