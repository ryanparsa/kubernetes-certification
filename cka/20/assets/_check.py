#!/usr/bin/env python3

import os
import re
import unittest

CERT_FILE = os.path.join(os.path.dirname(__file__), "..", "course", "certificate-info.txt")


class TestKubeletCertInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(CERT_FILE):
            raise FileNotFoundError(
                f"certificate-info.txt not found at {CERT_FILE}. Run fix.sh first."
            )
        with open(CERT_FILE) as f:
            cls.content = f.read()

    def test_client_cert_issuer(self):
        self.assertIn("Issuer: CN = kubernetes", self.content)

    def test_client_cert_eku(self):
        self.assertIn("TLS Web Client Authentication", self.content)

    def test_server_cert_issuer(self):
        self.assertRegex(self.content, r"Issuer: CN = cka-lab-worker-ca@\d+")

    def test_server_cert_eku(self):
        self.assertIn("TLS Web Server Authentication", self.content)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
