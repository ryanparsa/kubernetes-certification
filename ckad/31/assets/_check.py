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
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestAllowTrafficNetworkPolicy(unittest.TestCase):

    def _get_netpol(self):
        raw = kubectl("get", "networkpolicy", "allow-traffic", "-n", "networking",
                      "--ignore-not-found", "-o", "json")
        return json.loads(raw) if raw else {}

    def test_networkpolicy_exists(self):
        """NetworkPolicy allow-traffic exists in namespace networking"""
        name = kubectl("get", "networkpolicy", "allow-traffic", "-n", "networking",
                       "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "allow-traffic",
                         "NetworkPolicy 'allow-traffic' not found in namespace 'networking'")

    def test_pod_selector_matches_app_web(self):
        """NetworkPolicy selects pods with label app=web"""
        np = self._get_netpol()
        self.assertTrue(np, "NetworkPolicy not found")
        match_labels = np.get("spec", {}).get("podSelector", {}).get("matchLabels", {})
        self.assertEqual(match_labels.get("app"), "web",
                         f"podSelector.matchLabels.app should be 'web', got {match_labels!r}")

    def test_ingress_from_frontend_on_port_80(self):
        """NetworkPolicy allows ingress only from pods with label tier=frontend on TCP port 80"""
        np = self._get_netpol()
        self.assertTrue(np, "NetworkPolicy not found")
        spec = np.get("spec", {})

        # Must have Ingress in policyTypes
        policy_types = spec.get("policyTypes", [])
        self.assertIn("Ingress", policy_types,
                      f"policyTypes should include 'Ingress', got {policy_types!r}")

        ingress_rules = spec.get("ingress", [])
        self.assertTrue(ingress_rules, "No ingress rules defined")

        # Check at least one rule: from tier=frontend on TCP/80
        found_frontend_source = False
        found_port_80 = False
        for rule in ingress_rules:
            from_peers = rule.get("from", [])
            for peer in from_peers:
                peer_labels = peer.get("podSelector", {}).get("matchLabels", {})
                if peer_labels.get("tier") == "frontend":
                    found_frontend_source = True

            ports = rule.get("ports", [])
            for p in ports:
                if p.get("protocol") == "TCP" and p.get("port") == 80:
                    found_port_80 = True

        self.assertTrue(found_frontend_source,
                        "No ingress rule allows traffic from pods with label 'tier=frontend'")
        self.assertTrue(found_port_80,
                        "No ingress rule specifies TCP port 80")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
