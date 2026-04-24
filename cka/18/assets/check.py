#!/usr/bin/env python3

import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

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
        # Check if the deployment is using the updated values by checking one of the pods
        pod_name = kubectl("get", "pod", "-n", "lima-control", "-l", "app=controller", "-o", "jsonpath={.items[0].metadata.name}")
        if not pod_name:
            self.fail("No controller pod found")

        dns_1 = kubectl("exec", "-n", "lima-control", pod_name, "--", "sh", "-c", "echo $DNS_1")
        self.assertEqual(dns_1, "kubernetes.default.svc.cluster.local")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
