#!/usr/bin/env python3
import os
import unittest

LAB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lab")

class TestClusterEventLogging(unittest.TestCase):

    def test_cluster_events_script_exists(self):
        filepath = os.path.join(LAB_DIR, "cluster_events.sh")
        self.assertTrue(os.path.exists(filepath), "cluster_events.sh does not exist")

    def test_cluster_events_script_content(self):
        filepath = os.path.join(LAB_DIR, "cluster_events.sh")
        with open(filepath, 'r') as f:
            content = f.read()
        self.assertIn("kubectl get events", content)
        self.assertIn("--sort-by=.metadata.creationTimestamp", content)

    def test_pod_kill_log_exists(self):
        filepath = os.path.join(LAB_DIR, "pod_kill.log")
        self.assertTrue(os.path.exists(filepath), "pod_kill.log does not exist")

    def test_pod_kill_log_content(self):
        filepath = os.path.join(LAB_DIR, "pod_kill.log")
        with open(filepath, 'r') as f:
            content = f.read()
        # Common events when a pod is deleted and recreated by a DaemonSet
        self.assertTrue(any(word in content for word in ["Killing", "SuccessfulCreate", "Scheduled", "Started"]),
                        f"pod_kill.log does not contain expected events. Content: {content[:100]}...")

    def test_container_kill_log_exists(self):
        filepath = os.path.join(LAB_DIR, "container_kill.log")
        self.assertTrue(os.path.exists(filepath), "container_kill.log does not exist")

    def test_container_kill_log_content(self):
        filepath = os.path.join(LAB_DIR, "container_kill.log")
        with open(filepath, 'r') as f:
            content = f.read()
        # Common events when a container is killed and restarted by Kubelet
        self.assertTrue(any(word in content for word in ["Started", "Created"]),
                        f"container_kill.log does not contain expected events. Content: {content[:100]}...")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
