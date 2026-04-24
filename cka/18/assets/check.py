#!/usr/bin/env python3

import os
import subprocess
import unittest
import json
import time

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestDNSFQDNHeadlessService(unittest.TestCase):

    def test_dns_1_in_configmap(self):
        val = kubectl("get", "cm", "control-config", "-n", "lima-control", "-o", "jsonpath={.data.DNS_1}")
        self.assertEqual(val, "kubernetes.default.svc.cluster.local")

    def test_dns_2_in_configmap(self):
        val = kubectl("get", "cm", "control-config", "-n", "lima-control", "-o", "jsonpath={.data.DNS_2}")
        self.assertEqual(val, "department.lima-workload.svc.cluster.local")

    def test_dns_3_in_configmap(self):
        val = kubectl("get", "cm", "control-config", "-n", "lima-control", "-o", "jsonpath={.data.DNS_3}")
        self.assertEqual(val, "section100.section.lima-workload.svc.cluster.local")

    def test_dns_4_in_configmap(self):
        val = kubectl("get", "cm", "control-config", "-n", "lima-control", "-o", "jsonpath={.data.DNS_4}")
        self.assertEqual(val, "1-2-3-4.kube-system.pod.cluster.local")

    def test_deployment_env_values(self):
        # Give it a few retries as pods might be transitioning
        for _ in range(5):
            res = kubectl("get", "pod", "-n", "lima-control", "-l", "app=controller", "--field-selector=status.phase=Running", "-o", "json")
            if not res:
                time.sleep(2)
                continue

            pods_data = json.loads(res)
            valid_pods = [p for p in pods_data.get("items", []) if not p["metadata"].get("deletionTimestamp")]

            if not valid_pods:
                time.sleep(2)
                continue

            # Check the first valid pod found
            name = valid_pods[0]["metadata"]["name"]
            dns_1 = kubectl("exec", "-n", "lima-control", name, "--", "sh", "-c", "echo $DNS_1")

            if dns_1 == "kubernetes.default.svc.cluster.local":
                return # Success

            time.sleep(2)

        self.fail("Deployment pods not using updated ConfigMap values after retries")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
