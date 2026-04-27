#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG", os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml"))
LAB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lab")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestContainerInfo(unittest.TestCase):
    def test_pod_is_running(self):
        """Pod tigers-reunite is running in namespace project-tiger"""
        phase = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger",
                        "--ignore-not-found", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running", "Pod tigers-reunite is not Running")

    def test_single_container(self):
        """Pod has single container"""
        containers = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger",
                             "-o", "jsonpath={range .spec.containers[*]}{.name} {end}")
        self.assertEqual(len(containers.split()), 1, "Pod should have exactly one container")

    def test_container_image(self):
        """Pod container has correct image httpd:2-alpine"""
        image = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger",
                        "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_pod_labels(self):
        """Pod has correct labels (pod=container, container=pod)"""
        labels = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger",
                         "-o", "jsonpath={.metadata.labels}")
        self.assertIn('"pod":"container"', labels)
        self.assertIn('"container":"pod"', labels)

    def test_pod_container_txt_content(self):
        """lab/pod-container.txt contains correct container ID and runtimeType"""
        txt_path = os.path.join(LAB_DIR, "pod-container.txt")
        self.assertTrue(os.path.exists(txt_path), f"{txt_path} does not exist")

        with open(txt_path, 'r') as f:
            content = f.read().strip()

        parts = content.split()
        self.assertEqual(len(parts), 2, "pod-container.txt should have two parts: ID and runtimeType")
        container_id, runtime_type = parts
        self.assertEqual(runtime_type, "io.containerd.runc.v2")
        self.assertTrue(len(container_id) > 0)

    def test_pod_container_log_not_empty(self):
        """lab/pod-container.log contains container logs"""
        log_path = os.path.join(LAB_DIR, "pod-container.log")
        self.assertTrue(os.path.exists(log_path), f"{log_path} does not exist")

        with open(log_path, 'r') as f:
            content = f.read().strip()

        self.assertTrue(len(content) > 0, "pod-container.log should not be empty")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
