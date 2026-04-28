#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
KUBECONFIG_FILE = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


class TestApiNetworkPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        res = kubectl("get", "networkpolicy", "api-policy", "-n", "network-test", "-o", "json")
        cls.policy = json.loads(res.stdout) if res.returncode == 0 else None

    def test_networkpolicy_targets_api_pods(self):
        self.assertIsNotNone(self.policy, "NetworkPolicy 'api-policy' not found in namespace 'network-test'")
        selector = self.policy["spec"]["podSelector"].get("matchLabels", {})
        self.assertEqual(selector.get("role"), "api", "podSelector does not target role=api")

    def test_policy_types_include_ingress_and_egress(self):
        self.assertIsNotNone(self.policy)
        types = self.policy["spec"].get("policyTypes", [])
        self.assertIn("Ingress", types, "policyTypes does not include Ingress")
        self.assertIn("Egress", types, "policyTypes does not include Egress")

    def test_ingress_from_frontend_on_tcp_80(self):
        self.assertIsNotNone(self.policy)
        ingress = self.policy["spec"].get("ingress", [])
        found = False
        for rule in ingress:
            for frm in rule.get("from", []):
                pod_sel = frm.get("podSelector", {}).get("matchLabels", {})
                if pod_sel.get("role") == "frontend":
                    for port in rule.get("ports", []):
                        if port.get("protocol", "TCP") == "TCP" and port.get("port") == 80:
                            found = True
        self.assertTrue(found, "Ingress rule from role=frontend on TCP/80 not found")

    def test_egress_to_db_on_tcp_5432(self):
        self.assertIsNotNone(self.policy)
        egress = self.policy["spec"].get("egress", [])
        found = False
        for rule in egress:
            for to in rule.get("to", []):
                pod_sel = to.get("podSelector", {}).get("matchLabels", {})
                if pod_sel.get("role") == "db":
                    for port in rule.get("ports", []):
                        if port.get("protocol", "TCP") == "TCP" and port.get("port") == 5432:
                            found = True
        self.assertTrue(found, "Egress rule to role=db on TCP/5432 not found")

    def test_egress_dns_udp_53_to_any_namespace(self):
        self.assertIsNotNone(self.policy)
        egress = self.policy["spec"].get("egress", [])
        found = False
        for rule in egress:
            has_udp_53 = any(
                p.get("protocol") == "UDP" and p.get("port") == 53
                for p in rule.get("ports", [])
            )
            has_ns_selector = any("namespaceSelector" in to for to in rule.get("to", []))
            if has_udp_53 and has_ns_selector:
                found = True
        self.assertTrue(found, "Egress DNS rule (UDP/53 to any namespace via namespaceSelector) not found")


if __name__ == "__main__":
    unittest.main(verbosity=2)
