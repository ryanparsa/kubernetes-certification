#!/usr/bin/env python3
import os
import unittest

LAB_DIR = os.path.join(os.path.dirname(__file__), "..", "lab")


def read_file(name):
    with open(os.path.join(LAB_DIR, name)) as f:
        return f.read().strip()


class TestContexts(unittest.TestCase):

    def test_contexts_has_three_lines(self):
        lines = [l for l in read_file("contexts").splitlines() if l.strip()]
        self.assertEqual(len(lines), 3)

    def test_contexts_contains_all_names(self):
        contents = read_file("contexts")
        for name in ("cluster-admin", "cluster-w100", "cluster-w200"):
            self.assertIn(name, contents)

    def test_current_context(self):
        value = read_file("current-context")
        self.assertEqual(value, "cluster-w200")

    def test_cert_is_pem(self):
        cert = read_file("cert")
        self.assertTrue(cert.startswith("-----BEGIN CERTIFICATE-----"),
                        "cert does not start with PEM header")
        self.assertTrue(cert.endswith("-----END CERTIFICATE-----"),
                        "cert does not end with PEM footer")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
