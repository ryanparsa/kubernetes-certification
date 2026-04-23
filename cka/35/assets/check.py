#!/usr/bin/env python3
import os
import unittest

COURSE_DIR = os.path.join(os.path.dirname(__file__), "..", "course")
INFO_FILE = os.path.join(COURSE_DIR, "etcd-info.txt")

class TestEtcdInformation(unittest.TestCase):

    def test_file_exists(self):
        self.assertTrue(os.path.exists(INFO_FILE), f"{INFO_FILE} does not exist")

    def test_server_private_key_location(self):
        with open(INFO_FILE, "r") as f:
            content = f.read()
        self.assertIn("Server private key location: /etc/kubernetes/pki/etcd/server.key", content)

    def test_server_certificate_expiration_date(self):
        with open(INFO_FILE, "r") as f:
            content = f.read()
        self.assertIn("Server certificate expiration date: Oct 29 14:19:29 2025 GMT", content)

    def test_client_cert_auth_enabled(self):
        with open(INFO_FILE, "r") as f:
            content = f.read()
        self.assertIn("Is client certificate authentication enabled: yes", content)

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
