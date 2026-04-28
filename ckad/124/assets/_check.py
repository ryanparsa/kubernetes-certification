#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE):
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestSecretManagerRBAC(unittest.TestCase):
    def test_sa_exists(self):
        # ServiceAccount secret-manager exists in Namespace sun
        value = kubectl("get", "sa", "secret-manager", "-n", "sun", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(value, "secret-manager")

    def test_rolebinding_exists(self):
        # RoleBinding secret-manager in Namespace sun binds ServiceAccount to ClusterRole secret-manager
        cr = kubectl("get", "rolebinding", "secret-manager", "-n", "sun", "-o", "jsonpath={.roleRef.name}")
        self.assertEqual(cr, "secret-manager")

        sa = kubectl("get", "rolebinding", "secret-manager", "-n", "sun", "-o", "jsonpath={.subjects[0].name}")
        self.assertEqual(sa, "secret-manager")

        ns = kubectl("get", "rolebinding", "secret-manager", "-n", "sun", "-o", "jsonpath={.subjects[0].namespace}")
        self.assertEqual(ns, "sun")

    def test_auth_sun(self):
        # ServiceAccount can get Secrets in Namespace sun
        res = kubectl("auth", "can-i", "get", "secrets", "-n", "sun", "--as", "system:serviceaccount:sun:secret-manager")
        self.assertEqual(res, "yes")

    def test_auth_moon(self):
        # ServiceAccount cannot get Secrets in Namespace moon
        res = kubectl("auth", "can-i", "get", "secrets", "-n", "moon", "--as", "system:serviceaccount:sun:secret-manager")
        self.assertEqual(res, "no")

if __name__ == "__main__":
    unittest.main(verbosity=2)
