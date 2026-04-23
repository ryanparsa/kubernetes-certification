#!/usr/bin/env python3
import os
import subprocess
import unittest
import ipaddress

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

def docker_exec_cat(node, path):
    result = subprocess.run(
        ["docker", "exec", node, "cat", path],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestChangeServiceCIDR(unittest.TestCase):

    def test_pod_exists(self):
        phase = kubectl("get", "pod", "check-ip", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")
        image = kubectl("get", "pod", "check-ip", "-n", "default", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_service1_ip_range(self):
        ip = kubectl("get", "svc", "check-ip-service", "-n", "default", "-o", "jsonpath={.spec.clusterIP}")
        network = ipaddress.ip_network("10.96.0.0/12")
        self.assertIn(ipaddress.ip_address(ip), network)

    def test_service2_ip_range(self):
        ip = kubectl("get", "svc", "check-ip-service2", "-n", "default", "-o", "jsonpath={.spec.clusterIP}")
        network = ipaddress.ip_network("11.96.0.0/12")
        self.assertIn(ipaddress.ip_address(ip), network)

    def test_apiserver_config(self):
        manifest = docker_exec_cat("cka-lab-control-plane", "/etc/kubernetes/manifests/kube-apiserver.yaml")
        self.assertIn("--service-cluster-ip-range=11.96.0.0/12", manifest)

    def test_controller_manager_config(self):
        manifest = docker_exec_cat("cka-lab-control-plane", "/etc/kubernetes/manifests/kube-controller-manager.yaml")
        self.assertIn("--service-cluster-ip-range=11.96.0.0/12", manifest)

    def test_servicecidr_new_exists(self):
        cidrs = kubectl("get", "servicecidr", "svc-cidr-new", "-o", "jsonpath={.spec.cidrs[0]}")
        self.assertEqual(cidrs, "11.96.0.0/12")

    def test_servicecidr_kubernetes_deleted(self):
        # It might be in terminating state, so we check if it's either gone or has a deletion timestamp
        res = kubectl("get", "servicecidr", "kubernetes", "-o", "jsonpath={.metadata.deletionTimestamp}")
        # if kubectl returns error because it doesn't exist, that's also fine (but the wrapper might need adjustment)
        # For simplicity, if the resource is found, it must have a deletionTimestamp
        if res == "": # Not found or no deletion timestamp
            # Check if it actually exists
            check = subprocess.run(["kubectl", "--kubeconfig", KUBECONFIG, "get", "servicecidr", "kubernetes"], capture_output=True)
            if check.returncode == 0:
                self.fail("ServiceCIDR 'kubernetes' still exists and is not terminating")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
