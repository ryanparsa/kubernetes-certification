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
    return result

class TestRBACLab63(unittest.TestCase):
    def test_service_account_exists(self):
        res = kubectl("get", "sa", "app-admin", "-n", "cluster-admin")
        self.assertEqual(res.returncode, 0, "ServiceAccount app-admin does not exist in cluster-admin namespace")

    def test_role_pods_permissions(self):
        res = kubectl("auth", "can-i", "list", "pods", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot list pods")
        res = kubectl("auth", "can-i", "get", "pods", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot get pods")
        res = kubectl("auth", "can-i", "watch", "pods", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot watch pods")

    def test_role_deployments_permissions(self):
        res = kubectl("auth", "can-i", "list", "deployments", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot list deployments")
        res = kubectl("auth", "can-i", "update", "deployments", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot update deployments")

    def test_role_configmaps_permissions(self):
        res = kubectl("auth", "can-i", "create", "configmaps", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot create configmaps")
        res = kubectl("auth", "can-i", "delete", "configmaps", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "yes", "SA cannot delete configmaps")

    def test_role_binding_exists(self):
        res = kubectl("get", "rolebinding", "app-admin", "-n", "cluster-admin")
        self.assertEqual(res.returncode, 0, "RoleBinding app-admin does not exist")

    def test_pod_exists_and_uses_sa(self):
        res = kubectl("get", "pod", "admin-pod", "-n", "cluster-admin", "-o", "json")
        self.assertEqual(res.returncode, 0, "Pod admin-pod does not exist")
        pod = json.loads(res.stdout)
        self.assertEqual(pod["spec"]["serviceAccountName"], "app-admin", "Pod does not use correct ServiceAccount")
        self.assertEqual(pod["spec"]["containers"][0]["image"], "bitnami/kubectl:latest", "Pod does not use correct image")

    def test_denied_operations(self):
        res = kubectl("auth", "can-i", "create", "pods", "-n", "cluster-admin", "--as", "system:serviceaccount:cluster-admin:app-admin")
        self.assertEqual(res.stdout.strip(), "no", "SA should NOT be able to create pods")

if __name__ == "__main__":
    unittest.main(verbosity=2)
