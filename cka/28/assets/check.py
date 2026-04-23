#!/usr/bin/env python3
import os
import subprocess
import unittest
import base64

KUBECONFIG = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    result = subprocess.run(
        ["kubectl", "--kubeconfig", KUBECONFIG, *args],
        capture_output=True, text=True,
    )
    return result.stdout.strip()

class TestSecretPod(unittest.TestCase):

    def test_secret1_exists(self):
        name = kubectl("get", "secret", "secret1", "-n", "secret", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "secret1")

    def test_secret2_exists(self):
        name = kubectl("get", "secret", "secret2", "-n", "secret", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "secret2")

        # Verify values
        user_b64 = kubectl("get", "secret", "secret2", "-n", "secret", "-o", "jsonpath={.data.user}")
        pass_b64 = kubectl("get", "secret", "secret2", "-n", "secret", "-o", "jsonpath={.data.pass}")

        self.assertEqual(base64.b64decode(user_b64).decode(), "user1")
        self.assertEqual(base64.b64decode(pass_b64).decode(), "1234")

    def test_pod_exists(self):
        name = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(name, "secret-pod")

    def test_pod_single_container(self):
        containers = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[*].name}")
        self.assertEqual(len(containers.split()), 1)

    def test_pod_container_image(self):
        image = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].image}")
        self.assertEqual(image, "busybox:1")

    def test_pod_mounts_secret1_readonly(self):
        # Check volume
        vol_secret_name = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.volumes[?(@.name=='secret1')].secret.secretName}")
        self.assertEqual(vol_secret_name, "secret1")

        # Check mount path and readOnly
        mount_path = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].volumeMounts[?(@.name=='secret1')].mountPath}")
        self.assertEqual(mount_path, "/tmp/secret1")

        read_only = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].volumeMounts[?(@.name=='secret1')].readOnly}")
        self.assertEqual(read_only, "true")

    def test_pod_has_secret2_env(self):
        # APP_USER
        env_user_name = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].env[?(@.name=='APP_USER')].valueFrom.secretKeyRef.name}")
        env_user_key = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].env[?(@.name=='APP_USER')].valueFrom.secretKeyRef.key}")
        self.assertEqual(env_user_name, "secret2")
        self.assertEqual(env_user_key, "user")

        # APP_PASS
        env_pass_name = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].env[?(@.name=='APP_PASS')].valueFrom.secretKeyRef.name}")
        env_pass_key = kubectl("get", "pod", "secret-pod", "-n", "secret", "-o", "jsonpath={.spec.containers[0].env[?(@.name=='APP_PASS')].valueFrom.secretKeyRef.key}")
        self.assertEqual(env_pass_name, "secret2")
        self.assertEqual(env_pass_key, "pass")

class QuietResult(unittest.TextTestResult):
    def printErrors(self):
        pass

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, resultclass=QuietResult)
    unittest.main(testRunner=runner)
