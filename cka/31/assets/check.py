#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")
CLUSTER_INFO_FILE = os.path.join(COURSE_DIR, "cluster-info")

class TestClusterInformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CLUSTER_INFO_FILE):
            raise unittest.SkipTest(f"{CLUSTER_INFO_FILE} not found")

        cls.answers = {}
        with open(CLUSTER_INFO_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line and not line.startswith('#'):
                    key, value = line.split(':', 1)
                    cls.answers[key.strip()] = value.strip()

    def test_answer_1_valid(self):
        self.assertEqual(self.answers.get('1'), "1", "Incorrect number of controlplane nodes")

    def test_answer_2_valid(self):
        self.assertEqual(self.answers.get('2'), "0", "Incorrect number of worker nodes")

    def test_answer_3_valid(self):
        self.assertEqual(self.answers.get('3'), "10.96.0.0/12", "Incorrect Service CIDR")

    def test_answer_4_valid(self):
        # Allow some flexibility in formatting for answer 4
        ans4 = self.answers.get('4', "")
        self.assertIn("kindnet", ans4.lower())
        self.assertIn("/etc/cni/net.d/10-kindnet.conflist", ans4)

    def test_answer_5_valid(self):
        self.assertEqual(self.answers.get('5'), "-cka-lab-31-control-plane", "Incorrect static pod suffix")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
