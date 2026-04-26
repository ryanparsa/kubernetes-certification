#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

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

class TestMultiContainerPlayground(unittest.TestCase):
    def setUp(self):
        self.pod_json = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "json")
        self.pod = json.loads(self.pod_json) if self.pod_json else {}

    def test_pod_is_running(self):
        status = kubectl("get", "pod", "multi-container-playground", "-n", "default", "-o", "jsonpath={.status.phase}")
        self.assertEqual(status, "Running")

    def test_pod_has_three_containers(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(len(containers), 3)

    def test_pod_has_three_ready_containers(self):
        container_statuses = self.pod.get("status", {}).get("containerStatuses", [])
        ready_count = sum(1 for cs in container_statuses if cs.get("ready"))
        self.assertEqual(ready_count, 3)

    def test_container_1_name(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[0].get("name"), "c1")

    def test_container_1_image(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[0].get("image"), "nginx:1-alpine")

    def test_container_1_env_my_node_name(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        env = containers[0].get("env", [])
        my_node_name_env = next((e for e in env if e.get("name") == "MY_NODE_NAME"), None)
        self.assertIsNotNone(my_node_name_env)
        self.assertEqual(my_node_name_env.get("valueFrom", {}).get("fieldRef", {}).get("fieldPath"), "spec.nodeName")

    def test_container_2_name(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[1].get("name"), "c2")

    def test_container_2_image(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[1].get("image"), "busybox:1")

    def test_container_3_name(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[2].get("name"), "c3")

    def test_container_3_image(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        self.assertEqual(containers[2].get("image"), "busybox:1")

    def test_all_containers_have_volume_mounted(self):
        containers = self.pod.get("spec", {}).get("containers", [])
        for c in containers:
            mounts = c.get("volumeMounts", [])
            vol_mount = next((m for m in mounts if m.get("name") == "vol"), None)
            self.assertIsNotNone(vol_mount, f"Container {c.get('name')} missing volume mount 'vol'")
            self.assertEqual(vol_mount.get("mountPath"), "/vol")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=QuietResult, verbosity=2)
    unittest.main(testRunner=runner)
