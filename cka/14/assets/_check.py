#!/usr/bin/env python3
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
LAB_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lab"))


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestCertificateExpiration(unittest.TestCase):

    def test_expiration_file_exists(self):
        path = os.path.join(LAB_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/expiration not found")

    def test_expiration_file_not_empty(self):
        path = os.path.join(LAB_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/expiration not found")
        content = open(path).read().strip()
        self.assertTrue(content, "File cka/14/lab/expiration is empty")

    def test_renewal_script_exists(self):
        path = os.path.join(LAB_DIR, "kubeadm-renew-certs.sh")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/kubeadm-renew-certs.sh not found")

    def test_renewal_script_content(self):
        path = os.path.join(LAB_DIR, "kubeadm-renew-certs.sh")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/kubeadm-renew-certs.sh not found")
        content = open(path).read().strip()
        self.assertIn("kubeadm certs renew apiserver", content)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
