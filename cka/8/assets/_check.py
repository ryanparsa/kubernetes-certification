#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

def get_nodes():
    out = kubectl("get", "nodes",
                  "-o", "jsonpath={range .items[*]}{.metadata.name},{.status.conditions[-1].type},{.status.conditions[-1].status},{.status.nodeInfo.kubeletVersion}{'\\n'}{end}")
    return [line.split(",") for line in out.splitlines() if line]

class TestNodeJoinAndUpgrade(unittest.TestCase):

    def setUp(self):
        self.nodes = get_nodes()

    def test_worker_node_joined(self):
        cp_labels = kubectl("get", "nodes",
                            "-l", "node-role.kubernetes.io/control-plane",
                            "-o", "jsonpath={.items[*].metadata.name}").split()
        all_names = [n[0] for n in self.nodes]
        workers = [n for n in all_names if n not in cp_labels]
        self.assertGreater(len(workers), 0, "No worker node found in the cluster")

    def test_all_nodes_ready(self):
        not_ready = [n[0] for n in self.nodes if n[1] != "Ready" or n[2] != "True"]
        self.assertEqual(not_ready, [], f"Nodes not Ready: {not_ready}")

    def test_all_nodes_same_version(self):
        versions = {n[3] for n in self.nodes}
        self.assertEqual(len(versions), 1,
                         f"Nodes are running different versions: {versions}")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
