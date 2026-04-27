#!/usr/bin/env python3
import os
import subprocess
import unittest

LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


class TestDNSConfigMap(unittest.TestCase):

    def test_dns1_in_configmap(self):
        value = kubectl("get", "configmap", "control-config", "-n", "lima-control",
                        "-o", "jsonpath={.data.DNS_1}")
        self.assertEqual(value, "kubernetes.default.svc.cluster.local")

    def test_dns2_in_configmap(self):
        value = kubectl("get", "configmap", "control-config", "-n", "lima-control",
                        "-o", "jsonpath={.data.DNS_2}")
        self.assertEqual(value, "department.lima-workload.svc.cluster.local")

    def test_dns3_in_configmap(self):
        value = kubectl("get", "configmap", "control-config", "-n", "lima-control",
                        "-o", "jsonpath={.data.DNS_3}")
        self.assertEqual(value, "section100.section.lima-workload.svc.cluster.local")

    def test_dns4_in_configmap(self):
        value = kubectl("get", "configmap", "control-config", "-n", "lima-control",
                        "-o", "jsonpath={.data.DNS_4}")
        self.assertEqual(value, "1-2-3-4.kube-system.pod.cluster.local")

    def test_deployment_has_correct_configmap_values(self):
        # Confirm the Deployment is fully available with the updated ConfigMap
        available = kubectl("get", "deployment", "controller", "-n", "lima-control",
                            "-o", "jsonpath={.status.availableReplicas}")
        self.assertTrue(available and int(available) > 0,
                        "Deployment controller has no available replicas")
        # Verify pod env vars reflect the updated ConfigMap
        pod_name = kubectl("get", "pod", "-n", "lima-control",
                           "-l", "app=controller",
                           "-o", "jsonpath={.items[0].metadata.name}")
        self.assertTrue(pod_name, "No controller pod found")
        dns1_env = kubectl("exec", "-n", "lima-control", pod_name, "--",
                           "sh", "-c", "echo $DNS_1")
        self.assertEqual(dns1_env.strip(), "kubernetes.default.svc.cluster.local")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
