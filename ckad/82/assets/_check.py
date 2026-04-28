#!/usr/bin/env python3
import os
import subprocess
import unittest
import json
import base64

KUBECONFIG_FILE = os.path.join(os.path.dirname(__file__), "kubeconfig.yaml")

def kubectl(*args):
    cmd = ["kubectl"]
    if os.path.exists(KUBECONFIG_FILE) and "KUBECONFIG" not in os.environ:
        cmd.extend(["--kubeconfig", KUBECONFIG_FILE])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

class TestSecretVolume(unittest.TestCase):
    def test_secret_exists_with_keys(self):
        """Secret db-secret exists in secrets-ns with keys username and password"""
        data = json.loads(kubectl("get", "secret", "db-secret", "-n", "secrets-ns", "-o", "json"))["data"]

        username = base64.b64decode(data.get("username", "")).decode()
        password = base64.b64decode(data.get("password", "")).decode()

        self.assertEqual(username, "admin", "Secret key 'username' should be 'admin'")
        self.assertEqual(password, "SuperSecret123", "Secret key 'password' should be 'SuperSecret123'")

    def test_pod_is_running(self):
        """Pod secret-pod in secrets-ns is Running"""
        phase = kubectl("get", "pod", "secret-pod", "-n", "secrets-ns", "-o", "jsonpath={.status.phase}")
        self.assertEqual(phase, "Running", "Pod secret-pod should be in Running phase")

    def test_secret_mounted_as_volume(self):
        """Secret is mounted as a volume at /etc/secrets inside the container"""
        pod_json = json.loads(kubectl("get", "pod", "secret-pod", "-n", "secrets-ns", "-o", "json"))

        # Check volume references db-secret
        volumes = pod_json["spec"]["volumes"]
        secret_vol_name = None
        for vol in volumes:
            if "secret" in vol and vol["secret"].get("secretName") == "db-secret":
                secret_vol_name = vol["name"]
                break
        self.assertIsNotNone(secret_vol_name, "Pod does not have a volume for Secret db-secret")

        # Check volume is mounted at /etc/secrets
        volume_mounts = pod_json["spec"]["containers"][0]["volumeMounts"]
        found_mount = False
        for mount in volume_mounts:
            if mount["name"] == secret_vol_name and mount["mountPath"] == "/etc/secrets":
                found_mount = True
                break
        self.assertTrue(found_mount, "Pod does not mount the secret volume at /etc/secrets")

if __name__ == "__main__":
    unittest.main(verbosity=2)
