#!/usr/bin/env python3
import os
import subprocess
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.join(SCRIPT_DIR, "..", "course")
ETCD_INFO_FILE = os.path.join(COURSE_DIR, "etcd-info.txt")

LAB_ID = os.path.basename(os.path.dirname(SCRIPT_DIR))
EXAM = os.path.basename(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
CONTROL_PLANE_NODE = f"{EXAM}-lab-{LAB_ID}-control-plane"
ETCD_MANIFEST = "/etc/kubernetes/manifests/etcd.yaml"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

class TestEtcdInformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(ETCD_INFO_FILE):
            cls.etcd_info = {}
            return

        cls.etcd_info = {}
        with open(ETCD_INFO_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    cls.etcd_info[key.strip()] = value.strip()

    def test_file_exists(self):
        self.assertTrue(os.path.exists(ETCD_INFO_FILE), f"{ETCD_INFO_FILE} does not exist")

    def test_server_private_key_location(self):
        expected = run_command(f"docker exec {CONTROL_PLANE_NODE} grep '\\-\\-key-file=' {ETCD_MANIFEST} | cut -d= -f2")
        actual = self.etcd_info.get("Server private key location")
        self.assertEqual(actual, expected)

    def test_server_certificate_expiration_date(self):
        cert_file = run_command(f"docker exec {CONTROL_PLANE_NODE} grep '\\-\\-cert-file=' {ETCD_MANIFEST} | cut -d= -f2")
        expected = run_command(f"docker exec {CONTROL_PLANE_NODE} openssl x509 -noout -enddate -in {cert_file} | cut -d= -f2")
        actual = self.etcd_info.get("Server certificate expiration date")
        self.assertEqual(actual, expected)

    def test_client_certificate_authentication_enabled(self):
        client_auth = run_command(f"docker exec {CONTROL_PLANE_NODE} grep '\\-\\-client-cert-auth=' {ETCD_MANIFEST} | cut -d= -f2")
        expected = "yes" if client_auth == "true" else "no"
        actual = self.etcd_info.get("Is client certificate authentication enabled")
        self.assertEqual(actual, expected)

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
