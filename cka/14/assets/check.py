#!/usr/bin/env python3
import os
import subprocess
import unittest
from datetime import datetime

KUBECONFIG = os.getenv("KUBECONFIG", os.path.join(os.path.dirname(__file__), "kubeconfig.yaml"))
COURSE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "course"))

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

def get_cluster_name():
    # Try to derive cluster name from the script path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lab_id = os.path.basename(os.path.dirname(script_dir))
    exam = os.path.basename(os.path.dirname(os.path.dirname(script_dir)))
    return f"{exam}-lab-{lab_id}"

class TestCertificateExpiration(unittest.TestCase):
    def test_expiration_file_exists(self):
        path = os.path.join(COURSE_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/course/expiration not found")

    def test_expiration_file_matches_cluster(self):
        path = os.path.join(COURSE_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/course/expiration not found")

        with open(path) as f:
            file_content = f.read().strip()

        cluster_name = get_cluster_name()
        # Get expiration from cluster
        cmd = ["docker", "exec", f"{cluster_name}-control-plane", "openssl", "x509", "-noout", "-enddate", "-in", "/etc/kubernetes/pki/apiserver.crt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Failed to get cert info from {cluster_name}-control-plane")

        # notAfter=Oct 29 14:19:27 2025 GMT
        expected_expiry = result.stdout.strip().split("=")[1]

        # Normalize both dates for comparison if needed, or just compare strings if fix.sh is exact
        self.assertEqual(file_content, expected_expiry, "Expiration date in file does not match cluster certificate")

    def test_renewal_script_exists(self):
        path = os.path.join(COURSE_DIR, "kubeadm-renew-certs.sh")
        self.assertTrue(os.path.isfile(path), "File cka/14/course/kubeadm-renew-certs.sh not found")

    def test_renewal_script_content(self):
        path = os.path.join(COURSE_DIR, "kubeadm-renew-certs.sh")
        self.assertTrue(os.path.isfile(path), "File cka/14/course/kubeadm-renew-certs.sh not found")
        with open(path) as f:
            content = f.read().strip()
        self.assertIn("kubeadm certs renew apiserver", content)

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    import sys
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
