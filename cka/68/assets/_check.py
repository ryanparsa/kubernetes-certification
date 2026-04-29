#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG = os.environ.get("KUBECONFIG", os.path.join(SCRIPT_DIR, "kubeconfig.yaml"))

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result

class TestRBACDeploymentManager(unittest.TestCase):
    def test_namespace_ci_exists(self):
        res = kubectl("get", "namespace", "ci")
        self.assertEqual(res.returncode, 0, "Namespace 'ci' does not exist")

    def test_serviceaccount_cicd_sa_exists(self):
        res = kubectl("get", "serviceaccount", "cicd-sa", "-n", "ci")
        self.assertEqual(res.returncode, 0, "ServiceAccount 'cicd-sa' does not exist in namespace 'ci'")

    def test_role_deployment_manager_exists(self):
        res = kubectl("get", "role", "deployment-manager", "-n", "ci", "-o", "json")
        self.assertEqual(res.returncode, 0, "Role 'deployment-manager' does not exist in namespace 'ci'")
        role = json.loads(res.stdout)

        allowed_verbs = set()
        for rule in role.get("rules", []):
            if "apps" in rule.get("apiGroups", []) or "*" in rule.get("apiGroups", []):
                if "deployments" in rule.get("resources", []) or "*" in rule.get("resources", []):
                    allowed_verbs.update(rule.get("verbs", []))

        self.assertTrue(set(["create", "update", "delete"]).issubset(allowed_verbs),
                        f"Role 'deployment-manager' does not have correct permissions on deployments. Found verbs: {allowed_verbs}")

    def test_rolebinding_cicd_sa_deployment_manager_exists(self):
        res = kubectl("get", "rolebinding", "cicd-sa-deployment-manager", "-n", "ci", "-o", "json")
        self.assertEqual(res.returncode, 0, "RoleBinding 'cicd-sa-deployment-manager' does not exist in namespace 'ci'")
        rb = json.loads(res.stdout)

        self.assertEqual(rb.get("roleRef", {}).get("name"), "deployment-manager")

        found_subject = False
        for subject in rb.get("subjects", []):
            if subject.get("kind") == "ServiceAccount" and subject.get("name") == "cicd-sa" and subject.get("namespace") == "ci":
                found_subject = True
                break
        self.assertTrue(found_subject, "RoleBinding does not bind to ServiceAccount 'cicd-sa' in namespace 'ci'")

    def test_permissions_verification(self):
        # Can create deployments
        res = kubectl("auth", "can-i", "create", "deployments", "--as", "system:serviceaccount:ci:cicd-sa", "-n", "ci")
        self.assertIn("yes", res.stdout.strip().lower())

        # Cannot get pods
        res = kubectl("auth", "can-i", "get", "pods", "--as", "system:serviceaccount:ci:cicd-sa", "-n", "ci")
        self.assertIn("no", res.stdout.strip().lower())

if __name__ == "__main__":
    unittest.main(verbosity=2)
