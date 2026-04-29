#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(__file__)
KUBECONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")

# Use local kubeconfig if it exists, otherwise rely on environment (CI)
KUBECONFIG = KUBECONFIG_PATH if os.path.exists(KUBECONFIG_PATH) else os.environ.get("KUBECONFIG")

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

class TestLimitConsumer(unittest.TestCase):
    def test_pods_running(self):
        for pod in ["consumer", "producer", "web"]:
            res = kubectl("get", "pod", pod, "-o", "jsonpath={.status.phase}")
            self.assertEqual(res.stdout.strip(), "Running", f"Pod {pod} is not running")

    def test_services_exist(self):
        for svc in ["consumer", "producer", "web"]:
            res = kubectl("get", "svc", svc, "-o", "jsonpath={.spec.ports[0].port}")
            self.assertEqual(res.stdout.strip(), "80", f"Service {svc} does not exist on port 80")

    def test_network_policy_selector(self):
        res = kubectl("get", "netpol", "limit-consumer", "-o", "jsonpath={.spec.podSelector.matchLabels.run}")
        self.assertEqual(res.stdout.strip(), "consumer", "NetworkPolicy does not select consumer pod")

    def test_network_policy_ingress_rule(self):
        # Allow ingress from producer
        res = kubectl("get", "netpol", "limit-consumer", "-o", "json")
        policy = json.loads(res.stdout)

        ingress = policy.get("spec", {}).get("ingress", [])
        self.assertTrue(len(ingress) > 0, "No ingress rules found")

        from_list = ingress[0].get("from", [])
        found_producer = False
        for f in from_list:
            if f.get("podSelector", {}).get("matchLabels", {}).get("run") == "producer":
                found_producer = True
                break

        self.assertTrue(found_producer, "NetworkPolicy does not allow ingress from producer")

    def test_connectivity(self):
        # Producer to Consumer should succeed
        res_prod = kubectl("exec", "producer", "--", "curl", "-s", "--max-time", "5", "http://consumer")
        self.assertEqual(res_prod.returncode, 0, "Producer should be able to reach consumer")

        # Web to Consumer should fail
        res_web = kubectl("exec", "web", "--", "curl", "-s", "--max-time", "5", "http://consumer")
        self.assertNotEqual(res_web.returncode, 0, "Web should NOT be able to reach consumer")

if __name__ == "__main__":
    unittest.main(verbosity=2)
