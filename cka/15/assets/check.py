#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")
COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestClusterEventLogging(unittest.TestCase):
    def test_cluster_events_script_exists(self):
        path = os.path.join(COURSE_DIR, "cluster_events.sh")
        self.assertTrue(os.path.exists(path), f"{path} does not exist")

    def test_cluster_events_script_valid(self):
        path = os.path.join(COURSE_DIR, "cluster_events.sh")
        with open(path, 'r') as f:
            content = f.read()
        self.assertIn("kubectl get events -A", content)
        self.assertIn("--sort-by=.metadata.creationTimestamp", content)

    def test_pod_kill_log_exists(self):
        path = os.path.join(COURSE_DIR, "pod_kill.log")
        self.assertTrue(os.path.exists(path), f"{path} does not exist")
        self.assertGreater(os.path.getsize(path), 0, f"{path} is empty")

    def test_container_kill_log_exists(self):
        path = os.path.join(COURSE_DIR, "container_kill.log")
        self.assertTrue(os.path.exists(path), f"{path} does not exist")
        self.assertGreater(os.path.getsize(path), 0, f"{path} is empty")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
