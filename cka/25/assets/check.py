#!/usr/bin/env python3
import os
import unittest
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ANS_FILE = os.path.join(SCRIPT_DIR, "..", "course", "controlplane-components.txt")

class QuietResult(unittest.TextTestResult):
    def addSuccess(self, test):
        pass
    def addError(self, test, err):
        super().addError(test, err)
    def addFailure(self, test, err):
        super().addFailure(test, err)

class TestControlplaneInformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = {}
        if os.path.exists(ANS_FILE):
            with open(ANS_FILE, 'r') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        cls.findings[key.strip()] = value.strip()

    def test_kubelet_info_valid(self):
        self.assertEqual(self.findings.get("kubelet"), "process")

    def test_kube_apiserver_info_valid(self):
        self.assertEqual(self.findings.get("kube-apiserver"), "static-pod")

    def test_kube_scheduler_info_valid(self):
        self.assertEqual(self.findings.get("kube-scheduler"), "static-pod")

    def test_kube_controller_manager_info_valid(self):
        self.assertEqual(self.findings.get("kube-controller-manager"), "static-pod")

    def test_etcd_info_valid(self):
        self.assertEqual(self.findings.get("etcd"), "static-pod")

    def test_dns_info_valid(self):
        self.assertEqual(self.findings.get("dns"), "pod coredns")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=QuietResult, verbosity=0)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestControlplaneInformation)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
