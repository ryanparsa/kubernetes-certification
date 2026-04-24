#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KUBECONFIG = os.path.join(SCRIPT_DIR, "kubeconfig.yaml")
LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CLUSTER_NAME = f"{EXAM}-lab-{LAB_ID}"

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class QuietResult(unittest.TextTestResult):
    def addSuccess(self, test):
        pass
    def addError(self, test, err):
        super().addError(test, err)
    def addFailure(self, test, err):
        super().addFailure(test, err)

class TestStaticPodAndService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pod_name = f"my-static-pod-{CLUSTER_NAME}-control-plane"
        cls.pod_json = kubectl("get", "pod", cls.pod_name, "-n", "default", "-o", "json")
        if cls.pod_json:
            cls.pod_data = json.loads(cls.pod_json)
        else:
            cls.pod_data = {}

        cls.svc_json = kubectl("get", "svc", "static-pod-service", "-n", "default", "-o", "json")
        if cls.svc_json:
            cls.svc_data = json.loads(cls.svc_json)
        else:
            cls.svc_data = {}

    def test_static_pod_exists(self):
        """Static Pod my-static-pod exists on control-plane"""
        self.assertTrue(self.pod_data, f"Pod {self.pod_name} not found")
        self.assertEqual(self.pod_data.get("status", {}).get("phase"), "Running")

    def test_pod_has_single_container(self):
        """Pod has single container"""
        containers = self.pod_data.get("spec", {}).get("containers", [])
        self.assertEqual(len(containers), 1)

    def test_container_image(self):
        """Container has correct image nginx:1-alpine"""
        containers = self.pod_data.get("spec", {}).get("containers", [])
        if containers:
            self.assertEqual(containers[0].get("image"), "nginx:1-alpine")
        else:
            self.fail("No containers found in pod")

    def test_cpu_requests(self):
        """Pod has correct CPU resource requests"""
        containers = self.pod_data.get("spec", {}).get("containers", [])
        if containers:
            requests = containers[0].get("resources", {}).get("requests", {})
            self.assertEqual(requests.get("cpu"), "10m")
        else:
            self.fail("No containers found in pod")

    def test_memory_requests(self):
        """Pod has correct memory resource requests"""
        containers = self.pod_data.get("spec", {}).get("containers", [])
        if containers:
            requests = containers[0].get("resources", {}).get("requests", {})
            self.assertEqual(requests.get("memory"), "20Mi")
        else:
            self.fail("No containers found in pod")

    def test_service_type_nodeport(self):
        """Service is of type NodePort"""
        self.assertTrue(self.svc_data, "Service static-pod-service not found")
        self.assertEqual(self.svc_data.get("spec", {}).get("type"), "NodePort")

    def test_service_selector(self):
        """Service selector matches Pod"""
        self.assertTrue(self.svc_data, "Service static-pod-service not found")
        selector = self.svc_data.get("spec", {}).get("selector", {})
        self.assertEqual(selector.get("run"), "my-static-pod")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=QuietResult, verbosity=2)
    unittest.main(testRunner=runner)
