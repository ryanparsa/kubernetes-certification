#!/usr/bin/env python3
import json
import os
import subprocess
import unittest

KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")


def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def helm(*args):
    env = os.environ.copy()
    env["KUBECONFIG"] = KUBECONFIG
    result = subprocess.run(
        ["helm", *args],
        capture_output=True, text=True, env=env,
    )
    return result.stdout.strip()


class TestMinioOperator(unittest.TestCase):

    def test_namespace_exists(self):
        name = kubectl("get", "namespace", "minio", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "minio")

    def test_helm_release_deployed(self):
        out = helm("-n", "minio", "ls", "-o", "json")
        releases = json.loads(out) if out else []
        names = [r.get("name") for r in releases]
        self.assertIn("minio-operator", names)

    def test_tenant_exists(self):
        name = kubectl("get", "tenant", "tenant", "-n", "minio",
                       "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "tenant")

    def test_tenant_enable_sftp(self):
        value = kubectl("get", "tenant", "tenant", "-n", "minio",
                        "-o", "jsonpath={.spec.features.enableSFTP}")
        self.assertEqual(value, "true")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
