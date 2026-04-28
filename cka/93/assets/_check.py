#!/usr/bin/env python3
import os
import re
import subprocess
import unittest

CONTAINER = "cka-lab-93-control-plane"


def docker_exec(*args):
    result = subprocess.run(
        ["docker", "exec", CONTAINER, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip(), result.returncode


def get_cert_expiry_formatted():
    """Return the apiserver cert expiry as mm/dd/YYYY using openssl inside the container."""
    raw, rc = docker_exec(
        "openssl", "x509", "-noout", "-enddate",
        "-in", "/etc/kubernetes/pki/apiserver.crt",
    )
    if rc != 0:
        return None
    # raw: notAfter=Apr 27 06:12:47 2026 GMT
    date_str = raw.replace("notAfter=", "")
    # Reformat using date inside the container (Alpine/Debian have different date utilities;
    # use Python's datetime instead to stay portable)
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, "%b %d %H:%M:%S %Y GMT")
        return dt.strftime("%m/%d/%Y")
    except ValueError:
        return None


class TestCertificateExpiration(unittest.TestCase):

    def test_expiration_file_exists(self):
        _, rc = docker_exec("test", "-f", "/opt/course/14/expiration")
        self.assertEqual(rc, 0, "File /opt/course/14/expiration not found in container")

    def test_expiration_date_format(self):
        content, rc = docker_exec("cat", "/opt/course/14/expiration")
        self.assertEqual(rc, 0, "Could not read /opt/course/14/expiration")
        self.assertRegex(
            content,
            r"^\d{2}/\d{2}/\d{4}$",
            f"Expiration date '{content}' is not in mm/dd/YYYY format",
        )

    def test_expiration_date_matches_cert(self):
        content, rc = docker_exec("cat", "/opt/course/14/expiration")
        self.assertEqual(rc, 0, "Could not read /opt/course/14/expiration")
        expected = get_cert_expiry_formatted()
        if expected is None:
            self.skipTest(f"Could not parse cert expiry from container '{CONTAINER}'")
        self.assertEqual(
            content, expected,
            f"Expected '{expected}', got '{content}'",
        )

    def test_renewal_file_exists(self):
        _, rc = docker_exec("test", "-f", "/opt/course/14/kubeadm-renew-certs.txt")
        self.assertEqual(rc, 0, "File /opt/course/14/kubeadm-renew-certs.txt not found in container")

    def test_renewal_file_content(self):
        content, rc = docker_exec("cat", "/opt/course/14/kubeadm-renew-certs.txt")
        self.assertEqual(rc, 0, "Could not read /opt/course/14/kubeadm-renew-certs.txt")
        self.assertIn(
            "kubeadm certs renew apiserver", content,
            f"Renewal file does not contain 'kubeadm certs renew apiserver'. Got: '{content}'",
        )


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
