#!/usr/bin/env python3
import os
import subprocess
import unittest
import json

KUBECONFIG = os.environ.get("KUBECONFIG") or os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class QuietResult(unittest.TextTestResult):
    def addSuccess(self, test):
        pass

    def addError(self, test, err):
        super().addError(test, err)

    def addFailure(self, test, err):
        super().addFailure(test, err)


class TestCRDBackup(unittest.TestCase):
    def setUp(self):
        crd_json = kubectl("get", "crd", "backups.data.example.com", "-o", "json")
        self.crd = json.loads(crd_json) if crd_json else {}

    def test_crd_exists_with_correct_group_and_version(self):
        group = self.crd.get("spec", {}).get("group", "")
        self.assertEqual(group, "data.example.com")

        versions = [v.get("name") for v in self.crd.get("spec", {}).get("versions", [])]
        self.assertIn("v1alpha1", versions)

    def test_crd_schema_has_required_source_and_destination(self):
        versions = self.crd.get("spec", {}).get("versions", [])
        v1alpha1 = next((v for v in versions if v.get("name") == "v1alpha1"), None)
        self.assertIsNotNone(v1alpha1, "version v1alpha1 not found")

        spec_props = (
            v1alpha1.get("schema", {})
            .get("openAPIV3Schema", {})
            .get("properties", {})
            .get("spec", {})
        )

        required = spec_props.get("required", [])
        self.assertIn("source", required)
        self.assertIn("destination", required)

        props = spec_props.get("properties", {})
        self.assertEqual(props.get("source", {}).get("type"), "string")
        self.assertEqual(props.get("destination", {}).get("type"), "string")


if __name__ == "__main__":
    runner = unittest.TextTestRunner(resultclass=QuietResult, verbosity=2)
    unittest.main(testRunner=runner)
