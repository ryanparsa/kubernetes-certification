#!/usr/bin/env python3
import os
import subprocess
import unittest

LAB_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lab"))
CONTAINER = "cka-lab-14-control-plane"


def get_cert_expiration():
    result = subprocess.run(
        ["docker", "exec", CONTAINER,
         "openssl", "x509", "-noout", "-enddate", "-in", "/etc/kubernetes/pki/apiserver.crt"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    # output: notAfter=Oct 29 14:19:27 2025 GMT
    return result.stdout.strip().replace("notAfter=", "")


class TestCertificateExpiration(unittest.TestCase):

    def test_expiration_file_exists(self):
        path = os.path.join(LAB_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/expiration not found")

    def test_expiration_file_matches_cert(self):
        path = os.path.join(LAB_DIR, "expiration")
        self.assertTrue(os.path.isfile(path), "File cka/14/lab/expiration not found")
        cert_date = get_cert_expiration()
        if cert_date is None:
            self.skipTest(f"Could not read cert from container '{CONTAINER}' — is the lab running?")
        content = open(path).read().strip()
        self.assertEqual(
            content, cert_date,
            f"Expected openssl Not After date '{cert_date}', got '{content}'"
        )

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
