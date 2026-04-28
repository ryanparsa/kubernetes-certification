#!/usr/bin/env python3

import json
import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestAppStackNetworkPolicy(unittest.TestCase):

    def _get_netpol(self):
        raw = kubectl("get", "networkpolicy", "app-stack-network-policy",
                      "-n", "app-stack", "--ignore-not-found", "-o", "json")
        return json.loads(raw) if raw else {}

    def test_namespace_exists(self):
        """Namespace app-stack exists"""
        name = kubectl("get", "namespace", "app-stack",
                       "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "app-stack", "Namespace 'app-stack' not found")

    def test_pods_running(self):
        """Pods frontend, backend, and database are running in app-stack"""
        for pod_name in ("frontend", "backend", "database"):
            phase = kubectl("get", "pod", pod_name, "-n", "app-stack",
                            "--ignore-not-found", "-o", "jsonpath={.status.phase}")
            self.assertEqual(phase, "Running",
                             f"Pod '{pod_name}' in namespace 'app-stack' is not Running (got: '{phase}')")

    def test_networkpolicy_exists(self):
        """NetworkPolicy app-stack-network-policy exists in app-stack"""
        name = kubectl("get", "networkpolicy", "app-stack-network-policy",
                       "-n", "app-stack", "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "app-stack-network-policy",
                         "NetworkPolicy 'app-stack-network-policy' not found in namespace 'app-stack'")

    def test_policy_targets_database_pod(self):
        """NetworkPolicy targets pods with labels app=todo, tier=database"""
        np = self._get_netpol()
        self.assertTrue(np, "NetworkPolicy not found")
        match_labels = np.get("spec", {}).get("podSelector", {}).get("matchLabels", {})
        self.assertEqual(match_labels.get("app"), "todo",
                         f"podSelector.matchLabels.app should be 'todo', got {match_labels!r}")
        self.assertEqual(match_labels.get("tier"), "database",
                         f"podSelector.matchLabels.tier should be 'database', got {match_labels!r}")

    def test_ingress_from_backend_on_port_3306(self):
        """NetworkPolicy allows ingress from tier=backend on TCP port 3306 only"""
        np = self._get_netpol()
        self.assertTrue(np, "NetworkPolicy not found")
        spec = np.get("spec", {})

        policy_types = spec.get("policyTypes", [])
        self.assertIn("Ingress", policy_types,
                      f"policyTypes should include 'Ingress', got {policy_types!r}")

        ingress_rules = spec.get("ingress", [])
        self.assertTrue(ingress_rules, "No ingress rules defined")

        found_backend_source = False
        found_port_3306 = False
        for rule in ingress_rules:
            for peer in rule.get("from", []):
                peer_labels = peer.get("podSelector", {}).get("matchLabels", {})
                if peer_labels.get("tier") == "backend":
                    found_backend_source = True

            for p in rule.get("ports", []):
                if p.get("protocol") == "TCP" and p.get("port") == 3306:
                    found_port_3306 = True

        self.assertTrue(found_backend_source,
                        "No ingress rule allows traffic from pods with label 'tier=backend'")
        self.assertTrue(found_port_3306,
                        "No ingress rule specifies TCP port 3306")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
