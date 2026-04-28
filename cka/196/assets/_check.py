#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# Use local kubeconfig if it exists, otherwise rely on environment (CI)
KUBECONFIG = os.path.join(SCRIPT_DIR, "..", "lab", "kubeconfig.yaml")
if not os.path.exists(KUBECONFIG):
    KUBECONFIG = os.environ.get("KUBECONFIG", "")

LAB_DIR = os.path.join(SCRIPT_DIR, "..", "lab")

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

class TestTigersReunite(unittest.TestCase):
    def test_pod_exists_and_running(self):
        res = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.status.phase}")
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout.strip(), "Running")

    def test_pod_image(self):
        res = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(res.stdout.strip(), "httpd:2.4-alpine")

    def test_pod_labels(self):
        res = kubectl("get", "pod", "tigers-reunite", "-n", "project-tiger", "-o", "jsonpath={.metadata.labels}")
        import json
        labels = json.loads(res.stdout.strip())
        self.assertEqual(labels.get("pod"), "container")
        self.assertEqual(labels.get("container"), "pod")

    def test_pod_container_file(self):
        file_path = os.path.join(LAB_DIR, "pod-container.txt")
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            content = f.read().strip().split()
            self.assertEqual(len(content), 2)
            # content[0] is container ID, content[1] is runtimeType
            self.assertTrue(len(content[0]) > 0)
            self.assertIn("io.containerd", content[1])

    def test_container_log_file(self):
        file_path = os.path.join(LAB_DIR, "container.log")
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertTrue(len(content) > 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
