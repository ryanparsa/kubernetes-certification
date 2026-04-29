#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestAppReader(unittest.TestCase):
    def test_cluster_role(self):
        # Check ClusterRole app-reader exists and has correct permissions
        output = kubectl("get", "clusterrole", "app-reader", "-o", "json")
        role = json.loads(output)
        rules = role.get("rules", [])

        pod_rule = next((r for r in rules if "" in r.get("apiGroups", []) and "pods" in r.get("resources", [])), None)
        deploy_rule = next((r for r in rules if "apps" in r.get("apiGroups", []) and "deployments" in r.get("resources", [])), None)

        self.assertIsNotNone(pod_rule)
        self.assertIn("get", pod_rule.get("verbs", []))
        self.assertIn("list", pod_rule.get("verbs", []))
        self.assertIn("watch", pod_rule.get("verbs", []))

        self.assertIsNotNone(deploy_rule)
        self.assertIn("get", deploy_rule.get("verbs", []))
        self.assertIn("list", deploy_rule.get("verbs", []))
        self.assertIn("watch", deploy_rule.get("verbs", []))

    def test_cluster_role_binding(self):
        # Check ClusterRoleBinding app-reader exists and binds to the right SA
        output = kubectl("get", "clusterrolebinding", "app-reader", "-o", "json")
        binding = json.loads(output)

        self.assertEqual(binding.get("roleRef", {}).get("name"), "app-reader")
        subjects = binding.get("subjects", [])
        sa_subject = next((s for s in subjects if s.get("kind") == "ServiceAccount" and s.get("name") == "app-reader" and s.get("namespace") == "app"), None)
        self.assertIsNotNone(sa_subject)

    def test_kubeconfig_context(self):
        # Check context app-context exists and uses namespace app
        output = kubectl("config", "view", "-o", "json")
        config = json.loads(output)
        contexts = config.get("contexts", [])
        app_context = next((c for c in contexts if c.get("name") == "app-context"), None)

        self.assertIsNotNone(app_context)
        self.assertEqual(app_context.get("context", {}).get("namespace"), "app")

if __name__ == "__main__":
    unittest.main(verbosity=2)
