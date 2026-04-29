#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# Priority: 1. Environment Variable, 2. Local lab directory
KUBECONFIG = os.environ.get("KUBECONFIG")
if not KUBECONFIG:
    KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result

class TestRBACDeploymentManager(unittest.TestCase):
    def test_namespace_ci_exists(self):
        res = kubectl("get", "namespace", "ci")
        self.assertEqual(res.returncode, 0, f"Namespace 'ci' does not exist. Error: {res.stderr}")

    def test_serviceaccount_cicd_sa_exists(self):
        res = kubectl("get", "serviceaccount", "cicd-sa", "-n", "ci")
        self.assertEqual(res.returncode, 0, f"ServiceAccount 'cicd-sa' does not exist in namespace 'ci'. Error: {res.stderr}")

    def test_role_deployment_manager_exists(self):
        res = kubectl("get", "role", "deployment-manager", "-n", "ci", "-o", "json")
        self.assertEqual(res.returncode, 0, f"Role 'deployment-manager' does not exist in namespace 'ci'. Error: {res.stderr}")
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
        self.assertEqual(res.returncode, 0, f"RoleBinding 'cicd-sa-deployment-manager' does not exist in namespace 'ci'. Error: {res.stderr}")
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
        self.assertIn("yes", res.stdout.strip().lower(), f"ServiceAccount cannot create deployments. Output: {res.stdout}, Error: {res.stderr}")

        # Cannot get pods
        res = kubectl("auth", "can-i", "get", "pods", "--as", "system:serviceaccount:ci:cicd-sa", "-n", "ci")
        self.assertIn("no", res.stdout.strip().lower(), f"ServiceAccount can get pods but should not. Output: {res.stdout}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
