#!/usr/bin/env python3
import os
import unittest

LAB_DIR = os.path.join(os.path.dirname(__file__), "..", "lab")
INFO_FILE = os.path.join(LAB_DIR, "cluster-info")


class TestClusterInformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.answers = {}
        if os.path.exists(INFO_FILE):
            with open(INFO_FILE, "r") as f:
                for line in f:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        cls.answers[key.strip()] = value.strip()

    def test_answer_1_valid(self):
        # How many controlplane Nodes are available?
        self.assertEqual(self.answers.get("1"), "1")

    def test_answer_2_valid(self):
        # How many worker Nodes are available?
        self.assertEqual(self.answers.get("2"), "0")

    def test_answer_3_valid(self):
        # What is the Service CIDR?
        self.assertEqual(self.answers.get("3"), "10.96.0.0/12")

    def test_answer_4_valid(self):
        # Which Networking (or CNI Plugin) is configured and where is its config file?
        ans = self.answers.get("4", "")
        self.assertIn("kindnet", ans)
        self.assertIn("/etc/cni/net.d/10-kindnet.conflist", ans)

    def test_answer_5_valid(self):
        # Which suffix will static Pods have that run on cka-lab-31-control-plane?
        self.assertEqual(self.answers.get("5"), "-cka-lab-31-control-plane")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
