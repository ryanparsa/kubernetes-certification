#!/usr/bin/env python3
import json
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
SCRIPT_DIR = os.path.dirname(__file__)
RESULT_JSON = os.path.join(SCRIPT_DIR, "..", "lab", "result.json")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestContactK8sApi(unittest.TestCase):

    def test_pod_exists(self):
        """Pod api-contact exists in namespace project-swan"""
        name = kubectl("get", "pod", "api-contact", "-n", "project-swan",
                       "--ignore-not-found", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "api-contact", "Pod api-contact does not exist in project-swan")

    def test_result_file_contains_api_response_with_secrets(self):
        """lab/result.json contains correct API response with secrets"""
        self.assertTrue(os.path.isfile(RESULT_JSON),
                        f"lab/result.json does not exist (expected at {RESULT_JSON})")
        with open(RESULT_JSON) as f:
            data = json.load(f)
        self.assertEqual(data.get("kind"), "SecretList",
                         f"Expected SecretList, got {data.get('kind')!r}")
        names = [item.get("metadata", {}).get("name") for item in data.get("items", [])]
        self.assertIn("read-me", names,
                      "SecretList should include the 'read-me' secret")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
