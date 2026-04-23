#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")
ANSWER_FILE = os.path.join(COURSE_DIR, "controlplane-components.txt")

class TestGetControlplaneInformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.answers = {}
        if os.path.exists(ANSWER_FILE):
            with open(ANSWER_FILE, 'r') as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        cls.answers[key.strip()] = value.strip()

    def test_kubelet_info_valid(self):
        self.assertIn('kubelet', self.answers)
        self.assertEqual(self.answers['kubelet'], 'process')

    def test_kube_apiserver_info_valid(self):
        self.assertIn('kube-apiserver', self.answers)
        self.assertEqual(self.answers['kube-apiserver'], 'static-pod')

    def test_kube_scheduler_info_valid(self):
        self.assertIn('kube-scheduler', self.answers)
        self.assertEqual(self.answers['kube-scheduler'], 'static-pod')

    def test_kube_controller_manager_info_valid(self):
        self.assertIn('kube-controller-manager', self.answers)
        self.assertEqual(self.answers['kube-controller-manager'], 'static-pod')

    def test_etcd_info_valid(self):
        self.assertIn('etcd', self.answers)
        self.assertEqual(self.answers['etcd'], 'static-pod')

    def test_dns_info_valid(self):
        self.assertIn('dns', self.answers)
        self.assertEqual(self.answers['dns'], 'pod coredns')

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
