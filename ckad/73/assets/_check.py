#!/usr/bin/env python3

import os
import subprocess
import unittest

# Try local kubeconfig first (for local dev), then fallback to default (for CI)
LOCAL_KUBECONFIG = os.path.join(os.path.dirname(__file__), "..", "lab", "kubeconfig.yaml")
KUBECONFIG = LOCAL_KUBECONFIG if os.path.exists(LOCAL_KUBECONFIG) else os.environ.get("KUBECONFIG")


def kubectl(*args):
    cmd = ["kubectl"]
    if KUBECONFIG:
        cmd.extend(["--kubeconfig", KUBECONFIG])
    cmd.extend(args)
    result = subprocess.run(
        cmd,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


class TestSecretEnvVar(unittest.TestCase):

    def test_secret_exists(self):
        name = kubectl(
            "get", "secret", "db-credentials", "-n", "default",
            "-o", "jsonpath={.metadata.name}",
        )
        self.assertEqual(name, "db-credentials", "Secret 'db-credentials' not found in default namespace")

    def test_secret_contains_db_password_key(self):
        value = kubectl(
            "get", "secret", "db-credentials", "-n", "default",
            "-o", "jsonpath={.data.db-password}",
        )
        self.assertTrue(value, "Secret key 'db-password' is missing or empty")

    def test_pod_is_running(self):
        phase = kubectl(
            "get", "pod", "backend", "-n", "default",
            "-o", "jsonpath={.status.phase}",
        )
        self.assertEqual(phase, "Running", "Pod 'backend' is not in Running phase")

    def test_pod_db_password_env_from_secret(self):
        secret_name = kubectl(
            "get", "pod", "backend", "-n", "default",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_PASSWORD')].valueFrom.secretKeyRef.name}",
        )
        secret_key = kubectl(
            "get", "pod", "backend", "-n", "default",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_PASSWORD')].valueFrom.secretKeyRef.key}",
        )
        self.assertEqual(secret_name, "db-credentials", "DB_PASSWORD env var is not sourced from 'db-credentials' secret")
        self.assertEqual(secret_key, "db-password", "DB_PASSWORD env var is not sourced from 'db-password' key")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
