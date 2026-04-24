#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.environ.get("KUBECONFIG", os.path.join(os.path.dirname(__file__), "kubeconfig.yaml"))
COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestContainerInfo(unittest.TestCase):
    def test_pod_exists_with_labels(self):
        """Pod tigers-reunite exists with correct labels in project-tiger namespace"""
        labels = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels}")
        self.assertIn('"pod":"container"', labels)
        self.assertIn('"container":"pod"', labels)

        image = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "httpd:2-alpine")

    def test_pod_is_running(self):
        """Pod is scheduled and running"""
        phase = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_pod_container_txt_content(self):
        """cka/17/course/pod-container.txt contains correct container ID and runtimeType"""
        txt_path = os.path.join(COURSE_DIR, "pod-container.txt")
        self.assertTrue(os.path.exists(txt_path), f"{txt_path} does not exist")

        with open(txt_path, 'r') as f:
            content = f.read().strip()

        parts = content.split()
        self.assertEqual(len(parts), 2, "pod-container.txt should have two parts: ID and runtimeType")

        container_id = parts[0]
        runtime_type = parts[1]

        self.assertEqual(runtime_type, "io.containerd.runc.v2")
        self.assertTrue(len(container_id) > 0)

    def test_pod_container_log_not_empty(self):
        """cka/17/course/pod-container.log contains container logs"""
        log_path = os.path.join(COURSE_DIR, "pod-container.log")
        self.assertTrue(os.path.exists(log_path), f"{log_path} does not exist")

        with open(log_path, 'r') as f:
            content = f.read().strip()

        self.assertTrue(len(content) > 0, "pod-container.log should not be empty")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
