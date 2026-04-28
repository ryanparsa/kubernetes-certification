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

class TestAppConfig(unittest.TestCase):
    def test_namespace_exists(self):
        """Namespace configuration exists"""
        ns = kubectl("get", "namespace", "configuration", "-o", "jsonpath={.metadata.name}")
        self.assertEqual(ns, "configuration")

    def test_configmap_data(self):
        """ConfigMap app-config has correct data"""
        data = json.loads(kubectl("get", "configmap", "app-config", "-n", "configuration", "-o", "json"))["data"]
        self.assertEqual(data.get("DB_HOST"), "mysql")
        self.assertEqual(data.get("DB_PORT"), "3306")
        self.assertEqual(data.get("DB_NAME"), "myapp")

    def test_secret_data(self):
        """Secret app-secret has correct data"""
        data = json.loads(kubectl("get", "secret", "app-secret", "-n", "configuration", "-o", "json"))["data"]

        user = base64.b64decode(data.get("DB_USER")).decode()
        password = base64.b64decode(data.get("DB_PASSWORD")).decode()

        self.assertEqual(user, "admin")
        self.assertEqual(password, "s3cr3t")

    def test_pod_uses_configmap_env(self):
        """Pod app-pod uses ConfigMap as environment variables"""
        env_from = json.loads(kubectl("get", "pod", "app-pod", "-n", "configuration", "-o", "jsonpath={.spec.containers[0].envFrom}"))
        found = False
        for item in env_from:
            if "configMapRef" in item and item["configMapRef"].get("name") == "app-config":
                found = True
                break
        self.assertTrue(found, "Pod does not use ConfigMap app-config in envFrom")

    def test_pod_mounts_secret_volume(self):
        """Pod app-pod mounts Secret as volume at /etc/app-secret"""
        pod_json = json.loads(kubectl("get", "pod", "app-pod", "-n", "configuration", "-o", "json"))

        # Check volume
        volumes = pod_json["spec"]["volumes"]
        secret_vol_name = None
        for vol in volumes:
            if "secret" in vol and vol["secret"].get("secretName") == "app-secret":
                secret_vol_name = vol["name"]
                break
        self.assertIsNotNone(secret_vol_name, "Pod does not have a volume for Secret app-secret")

        # Check volume mount
        volume_mounts = pod_json["spec"]["containers"][0]["volumeMounts"]
        found_mount = False
        for mount in volume_mounts:
            if mount["name"] == secret_vol_name and mount["mountPath"] == "/etc/app-secret":
                found_mount = True
                break
        self.assertTrue(found_mount, "Pod does not mount the secret volume at /etc/app-secret")

if __name__ == "__main__":
    unittest.main(verbosity=2)
