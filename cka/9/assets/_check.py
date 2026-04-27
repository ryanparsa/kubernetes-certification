#!/usr/bin/env python3
import json
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
SCRIPT_DIR = os.path.dirname(__file__)
RESULT_JSON = os.path.join(SCRIPT_DIR, "..", "lab", "9", "result.json")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestContactK8sApi(unittest.TestCase):

    def test_pod_exists(self):
        name = kubectl("get", "pod", "api-contact", "-n", "project-swan",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "api-contact")

    def test_pod_uses_service_account(self):
        sa = kubectl("get", "pod", "api-contact", "-n", "project-swan",
                     "-o", "jsonpath={.spec.serviceAccountName}")
        self.assertEqual(sa, "secret-reader")

    def test_pod_is_running(self):
        phase = kubectl("get", "pod", "api-contact", "-n", "project-swan",
                        "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running")

    def test_result_json_exists(self):
        self.assertTrue(os.path.isfile(RESULT_JSON),
                        f"lab/9/result.json does not exist (expected at {RESULT_JSON})")

    def test_result_json_is_secret_list(self):
        with open(RESULT_JSON) as f:
            data = json.load(f)
        self.assertEqual(data.get("kind"), "SecretList")

    def test_result_json_contains_read_me_secret(self):
        with open(RESULT_JSON) as f:
            data = json.load(f)
        names = [item.get("metadata", {}).get("name") for item in data.get("items", [])]
        self.assertIn("read-me", names)


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
