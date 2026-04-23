#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestNetworkPolicy(unittest.TestCase):

    def test_networkpolicy_exists(self):
        name = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "np-backend")

    def test_pod_selector(self):
        selector = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake", "-o", "jsonpath={.spec.podSelector.matchLabels.app}")
        self.assertEqual(selector, "backend")

    def test_egress_policy_type(self):
        policy_types = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake", "-o", "jsonpath={.spec.policyTypes}")
        self.assertIn("Egress", policy_types)

    def test_egress_to_db1_port_1111(self):
        egress = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake", "-o", "jsonpath={.spec.egress}")
        self.assertIn("db1", egress)
        self.assertIn("1111", egress)

    def test_egress_to_db2_port_2222(self):
        egress = kubectl("get", "networkpolicy", "np-backend", "-n", "project-snake", "-o", "jsonpath={.spec.egress}")
        self.assertIn("db2", egress)
        self.assertIn("2222", egress)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
