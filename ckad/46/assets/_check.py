#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(SCRIPT_DIR, "../lab/kubeconfig.yaml")

def kubectl(*args):
    env = os.environ.copy()
    env["KUBECONFIG"] = KUBECONFIG
    result = subprocess.run(
        ["kubectl", *args],
        capture_output=True, text=True, env=env
    )
    return result.stdout.strip()

class TestNetworkPolicyLab(unittest.TestCase):
    def test_namespace_exists(self):
        ns = kubectl("get", "ns", "networking", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "networking")

    def test_pods_created(self):
        pods = ["secure-db", "frontend", "monitoring"]
        for pod in pods:
            status = kubectl("get", "pod", pod, "-n", "networking", "-o", "jsonpath={.status.phase}")
            self.assertEqual(status, "Running")

    def test_network_policy_exists(self):
        name = kubectl("get", "networkpolicy", "db-network-policy", "-n", "networking", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "db-network-policy")

    def test_network_policy_selector(self):
        selector = kubectl("get", "networkpolicy", "db-network-policy", "-n", "networking", "-o", "jsonpath={.spec.podSelector.matchLabels.app}")
        self.assertEqual(selector, "db")

    def test_network_policy_ingress(self):
        # Check ingress from role=frontend on port 5432
        ingress_from = kubectl("get", "networkpolicy", "db-network-policy", "-n", "networking", "-o", "jsonpath={.spec.ingress[?(@.ports[0].port==5432)].from[0].podSelector.matchLabels.role}")
        self.assertEqual(ingress_from, "frontend")

    def test_network_policy_egress(self):
        # Check egress to role=monitoring on port 8080
        egress_to = kubectl("get", "networkpolicy", "db-network-policy", "-n", "networking", "-o", "jsonpath={.spec.egress[?(@.ports[0].port==8080)].to[0].podSelector.matchLabels.role}")
        self.assertEqual(egress_to, "monitoring")

if __name__ == "__main__":
    unittest.main(verbosity=2)
