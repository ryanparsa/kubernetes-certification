#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestUpdateKubernetesVersion(unittest.TestCase):

    def test_all_nodes_ready(self):
        not_ready = kubectl(
            "get", "nodes",
            "-o", "jsonpath={range .items[?(@.status.conditions[-1].type=='Ready')]}"
                  "{.status.conditions[-1].status} {end}",
        )
        for status in not_ready.split():
            self.assertEqual(status, "True", "One or more nodes are not Ready")

    def test_nodes_same_version(self):
        versions = kubectl("get", "nodes", "-o", "jsonpath={range .items[*]}{.status.nodeInfo.kubeletVersion} {end}")
        version_list = versions.split()
        self.assertGreater(len(version_list), 0)
        self.assertEqual(len(set(version_list)), 1, f"Nodes run different versions: {version_list}")

    def test_worker_joined(self):
        node_count = kubectl("get", "nodes", "-o", "jsonpath={range .items[*]}{.metadata.name} {end}")
        self.assertGreaterEqual(len(node_count.split()), 2, "Expected at least 2 nodes (control-plane + worker)")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
