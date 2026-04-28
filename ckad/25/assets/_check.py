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


class TestMysqlSecretCredentials(unittest.TestCase):

    def test_secret_exists_with_correct_keys(self):
        username = kubectl(
            "get", "secret", "db-credentials", "-n", "workloads",
            "-o", "jsonpath={.data.username}",
        )
        password = kubectl(
            "get", "secret", "db-credentials", "-n", "workloads",
            "-o", "jsonpath={.data.password}",
        )
        random = kubectl(
            "get", "secret", "db-credentials", "-n", "workloads",
            "-o", "jsonpath={.data.random}",
        )
        self.assertTrue(username, "Secret key 'username' is missing or empty")
        self.assertTrue(password, "Secret key 'password' is missing or empty")
        self.assertTrue(random, "Secret key 'random' is missing or empty")

    def test_pod_is_running(self):
        phase = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.status.phase}",
        )
        self.assertEqual(phase, "Running")

    def test_env_db_user_from_secret(self):
        name = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_USER')].valueFrom.secretKeyRef.name}",
        )
        key = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_USER')].valueFrom.secretKeyRef.key}",
        )
        self.assertEqual(name, "db-credentials")
        self.assertEqual(key, "username")

    def test_env_db_password_from_secret(self):
        name = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_PASSWORD')].valueFrom.secretKeyRef.name}",
        )
        key = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='DB_PASSWORD')].valueFrom.secretKeyRef.key}",
        )
        self.assertEqual(name, "db-credentials")
        self.assertEqual(key, "password")

    def test_env_mysql_random_root_password_from_secret(self):
        name = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='MYSQL_RANDOM_ROOT_PASSWORD')].valueFrom.secretKeyRef.name}",
        )
        key = kubectl(
            "get", "pod", "secure-pod", "-n", "workloads",
            "-o", "jsonpath={.spec.containers[0].env[?(@.name=='MYSQL_RANDOM_ROOT_PASSWORD')].valueFrom.secretKeyRef.key}",
        )
        self.assertEqual(name, "db-credentials")
        self.assertEqual(key, "random")


class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
